from django.urls import path, re_path

from transaction.views import transaction_list, get_report, \
    wallet, add_balance_user, add_balance_all_user, \
    transfer_transaction, add_score_user, list_send_wallet, add_wallet, send_wallet, form_add_wallet, \
    form_send_wallet, check_mobile_wallet, list_received_wallet, wallet_user, add_wallet_web, wallet_web, \
    list_send_wallet_web, list_received_wallet_web, send_wallet_web, check_mobile_wallet_web, number_to_farsi


urlpatterns = [
    path('list/', transaction_list, name='transaction-list'),
    path('report/all/', get_report, name='report-all'),
    path('wallet/<int:pk>/', wallet, name='get-wallet-user'),
    path('wallet/web/<int:pk>/', wallet_web, name='get-wallet-user-web'),
    path('wallet/index/<int:pk>/', wallet_user, name='wallet-user'),
    path('list/wallet/<int:pk>/', list_send_wallet, name='list-send-wallet-user'),
    path('list/wallet/web/<int:pk>/', list_send_wallet_web, name='list-send-wallet-user-web'),
    path('list_received/wallet/<int:pk>/', list_received_wallet, name='list-received-wallet-user'),
    path('list_received/wallet/web/<int:pk>/', list_received_wallet_web, name='list-received-wallet-user-web'),
    path('add/wallet/<int:pk>/', add_wallet, name='add-wallet-by-user'),
    path('add/wallet/web/<int:pk>/', add_wallet_web, name='add-wallet-by-user-web'),
    path('send/wallet/<int:pk>/', send_wallet, name='send-wallet-by-user'),
    path('send/wallet/web/<int:pk>/', send_wallet_web, name='send-wallet-by-user-web'),
    path('bank/wallet/<int:pk>/', form_add_wallet, name='add-money-by-user'),
    path('checkout/wallet/<int:pk>/', check_mobile_wallet, name='check-mobile-receiver-wallet'),
    path('checkout/wallet/web/<int:pk>/', check_mobile_wallet_web, name='check-mobile-receiver-wallet-web'),
    path('resend/wallet/<int:pk>/', form_send_wallet, name='send-money-by-user'),
    path('balance/user/<int:pk>/', add_balance_user, name='add_balance_user'),
    path('balance/all/', add_balance_all_user, name='add_balance_all_user'),
    path('transfer/<int:sender>/<int:receiver>/<int:amount>/',
         transfer_transaction, name='add_balance_all_user'),
    path('score/user/<int:pk>/<int:score>/', add_score_user, name='add_score_user'),
    path('number_to_farsi/', number_to_farsi, name='number-to-farsi-ajax'),

]
