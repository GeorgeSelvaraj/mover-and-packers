"""
URL configuration for MoversAndPackers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from moverspackers import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ================= CORE =================
    path('', views.index, name='index'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('change_password/', views.change_password, name='change_password'),
    path('manage_admins/', views.manage_admins, name='manage_admins'),
    path('delete_admin/<int:pid>/', views.delete_admin, name='delete_admin'),
    path('toggle_admin/<int:pid>/', views.toggle_admin, name='toggle_admin'),
    path('reset_admin_password/<int:pid>/', views.reset_admin_password, name='reset_admin_password'),
    path('logout/', views.Logout, name='logout'),

    # ================= SERVICES =================
    path('add_services/', views.add_services, name='add_services'),
    path('manage_services/', views.manage_services, name='manage_services'),
    path('edit_service/<int:pid>/', views.edit_service, name='edit_service'),
    path('delete_service/<int:pid>/', views.delete_service, name='delete_service'),
    path('services/', views.services, name='services'),

    # ================= AGENTS =================
    path('agents/', views.agents, name='agents'),
    path('delete_agent/<int:pid>/', views.delete_agent, name='delete_agent'),

    # ================= WEBSITE =================
    path('about/', views.about, name='about'),
    path('request_quote/', views.request_quote, name='request_quote'),

    # ================= BOOKINGS =================
    path('new_booking/', views.new_booking, name='new_booking'),
    path('view_bookingdetail/<int:pid>/', views.view_bookingdetail, name='view_bookingdetail'),
    path('old_booking/', views.old_booking, name='old_booking'),
    path('delete_booking/<int:pid>/', views.delete_booking, name='delete_booking'),

    # ================= CONTACT =================
    path('contact/', views.contact, name='contact'),
    path('unread_queries/', views.unread_queries, name='unread_queries'),
    path('read_queries/', views.read_queries, name='read_queries'),
    path('view_queries/<int:pid>/', views.view_queries, name='view_queries'),
    path('delete_query/<int:pid>/', views.delete_query, name='delete_query'),

    # ================= SEARCH =================
    path('search/', views.search, name='search'),

    # ================= REPORT =================
    path('booking_report/', views.booking_report, name='booking_report'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)