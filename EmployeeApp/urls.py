from django.urls import re_path
from EmployeeApp import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    re_path(r'^department$', views.departmentAPI),
    re_path(r'^department/([0-9]+)$', views.departmentAPI),

    re_path(r'^employee$',views.employeeAPI),
    re_path(r'^employee/([0-9]+)$',views.employeeAPI),

    re_path(r'^employee/savefile',views.SaveFile),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)