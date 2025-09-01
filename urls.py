from django.urls import path
from .views import invitation_codes, create_invitation_code, delete_invitation_code
from .clients import client_list, delete_client, view_client, edit_client
from .widthraw import withdrawal_request_list, delete_withdrawal_request, edit_withdrawal_request
from .chat import chat, conversation_list_json, check_new_messages
from .vip_plans import vip_plan_list, edit_vip_plan, create_vip_plan, delete_vip_plan
from .customer_service import customer_service
from .clients import reset_premium_client
from .terms_and_conditions import edit_terms

urlpatterns = [
    path("codes", invitation_codes, name="invitaion code"),
    path('create-invitation-code/', create_invitation_code, name='create_invitation_code'),
    path('invitation-codes/delete/<int:pk>/', delete_invitation_code, name='delete_invitation_code'),

    path('clients/', client_list, name='client_list'),
    path('clients/delete/<int:pk>/', delete_client, name='delete_client'),
    path('clients/view/<int:pk>/', view_client, name='view_client'),
    path('clients/<int:pk>/edit/', edit_client, name='edit_client'),

    path('withdrawal-requests/', withdrawal_request_list, name='withdrawal_request_list'),
    path('withdrawal-requests/edit/<int:pk>/', edit_withdrawal_request, name='edit_request'),
    path('withdrawal-requests/delete/<int:pk>/', delete_withdrawal_request, name='withdraw_delete'),
    
    path('chat/', chat, name='chat'),
    path('conversations/', conversation_list_json, name='conversation-list'),
    path('check_new_messages/', check_new_messages, name='check_new_messages'),

    path('vip-plans/', vip_plan_list, name='vip_plan_list'),
    path('vip-plans/new/', create_vip_plan, name='create_vip_plan'),
    path('vip-plans/edit/<int:pk>/', edit_vip_plan, name='edit_vip_plan'),
    path('vip-plans/delete/<int:pk>/', delete_vip_plan, name='delete_vip_plan'),
    
    path('customer_service/', customer_service, name='customer_service'),
    
    path('reset_premium_client/', reset_premium_client, name='reset_premium_client'),
    
    path('edit_terms/', edit_terms, name='edit_terms'),
]