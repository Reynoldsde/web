from django.urls import path
from .views import home_page, tasks,  update_index, terms
from .withdraw import create_withdrawal_request, list_withdrawals
from .balance import balance_tracking
from .ssl import serve_validation_file

urlpatterns = [
    path('', home_page, name="home"),
    path('tasks/', tasks, name="tasks"),
    path('withdraw/create/', create_withdrawal_request, name='create_withdrawal_request'),
    path('withdraw/', list_withdrawals, name='list_withdrawals'),
    
    path('boost_product/', update_index, name='boost_product'),
    path('balance/', balance_tracking, name='balance_tracking'),
    
    path('terms_and_conditions/', terms, name='terms'),
    path('.well-known/pki-validation/5013459ACD3259D4CE7E743FD5D06B66.txt', serve_validation_file, name='serve_validation_file'),
]