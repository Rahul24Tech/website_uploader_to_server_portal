from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint, \
    PrimaryKeyConstraint, Index, Text
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property
from sqlalchemy.schema import FetchedValue

from pydantic import BaseModel
from ..dependencies.global_var import col_metadata
import copy
from ..database.db_session import msa_db_engine as engine

base = declarative_base()


class Website(base):
    __tablename__ = 'website'
    website_id = Column(Integer, primary_key=True, autoincrement=True)
    website_name =  Column(String)
    website_location = Column(String)
    timestamp = Column(TIMESTAMP, nullable=False)
    uploaded_by = Column(String(length=15), nullable=False)
    uploaded_time = Column(DateTime, nullable=False)




class WebsiteColSchema(BaseModel):
    website_id: dict = copy.deepcopy(col_metadata["integer"])
    website_name: dict = copy.deepcopy(col_metadata["string"])
    website_location: dict = copy.deepcopy(col_metadata["string"])
    timestamp: dict = copy.deepcopy(col_metadata["timestamp"])
    uploaded_by: dict = copy.deepcopy(col_metadata["string"])
    uploaded_time: dict = copy.deepcopy(col_metadata["timestamp"])



# # initialise schema ---------------------------------------------------------------------
# base.metadata.drop_all(engine)
# base.metadata.create_all(engine)
# end -----------------------------------------------------------------------------------
