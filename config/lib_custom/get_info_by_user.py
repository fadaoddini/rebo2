from catalogue.models import Product
import datetime

from config.lib_custom.utils import CustomPagination
from info.models import Info
from learn.models import Learn
from transaction.models import Transaction


class GetInfoByUser:
    def __int__(self, request):
        self.request = request
        super().__init__()

    @classmethod
    def get_all_info_by_user(cls, request):
        user = request.user
        context = dict()
        context['user_info'] = user
        if user.first_name:
            first_name = user.first_name
        else:
            first_name = "دوست"

        if user.last_name:
            last_name = user.last_name
        else:
            last_name = "گرامی"

        context['first_name'] = first_name
        context['last_name'] = last_name

        if user.image == "":
            context['image'] = "https://rebo.ir/static/web/assets/img/profile/profile2.jpg"
        else:
            context['image'] = user.image.url

        products = Product.objects.filter(sell_buy=1).filter(user=user).filter(
            expire_time__gt=datetime.datetime.now()).order_by('price')
        context['products'] = products
        context['product_count'] = products.count()
        new_context = CustomPagination.create_paginator(products, 8, 3, context, request)
        context['paginator'] = new_context['paginator']
        context['page_obj'] = new_context['page_obj']
        context['limit_number'] = new_context['limit_number']
        context['num_pages'] = new_context['num_pages']

        requests = Product.objects.filter(user=user).filter(sell_buy=2).order_by('price')
        context['requests'] = requests
        context['count_request'] = requests.count()
        new_context_request = CustomPagination.create_paginator(requests, 8, 3, context, request)
        context['paginator_request'] = new_context_request['paginator']
        context['page_obj_request'] = new_context_request['page_obj']
        context['limit_number_request'] = new_context_request['limit_number']
        context['num_pages_request'] = new_context_request['num_pages']

        learns = Learn.objects.filter(user=user)
        count_learning = learns.count()
        context['learns'] = learns
        context['count_learning'] = count_learning
        new_context_learn = CustomPagination.create_paginator(learns, 8, 3, context, request)
        context['paginator_learn'] = new_context_learn['paginator']
        context['page_obj_learn'] = new_context_learn['page_obj']
        context['limit_number_learn'] = new_context_learn['limit_number']
        context['num_pages_learn'] = new_context_learn['num_pages']

        user_wallet = Transaction.get_report_by_user(user.pk)
        list_wallet = Transaction.get_list_transaction_by_user(user.pk)
        context['balance'] = user_wallet['balance']
        context['transaction_count'] = user_wallet['transaction_count']
        context['transaction_list'] = list_wallet
        new_context_wallet = CustomPagination.create_paginator(list_wallet, 8, 3, context, request)
        context['paginator_wallet'] = new_context_wallet['paginator']
        context['page_obj_wallet'] = new_context_wallet['page_obj']

        context['limit_number_wallet'] = new_context_wallet['limit_number']
        context['num_pages_wallet'] = new_context_wallet['num_pages']
        context['okmeli'] = False
        context['okbank'] = False

        information = Info.objects.filter(user=user).first()
        if information:
            context['info'] = information
            if information.image_codemeli == "":
                context['image_codemeli'] = "https://rebo.ir/static/web/assets/images/cardmeli.jpg"
                context['okmeli'] = False
            else:
                context['image_codemeli'] = information.image_codemeli.url
                context['okmeli'] = information.okmeli
            if information.image_shaba == "":
                context['image_shaba'] = "https://rebo.ir/static/web/assets/images/cardbanki.jpg"
                context['okbank'] = False
            else:
                context['image_shaba'] = information.image_shaba.url
                context['okbank'] = information.okbank
        else:
            context['image_codemeli'] = "https://rebo.ir/static/web/assets/images/cardmeli.jpg"
            context['image_shaba'] = "https://rebo.ir/static/web/assets/images/cardbanki.jpg"

        return context


