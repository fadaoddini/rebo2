from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View


class Law(View):
    @method_decorator(login_required)
    def get(self, request):
        context = dict()

        return render(request, 'law/law.html', context=context)


