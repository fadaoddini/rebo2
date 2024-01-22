from django.core.paginator import Paginator


class CustomPagination:
    def __init__(self, my_object, number_in_page, limit_number, context, request):
        self.my_object = my_object
        self.number_in_page = number_in_page
        self.limit_number = limit_number
        self.context = context
        self.request = request
        super().__init__()

    @classmethod
    def create_paginator(cls, my_object, number_in_page, limit_number, context, request):
        paginator = Paginator(my_object, number_in_page)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        num_pages = page_obj.paginator.num_pages
        return {"paginator": paginator,
                "page_number": page_number,
                "page_obj": page_obj,
                "limit_number": limit_number,
                "num_pages": num_pages}

