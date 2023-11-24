from ...dependencies.global_var import templates, url_types
from ...modals.website import Website, WebsiteColSchema
from ...modals.server import IPDomainPair, Server
from ...modals.pmta_job import ISPTLDS
# from ...modals.url_pattern import UrlPatterns, UrlPatternsColSchema
from ...database.db_session import msa_db_engine as session
from ...dependencies.oauth import get_user_profile
from ...dependencies.functions import get_user_team_isp, is_valid_email, get_ist
from ...portal_tabs.login.login import ensure_logged_in
from fastapi import APIRouter, Depends
import traceback
import time
import copy
import shutil
import os
import pandas as pd
from datetime import datetime
from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse
# from urllib.parse import urlparse
import validators
from sqlalchemy.exc import SQLAlchemyError
from ...database.db_session import access_right_db_session
from ...modals.access_ctrl import AssetCtrl, TaskCtrl
from ...database import datatables
import re
import logging
import pathlib
import json
import zipfile
import io
import traceback
import subprocess
from ...database.db_session import msa_db_session as session

endpoint = APIRouter(
    prefix=f"/{os.path.split(os.path.split(__file__)[0])[-1]}/{os.path.splitext(os.path.split(__file__)[-1])[0]}",
    dependencies=[Depends(ensure_logged_in)]
)


# ------------------------------------------------------------

@endpoint.get("/", response_class=HTMLResponse)
async def add_viewer(request: Request, session_id=Depends(ensure_logged_in)):
    dt_request = dict(await request.form())
    hiden_cols = {'website_location'}
    tbl_cols = list(WebsiteColSchema().dict(exclude=hiden_cols).keys())

    tbl_col_idx = {col: idx for idx, col in enumerate(tbl_cols)}
    front_end_extra_cols = []
    tbl_col_idx.update({col: len(tbl_cols) + idx for idx, col in enumerate(front_end_extra_cols)})
    default_hidden_columns = []
    column_alias = {}

    return templates.TemplateResponse(f"{request.url.path.rstrip('/')}.html",
                                      {"request": request,

                                       "url_types": url_types,
                                       "tbl_cols": tbl_cols,
                                       "front_end_extra_cols": front_end_extra_cols,
                                       "default_hidden_columns": default_hidden_columns,
                                       "index_of": tbl_col_idx,
                                       "tbl_col_schema": WebsiteColSchema().dict(),
                                       "column_alias": column_alias,
                                       "enumerate": enumerate})


@endpoint.post("/website", response_class=JSONResponse)
async def upload_folder(request: Request, session_id=Depends(ensure_logged_in)):
    user_profile = get_user_profile(session_id)
    print(user_profile)
    emp_name = user_profile["fullname"]
    try:
        form_data = await request.form()
        files = form_data.getlist("multiple_website_folder[]")


        if not files:
            raise Exception("Please upload website source file")

        for file in files:
            file_bytes = await file.read()
            # Read the contents of the zip file
            with zipfile.ZipFile(io.BytesIO(file_bytes), "r") as zip_ref:
                unique_folder_names = set()
                logging.info(f"***************{zip_ref.namelist()}")
                for file_name in zip_ref.namelist():
                    if file_name.endswith('.html'):
                        folder_name = file_name.split('/')[0]
                        unique_folder_names.add(folder_name)

                for folder_name in unique_folder_names:
                    current_directory = []
                    result = subprocess.run(['pwd'], capture_output=True, text=True)
                    print(f"****************** path {result}")
                    if result.returncode == 0:
                        # Get the output of the command
                        output = result.stdout.strip()
                        current_directory.append((output))
                    folder_with_path = os.path.join("app/uploads", "websites")

                    base_dir = os.path.join(current_directory[0], folder_with_path)
                    folder_path = "/".join(base_dir.split("/"))

                    save_file_path = os.path.join(folder_with_path, f"{folder_name}.zip")
                    with open(save_file_path, "wb") as save_file:
                        save_file.write(file_bytes)

                    addWebsiteFolder = Website(
                        website_name=folder_name,
                        timestamp=get_ist(),
                        uploaded_by=emp_name,
                        uploaded_time=get_ist(),
                        website_location=folder_path
                    )

                    try:
                        session.add(addWebsiteFolder)
                        session.commit()

                    except SQLAlchemyError as e:
                        print(f"SQLAlchemyError upload_website_folder: {e}")
                        session.rollback()
                        return {"status": "fail",
                            "error": f"upload_website_folder upload_folder error: {e}; Please try again."}


        return {"status": "success", "message": f"Folder uploaded successfully"}

    except Exception as e:
        traceback.print_exc()
        logging.error(traceback.print_exc())
        print(e)
        return {"status": "fail", "error": str(e)}


@endpoint.post("/config", response_class=JSONResponse)
async def website_config(request: Request, session_id=Depends(ensure_logged_in)):
    user_profile = get_user_profile(session_id)
    emp_id = user_profile["emp_id"]
    try:
        form_data = await request.form()
        selected_option = form_data.get("flexRadioDefault")
        servers = re.split(r"[\s,;\t\n\r]+", form_data.get("server_input"))
        server_name = [item for item in servers if item]
        server_config_dict = {}
        for data in server_name:
            server_n, domain_name, website = data.split(":")
            if not server_config_dict:
                server_config_dict[server_n] = [(domain_name, website)]
            elif server_n in server_config_dict:
                server_config_dict[server_n].append((domain_name, website))
            else:
                server_config_dict[server_n] = [(domain_name, website)]

        for server, config in server_config_dict.items():
            website_dict = {}
            domain_list = []
            server_l = session.query(IPDomainPair.main_domain).filter(IPDomainPair.status == 'active',
                                                                      IPDomainPair.pair_status != 'dissolved',
                                                                      IPDomainPair.server_name == server).all()
            data = session.query(Server.website_info).filter(Server.server_name == server).one()
            if data[0]:
                existing_data = json.loads(data[0])


            if selected_option == "override":
                for (domain,) in server_l:
                    domain_list.append(domain)
                for tuple_value in config:
                    domain_name, website = tuple_value
                    if domain_name in domain_list:
                        website_dict[domain_name] = website
                    else:
                        raise Exception('Domain name does not belong to given server')
                    website = json.dumps(website_dict)
                    try:
                        session.query(Server).filter(Server.server_name == server).update(
                            {Server.website_info: website})
                        session.commit()

                    except SQLAlchemyError as e:
                        print(f"SQLAlchemyError Domain not found: {e}")
                        session.rollback()
                        return {"status": "fail", "error": f"Domain not found: {e}; Please try again."}

            else:
                for (domain,) in server_l:
                    domain_list.append(domain)

                for tuple_value in config:
                    domain_name, website = tuple_value
                    if domain_name in domain_list:
                        website_dict[domain_name] = website
                    else:
                        raise Exception('Domain name does not belong to given server')

                for key in website_dict:
                    if key not in existing_data:
                        existing_data[key] = ""
                    if key in existing_data:
                        existing_data[key] = website_dict[key]

                updated_data = json.dumps(existing_data)

                try:
                    session.query(Server).filter(Server.server_name == server).update(
                        {Server.website_info: updated_data})
                    session.commit()

                except SQLAlchemyError as e:
                    print(f"SQLAlchemyError Domain not found: {e}")
                    session.rollback()
                    return {"status": "fail", "error": f"Domain not found: {e}; Please try again."}
        return {"status": "success", "msg": f"domain web config successfully"}

    except Exception as e:
        traceback.print_exc()
        print(e)
        return {"status": "fail", "error": str(e)}


@endpoint.post("/datatable", response_class=JSONResponse)
async def get_data(request: Request, session_id=Depends(ensure_logged_in)):
    try:
        dt_request = dict(await request.form())

        tbl_cols_to_select = Website.__table__.columns.keys()  # select all columns
        user_profile = get_user_profile(session_id)
        emp_name = user_profile["fullname"]

        for key, val in dt_request.items():
            if val == "uploaded_by":
                if re.match(r"columns\[\d{1,3}]\[name]", key):
                    num = re.search(r"\d{1,3}", key).group()
                    dt_request[f"columns[{num}][search][value]"] = json.dumps(
                        {"optr": "equals", "val": emp_name})

        return datatables.process(dt_request, Website, session, tbl_cols_to_select)
    except Exception as e:
        print(e)
        return {"status": "fail", "error": str(e)}