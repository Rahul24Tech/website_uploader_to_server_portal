from fastapi.responses import RedirectResponse
import uvicorn
from app.portal_tabs.login import login
from app.dependencies import oauth
from app.dependencies.global_var import server_port
import logging
from fastapi import APIRouter, Depends
from fastapi import Request
from fastapi.responses import HTMLResponse

# ---------------------------------------------------------------------------------------
# Your view import goes below this line

from app.portal_tabs.dashboard import dashboard
from app.portal_tabs.profile import details as profile_details
from app.portal_tabs.offer import viewer as offer_viewer, sponsor_detail, QA_viewer, sponsor_viewer, suppression_viewer ,sensitive_keyword, suppression_status, black_list_email, sponsor_auto_login
from app.portal_tabs.offer import sub_id
from app.portal_tabs.data import select as data_select, query_viewer as data_query_viewer, viewer as data_viewer, select_range
from app.portal_tabs.data import sample_data_viewer
from app.portal_tabs.data import data_sync_supr, data_sync_supr_viewer
from app.portal_tabs.server import assigned_to as server_assigned_to, core_viewer, execution_viewer, executor, \
        ip_domain_pair_viewer, misc_serv_viewer, viewer as server_viewer, vmta, windows_viewer, add as server_add, \
        commission as server_commission, decommission as server_decommission, monitor as server_monitor, \
        sep_ip_commission as server_sep_ip_commission, sep_ip_decommission as server_sep_ip_decommission, custom_commission, monitor_reports, new_server_requests, \
        add_custom_vmta, mse_containers_status, core_containers_status, pmta_configuration, add_extra_domains, add_spf, add_txt, website_uploader, rdns, health_report

from app.portal_tabs.ip_pool import viewer as ip_pool_viewer, assigned_to as ip_pool_assigned_to, add as ip_pool_add
from app.portal_tabs.domain import viewer as domain_viewer, stats as domain_stats, purchase as domain_purchase, \
    purchase_jobs as domain_purchase_jobs, purchase_new as domain_purchase_new, \
    purchase_jobs_new as domain_purchase_jobs_new, push as domain_push, \
    push_jobs as domain_push_jobs, push_new as domain_push_new, push_jobs_new as domain_push_jobs_new, \
    replace as domain_replace
from app.portal_tabs.proxy import viewer as proxy_viewer, assigned_to as proxy_assigned_to, add as proxy_add
from app.portal_tabs.seed import viewer as seed_viewer, assigned_to as seed_assigned_to, add as seed_add
# from app.portal_tabs.templates import text_body, html_body, header, negative, html_template
from app.portal_tabs.templates import html_template
from app.portal_tabs.mailing import submit_job, account_sending_job, pmta_jobs, pmta_live_log,pmta_monitoring, insert_test_ids, generate_uid, \
    negative as negative_viewer, upload_warming_files, avoid_restrictions, s3_buckets, aws_html_img_upload, imgur_img_upload, check_clicks, short_url
from app.portal_tabs.header_testing import send_test_mail
from app.portal_tabs.pmta_job_restriction import applied_restriction_viewer, add_applied_restrictions, add_restrictions
from app.portal_tabs.support import ticket_for_mailer_use, ticket_tech_n_mailer, ticket_for_tech_use, sms_portal_api
from app.portal_tabs.url_patterns import create as create_url_patters
from app.portal_tabs.aws_url_patterns import create_aws_url_patterns
from app.portal_tabs.setting import datatable_col
from app.portal_tabs.reports import test_mailing_user_stats, warming_user_stats, true_mailing_user_stats # user_stats
from app.portal_tabs.reports import revenue_report, asset_report, aggregate_warming_report, aggregate_true_mailing_report, missing_lead, list_data_report, daily_teamwise_revenue
from app.portal_tabs.reports import listing_report , missing_lead_info
from app.portal_tabs.reports import true_mailing_sent_stats, warming_sent_stats, test_mailing_sent_stats, \
    aggregate_stats, server_cost_revenue_report
from app.portal_tabs.incoming_mails import viewer as incoming_email_viewer
from app.portal_tabs.notification import notifications
from app.portal_tabs.faq import faq
from app.portal_tabs.tutorial import tutorial

from app.modals.ip_pool import IPPool
# Importing view ends here --------------------------------------------------------------
from app.dependencies.get_app import app

app.include_router(login.endpoint)
app.include_router(oauth.endpoint)
# ---------------------------------------------------------------------------------------
# Include your imported endpoints below this line
app.include_router(daily_teamwise_revenue.endpoint)
app.include_router(sensitive_keyword.endpoint)
app.include_router(dashboard.endpoint)
app.include_router(profile_details.endpoint)
app.include_router(offer_viewer.endpoint)
app.include_router(sponsor_auto_login.endpoint)
app.include_router(black_list_email.endpoint)
app.include_router(sponsor_detail.endpoint)
app.include_router(sponsor_viewer.endpoint)
app.include_router(suppression_viewer.endpoint)
app.include_router(suppression_status.endpoint)
app.include_router(QA_viewer.endpoint)
app.include_router(data_select.endpoint)
app.include_router(select_range.endpoint)
app.include_router(data_query_viewer.endpoint)
app.include_router(data_viewer.endpoint)
app.include_router(sample_data_viewer.endpoint)
app.include_router(rdns.endpoint)
app.include_router(sub_id.endpoint)
app.include_router(data_sync_supr.endpoint)
app.include_router(data_sync_supr_viewer.endpoint)
app.include_router(server_viewer.endpoint)
app.include_router(website_uploader.endpoint)
app.include_router(server_assigned_to.endpoint)
app.include_router(core_viewer.endpoint)
app.include_router(windows_viewer.endpoint)
app.include_router(misc_serv_viewer.endpoint)
app.include_router(executor.endpoint)
app.include_router(execution_viewer.endpoint)
app.include_router(server_add.endpoint)
app.include_router(server_commission.endpoint)
app.include_router(server_decommission.endpoint)
app.include_router(server_monitor.endpoint)
app.include_router(new_server_requests.endpoint)
app.include_router(add_extra_domains.endpoint)
app.include_router(monitor_reports.endpoint)
app.include_router(mse_containers_status.endpoint)
app.include_router(core_containers_status.endpoint)
app.include_router(server_sep_ip_commission.endpoint)
app.include_router(server_sep_ip_decommission.endpoint)
app.include_router(custom_commission.endpoint)
app.include_router(add_custom_vmta.endpoint)
app.include_router(ip_pool_viewer.endpoint)
app.include_router(ip_pool_assigned_to.endpoint)
app.include_router(ip_pool_add.endpoint)
app.include_router(domain_viewer.endpoint)
app.include_router(domain_stats.endpoint)
app.include_router(domain_purchase.endpoint)
app.include_router(domain_purchase_jobs.endpoint)
app.include_router(domain_purchase_new.endpoint)
app.include_router(domain_purchase_jobs_new.endpoint)
app.include_router(domain_push.endpoint)
app.include_router(domain_push_jobs.endpoint)
app.include_router(domain_push_new.endpoint)
app.include_router(domain_push_jobs_new.endpoint)
app.include_router(domain_replace.endpoint)
app.include_router(vmta.endpoint)
app.include_router(proxy_viewer.endpoint)
app.include_router(proxy_assigned_to.endpoint)
app.include_router(proxy_add.endpoint)
app.include_router(seed_viewer.endpoint)
app.include_router(seed_assigned_to.endpoint)
app.include_router(seed_add.endpoint)
# app.include_router(text_body.endpoint)
# app.include_router(html_body.endpoint)
# app.include_router(header.endpoint)
app.include_router(negative_viewer.endpoint)
app.include_router(html_template.endpoint)
app.include_router(insert_test_ids.endpoint)
app.include_router(submit_job.endpoint)
app.include_router(account_sending_job.endpoint)
app.include_router(pmta_jobs.endpoint)
app.include_router(short_url.endpoint)
app.include_router(pmta_live_log.endpoint)
app.include_router(s3_buckets.endpoint)
app.include_router(aws_html_img_upload.endpoint)
app.include_router(imgur_img_upload.endpoint)
app.include_router(check_clicks.endpoint)
app.include_router(pmta_monitoring.endpoint)
app.include_router(avoid_restrictions.endpoint)
app.include_router(upload_warming_files.endpoint)
app.include_router(generate_uid.endpoint)
app.include_router(ticket_for_mailer_use.endpoint)
app.include_router(ticket_tech_n_mailer.endpoint)
app.include_router(ticket_for_tech_use.endpoint)
app.include_router(sms_portal_api.endpoint)
app.include_router(create_url_patters.endpoint)
app.include_router(create_aws_url_patterns.endpoint)
# app.include_router(custom_report.endpoint)
# app.include_router(user_stats.endpoint)
app.include_router(missing_lead.endpoint)
app.include_router(health_report.endpoint)
app.include_router(list_data_report.endpoint)
app.include_router(test_mailing_user_stats.endpoint)
app.include_router(warming_user_stats.endpoint)
app.include_router(true_mailing_user_stats.endpoint)
app.include_router(aggregate_warming_report.endpoint)
app.include_router(aggregate_true_mailing_report.endpoint)
app.include_router(asset_report.endpoint)
app.include_router(revenue_report.endpoint)
app.include_router(listing_report.endpoint)
app.include_router(missing_lead_info.endpoint)
app.include_router(true_mailing_sent_stats.endpoint)
app.include_router(warming_sent_stats.endpoint)
app.include_router(test_mailing_sent_stats.endpoint)
app.include_router(server_cost_revenue_report.endpoint)
app.include_router(datatable_col.endpoint)
app.include_router(ip_domain_pair_viewer.endpoint)
app.include_router(applied_restriction_viewer.endpoint)
app.include_router(add_applied_restrictions.endpoint)
app.include_router(add_restrictions.endpoint)

app.include_router(incoming_email_viewer.endpoint)
app.include_router(notifications.endpoint)
app.include_router(faq.endpoint)
app.include_router(tutorial.endpoint)

app.include_router(add_txt.endpoint)
app.include_router(add_spf.endpoint)
app.include_router(pmta_configuration.endpoint)
app.include_router(send_test_mail.endpoint)


# Including endpoint ends here ----------------------------------------------------------


@app.get("/", response_class=RedirectResponse)
async def index():
    return RedirectResponse("/dashboard/dashboard/")


if __name__ == "__main__":
    uvicorn.run("main:app", host='10.160.0.6', port=server_port, reload=True, workers=1
                # , debug=True
                , log_config="log.ini"
                # FORWARDED_ALLOW_IPS
                # ssl_keyfile="/etc/letsencrypt/live/mailing.sky3team.com/privkey.pem",
                # ssl_certfile="/etc/letsencrypt/live/mailing.sky3team.com/fullchain.pem",
                # ssl_keyfile="privkey.pem",
                # ssl_certfile="fullchain.pem"
                )
