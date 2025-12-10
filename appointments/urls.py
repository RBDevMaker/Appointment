"App URL routes"
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("service/<int:service_id>/", views.index, name="index-service"),
    path("services/<str:service_ids>/", views.index, name="index-services"),
    path(
        "service/<int:service_id>/hairdresser/<int:hairdresser_id>",
        views.index,
        name="index-hairdresser",
    ),
    path(
        "services/<str:service_ids>/hairdresser/<int:hairdresser_id>",
        views.index,
        name="index-services-hairdresser",
    ),
    path(
        "service/<int:service_id>/hairdresser/<int:hairdresser_id>/date/<str:date_string>",
        views.index,
        name="index-date",
    ),
    path(
        "services/<str:service_ids>/hairdresser/<int:hairdresser_id>/date/<str:date_string>",
        views.index,
        name="index-services-date",
    ),
    path("create", views.create, name="create"),
    path("cancel/<str:token>/", views.cancel, name="cancel"),
    path("setup-admin/", views.setup_admin, name="setup-admin"),
]
