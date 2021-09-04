"""apexindustries URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from apex.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Login,name='login'),

    path('Admin-Dashboard/',Admin_Dashboard,name='admin_dashboard'),
    path('User-Account/',User_Account,name='user_account'),
    path('Finished-Material-Stock/',User_Finished_Material,name='user_finished_material'),
    path('Un-Finished-Material-Stock/',User_UnFinished_Material,name='user_unfinished_material'),
    path('Raw-Material-Stock/',User_Raw_Material,name='user_raw_material'),
    path('Essential-Item-Stock/',User_Essential_Material,name='user_essential_material'),
    path('Register/',register, name='register'),
    path('logout/',Logout, name='logout'),
    path('Raw-Material-Stock/raw_save',raw_save,name='raw_save'),
    path('Raw-Material-Stock/raw_delete',raw_delete,name='raw_delete'),
    path('ufm_save/',uf_save,name='uf_save'),
    path('Un-Finished-Material-Stock/ufm_delete',uf_delete,name='uf_delete'),
    path('fm_save/',fm_save,name='fm_save'),
    path('fm_delete/',fm_delete,name='fm_delete'),
    path('Finished-Material-Stock/sale_save',sale_save,name='sale_save'),
    path('Finished-Material-Stock/sale_delete',sale_delete,name='sale_delete'),
    path('Un-Finished-Material-Stock/usale_save',usale_save,name='usale_save'),
    path('Un-Finished-Material-Stock/usale_delete',usale_delete,name='usale_delete'),

    path('Essential-Item-Stock/es_save',es_save,name='es_save'),
    path('Essential-Item-Stock/es_delete',es_delete,name='es_delete'),
    
    path('Essential-Item-Stock/upd_save',upd_save,name='upd_save'),
    path('Essential-Item-Stock/upd_delete',upd_delete,name='upd_delete'),
    path('user_save/',user_save,name='user_save'),
    path('user_delete/',user_delete,name='user_delete'),
    path('save_timmer/',save_timmer,name='save_timmer'),
    path('n_send/',n_send,name='n_send'),
    path('p_user/',p_user,name='p_user'),
    path('noti_alert/',noti_alert,name='noti_alert'),
    path('Essential-Item-Stock/get_es_type/<str:id>/',get_es_type,name='get_es_type'),
    path('Finished-Material-Stock/get_rw_grade/<str:id>/',get_rw_grade,name='get_rw_grade'),
    path('Finished-Material-Stock/get_s_type/<str:id>/',get_s_type,name='get_s_type'),
    path('Un-Finished-Material-Stock/get_us_type/<str:id>/',get_us_type,name='get_us_type'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
