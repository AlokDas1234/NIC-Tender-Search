# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.index, name='views_template_urls'),
#     path('show_data', views.show_data, name='show_data'),
#     path('run_task', views.run_task, name='run_task'),
#     path('show_tender_data', views.show_tender_data, name='show_tender_data'),
# ]


from django.urls import path
from .views import (
    upload_clients,
    get_clients,
    get_tenders,
    # del_tenders,
    del_req,
    run_scraper_task,
    scraper_status,
    download_client_fields_excel,
    download_client_fields,
    login,
    stop_scraper_task,
    get_client_search,
    upload_search_tender_req,
    del_search,
    del_scraper_task,
    add_search_req,
)

urlpatterns = [
    path("upload-clients/", upload_clients),
    path("upload-search-req/", upload_search_tender_req),
    path("clients/", get_clients),
    path("tenders/", get_tenders),
    path("add-search-req/", add_search_req),
    # path("del-tenders/", del_tenders),
    path("del-req/", del_req),
    path("del-search/", del_search),
    path("run-scraper/", run_scraper_task),
    path("del-scraper/<int:search_id>/", del_scraper_task),
    path("run-scraper/<int:search_id>/", run_scraper_task),
    path("scraper-status/", scraper_status),
    path("search/", get_client_search),
    path("client-fields-excel/", download_client_fields_excel),
    path("client-fields/", download_client_fields),
    path("login-page/", login),
    path("stop-scraper/", stop_scraper_task),

]
