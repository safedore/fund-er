"""crowd_funding URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from myapp import views

urlpatterns = [
    path('login/', views.login),
    path('login_post/', views.login_post),
    path('admin_home/', views.admin_home),

    path('admin_add_fund_categories/', views.admin_add_fund_categories),
    path('admin_add_fund_categories_post/', views.admin_add_fund_categories_post),
    path('admin_view_fund_categories/', views.admin_view_fund_categories),
    path('admin_delete_fund_categories/<id>', views.admin_delete_fund_categories),

    path('admin_add_fund_schemes/', views.admin_add_fund_schemes),
    path('admin_add_fund_schemes_post/', views.admin_add_fund_schemes_post),
    path('admin_view_fund_schemes/', views.admin_view_fund_schemes),

    path('admin_view_fund_requests/<id>', views.admin_view_fund_requests),
    path('admin_approve_fund_requests/<id>', views.admin_approve_fund_requests),
    path('admin_reject_fund_requests/<id>', views.admin_reject_fund_requests),

    path('admin_change_password/', views.admin_change_password),
    path('admin_change_password_post/', views.admin_change_password_post),

    path('complaint_reply/<int:id>', views.complaint_reply),
    path('complaint_reply_post/', views.complaint_reply_post),
    path('admin_view_complaints/', views.admin_view_complaints),
    path('admin_view_complaints_search/', views.admin_view_complaints_search),

    path('view_user/', views.view_user),
    path('search_user/', views.search_user),


    path('signup/', views.signup),
    path('signup_post/', views.signup_post),

    path('user_home/', views.user_home),

    path('view_user_profile/', views.view_user_profile),
    path('view_edit_profile/', views.edit_profile),
    path('view_edit_profile_post/', views.editprofilepost),

    path('user_change_password/', views.change_password),
    path('user_password_post/', views.change_password_post),

    path('sent_complaint/', views.sent_complaint),
    path('sent_complaint_post/', views.sent_complaint_post),
    path('user_view_reply/', views.user_view_reply),
    path('user_view_replysearch/', views.user_view_replysearch),

    path('user_view_fund_schemes/', views.user_view_fund_schemes),
    path('user_send_fund_request/<id>', views.user_send_fund_request),
    path('user_send_fund_request_post/', views.user_send_fund_request_post),
    path('user_view_fund_requests/', views.user_view_fund_requests),
    path('user_view_approved_fund_requests/', views.user_view_approved_fund_requests),

    path('get_transaction_history/', views.get_transaction_history),

    path('logout/',views.logout)


]