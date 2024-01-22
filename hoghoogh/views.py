from collections import Counter

import jdatetime
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import Sum, F, Q
from django.db.models.functions import Coalesce
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from company.models import Company, Location, Staff
from hoghoogh import forms
from hoghoogh.forms import SettingHoghooghForm, ListPriceForm, ListAmarForm, HoghooghFormFirst
from hoghoogh.models import SettingHoghoogh, ListPrice, Amar, Hoghoogh, Sarparasti, Tolid, AmarArchive, HoghooghArchive
from hoghoogh.serializers import AmarSerializer
from hoghoogh.utils import check_is_active, check_is_ok, check_is_location, check_is_staff, check_is_staff_by_staff_pk


def hoghoogh_list(request):
    return HttpResponse("hoghoogh list")


@login_required
@user_passes_test(check_is_active)
def setting_hoghoogh(request):
    context = dict()
    company = Company.objects.filter(user=request.user).first()
    context['locations'] = Location.objects.filter(company=company)
    return render(request, 'hoghoogh/setting.html', context=context)


@login_required
@user_passes_test(check_is_active)
def update_setting_hoghoogh(request, pk):
    context = dict()
    has_location = Location.objects.filter(company=request.user.company)
    if check_is_location(has_location, pk):
        location = Location.objects.filter(pk=pk).first()
        setting_hoghoogh1 = SettingHoghoogh.objects.filter(location=location)
        context['setting_hoghoogh1'] = "NO"
        form_setting_hoghoogh = SettingHoghooghForm()
        if setting_hoghoogh1:
            setting_hoghoogh1 = setting_hoghoogh1.first()
            context['setting_hoghoogh1'] = setting_hoghoogh1
            form_setting_hoghoogh = SettingHoghooghForm(instance=setting_hoghoogh1)

        context['location'] = location
        context['pk'] = pk

        context['form_setting_hoghoogh'] = form_setting_hoghoogh
        return render(request, 'hoghoogh/update_setting.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))

@login_required
@user_passes_test(check_is_active)
@require_http_methods(request_method_list=['POST'])
def update_setting_hoghoogh_send(request, pk):
    has_location = Location.objects.filter(company=request.user.company)
    if check_is_location(has_location, pk):
        location = Location.objects.filter(pk=pk).first()
        form = forms.SettingHoghooghForm(request.POST)
        if form.is_valid():
            setting_hoghooghi = form.save(commit=False)
            setting_hoghooghi.location = location
            setting_hoghooghi.save()
            messages.info(request, "اطلاعات با موفقیت ثبت شد")
            return HttpResponseRedirect(reverse_lazy('setting-hoghoogh'))

        messages.error(request, "اطلاعات ارسال شده توسط شما مطابق انتظار ما نبود! لطفا مجددا تلاش نمائید")
        return HttpResponseRedirect(reverse_lazy('index'))
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))

@login_required
@user_passes_test(check_is_active)
@require_http_methods(request_method_list=['POST'])
def update_setting_hoghoogh_edit(request, pk):
    has_location = Location.objects.filter(company=request.user.company)
    if check_is_location(has_location, pk):
        location = Location.objects.filter(pk=pk).first()
        setting_hoghoogh1 = SettingHoghoogh.objects.filter(location=location).first()
        form = forms.SettingHoghooghForm(request.POST, instance=setting_hoghoogh1)
        if form.is_valid():
            form.save()
            messages.info(request, "اطلاعات با موفقیت ویرایش شد")
            return HttpResponseRedirect(reverse_lazy('setting-hoghoogh'))

        messages.error(request, "اطلاعات ارسال شده توسط شما مطابق انتظار ما نبود! لطفا مجددا تلاش نمائید")
        return HttpResponseRedirect(reverse_lazy('index'))
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))

@login_required
@user_passes_test(check_is_active)
def listprice(request, pk):
    context = dict()
    has_location = Location.objects.filter(company=request.user.company)
    if check_is_location(has_location, pk):
        location = Location.objects.filter(pk=pk).first()
        context['pk'] = pk
        context['location'] = location
        context['listprices'] = ListPrice.objects.filter(location=location)
        form_listprice = ListPriceForm()
        context['form_listprice'] = form_listprice
        return render(request, 'hoghoogh/listprice.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))

@login_required
@user_passes_test(check_is_active)
def add_listprice(request, pk):
    has_location = Location.objects.filter(company=request.user.company)
    if check_is_location(has_location, pk):
        location = Location.objects.filter(pk=pk).first()
        form = forms.ListPriceForm(request.POST)
        if form.is_valid():
            listprice1 = form.save(commit=False)
            listprice1.location = location
            listprice1.is_active = True
            listprice1.save()
            messages.info(request, "اطلاعات با موفقیت ثبت شد")
            return HttpResponseRedirect(reverse_lazy('listprice', kwargs={'pk': pk}))

        messages.error(request, "اطلاعات ارسال شده توسط شما مطابق انتظار ما نبود! لطفا مجددا تلاش نمائید")
        return HttpResponseRedirect(reverse_lazy('listprice', kwargs={'pk': pk}))
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
@user_passes_test(check_is_active)
def amar(request, pk):
    context = dict()
    list_price = ListPrice.objects.filter(is_active=True)

    context['list_price'] = list_price
    context['num_list_price'] = len(list_price)
    staff_choose = Staff.objects.filter(pk=pk).first()
    context['staff_choose'] = staff_choose
    context['location'] = staff_choose.location
    settinghoghoogh = SettingHoghoogh.objects.filter(location=staff_choose.location).first()
    num_day = settinghoghoogh.num_day
    tarikh = settinghoghoogh.start_end_hoghoogh.split('/')
    year = int(tarikh[0])
    context['year'] = year
    month = int(tarikh[1])
    context['month'] = month
    day = int(tarikh[2])
    context['day'] = day
    finish_tarikh = 32
    if num_day + day > finish_tarikh:
        range_days = range(day, finish_tarikh)
    else:
        range_days = range(day, num_day + day)
    context['time_range'] = range_days
    # CREATE TIME FOR CALCULATE NUM DAY LATER ----->>> shamsi to miladi
    # tarikh_choose_en = jdatetime.date(year=year, month=month, day=day).togregorian()
    # new_tarikh_split = str(tarikh_choose_en).split('-')
    # new_year = int(new_tarikh_split[0])
    # new_month = int(new_tarikh_split[1])
    # new_day = int(new_tarikh_split[2])
    # new_tarikh_shamsi = jdatetime.date.fromgregorian(year=new_year, month=new_month, day=new_day)
    context['settinghoghoogh'] = settinghoghoogh
    amarexist = Amar.objects.filter(staff_id=pk).select_related('listprice').all().order_by('tarikh')

    # amarexist = Amar.objects.filter(staff_id=pk)

    hoghooghexist = Hoghoogh.objects.filter(staff_id=staff_choose.pk)
    if hoghooghexist:
        hoghooghexist = hoghooghexist.first()
        form_hoghoogh_first = HoghooghFormFirst(instance=hoghooghexist)
    else:
        form_hoghoogh_first = HoghooghFormFirst()
    context['form_hoghoogh_first'] = form_hoghoogh_first

    if amarexist:

        context['amarexist'] = amarexist
        form_amar = ListAmarForm()
        context['form_amar'] = form_amar

    else:

        form_amar = ListAmarForm()
        context['form_amar'] = form_amar

    return render(request, 'hoghoogh/amar.html', context=context)


@login_required
@user_passes_test(check_is_active)
def edit_amar(request, pk):

    staff = Staff.objects.filter(pk=pk).first()
    with transaction.atomic():
        add_hoghogh_first(request, staff.pk)
        tedad_day_by_staff = Hoghoogh.calculate_day_by_staff(staff)
        if tedad_day_by_staff == 0:
            messages.error(request, "محاسبه روز غیر ممکن است!")
            return HttpResponseRedirect(reverse_lazy('staff-list', kwargs={'pk': staff.location.pk}))
        year_month = get_year_month(request, staff)
        year = year_month[0]
        month = year_month[1]
        location = staff.location
        list_amar = request.POST
        for item in list_amar:
            if not item == "csrfmiddlewaretoken":
                editamar = Amar.objects.filter(pk=item)
                if editamar:
                    editamar = editamar.first()
                    newname = str(item)
                    tedad_new = request.POST.get(newname)

                    editamar.tedad = tedad_new
                    editamar.save()
        if staff.role == 3:
            Sarparasti.update_sarparastha(tedad_day_by_staff, year, month, staff)
            # sum_tolid(request, year, month, staff)
            instance = Tolid.calculate_tolid_all(year, month, staff)
        else:
            update_sarparast_check_role(request, year, month, staff)
            # sum_tolid(request, year, month, staff)
            instance = Tolid.calculate_tolid_all(year, month, staff)
        messages.info(request, "اطلاعات با موفقیت ویرایش شد")

    return HttpResponseRedirect(reverse_lazy('staff-list', kwargs={'pk': location.pk}))


@login_required
@user_passes_test(check_is_active)
def add_amar(request, pk):
    staff = Staff.objects.filter(pk=pk).first()
    if staff.role == 3:
        is_sarparast = True
    else:
        is_sarparast = False
    location = staff.location
    list_prices = ListPrice.objects.filter(is_active=True, location_id=location.pk)
    settinghoghoogh = SettingHoghoogh.objects.filter(location_id=location.pk).first()
    num_day = settinghoghoogh.num_day
    tarikh = settinghoghoogh.start_end_hoghoogh.split('/')
    year = int(tarikh[0])
    month = int(tarikh[1])
    day = int(tarikh[2])
    finish_tarikh = 32
    if num_day + day > finish_tarikh:
        range_days = range(day, finish_tarikh)
    else:
        range_days = range(day, num_day + day)
    day_active = range_days
    test = request.POST
    year = test['year']
    month = test['month']
    year_month =year+month

    with transaction.atomic():
        for list_price in list_prices:
            num_list = list_price.pk
            new_price = list_price.price
            vlu = list_price.value_type
            if vlu == 1:
                new_type = "dates"
            else:
                new_type = "etc"

            newname = "name["+str(num_list)+"]"
            idlistprice = num_list

            for day in day_active:
                new_tedad = "tedad["+str(day)+"]["+str(num_list)+"]"
                if day < 10:
                    tarikh = str(year)+"/"+str(month)+"/0"+str(day)
                else:
                    tarikh = str(year) + "/" + str(month) + "/" + str(day)

                if test[new_tedad] != "0":
                    name = test[newname]
                    price = new_price
                    type = new_type
                    tedad = test[new_tedad]
                    tarikh = tarikh
                    createform = Amar(name=name, price=price, tedad=tedad, type=type, tarikh=tarikh, staff_id=staff.pk,
                                      listprice_id=idlistprice, is_sarparast=is_sarparast, location=location)
                    createform.save()
        add_hoghogh_first(request, staff.pk)
        tedad_day_by_staff = Hoghoogh.calculate_day_by_staff(staff)
        if tedad_day_by_staff == 0:
            messages.error(request, "محاسبه روز غیر ممکن است!")
            return HttpResponseRedirect(reverse_lazy('staff-list', kwargs={'pk': staff.location.pk}))

        if staff.role == 3:
            Sarparasti.update_sarparastha(tedad_day_by_staff, year, month, staff)
            # sum_tolid(request, year, month, staff)
            Tolid.calculate_tolid_all(year, month, staff)
        else:
            update_sarparast_check_role(request, year, month, staff)
            # sum_tolid(request, year, month, staff)
            Tolid.calculate_tolid_all(year, month, staff)
        messages.info(request, "اطلاعات با موفقیت ثبت شد")

    return HttpResponseRedirect(reverse_lazy('staff-list', kwargs={'pk': location.pk}))


@login_required()
@user_passes_test(check_is_active)
def delete_item_amar(request, pk):
    item_amar = Amar.objects.filter(pk=pk).first()
    staff_id = item_amar.staff_id
    tarikh = item_amar.tarikh
    tarikh1 = tarikh.split("/")
    year = tarikh1[0]
    month = tarikh1[1]
    item_amar.delete()
    staff = Staff.objects.filter(pk=staff_id).first()
    tedad_day_by_staff = Hoghoogh.calculate_day_by_staff(staff)
    if tedad_day_by_staff == 0:
        messages.error(request, "محاسبه روز غیر ممکن است!")
        return HttpResponseRedirect(reverse_lazy('staff-list', kwargs={'pk': staff.location.pk}))

    Tolid.calculate_tolid_all(year, month, staff)
    Sarparasti.update_sarparastha(tedad_day_by_staff, year, month, staff)
    messages.error(request, "اطلاعات با موفقیت حذف شد")
    return HttpResponseRedirect(reverse_lazy('amar', kwargs={'pk': staff_id}))


@login_required()
@user_passes_test(check_is_active)
def delete_all_item_amar_by_staff(request, pk):

    staff = Staff.objects.filter(pk=pk).first()
    item_amar = Amar.objects.filter(staff_id=pk)
    for item in item_amar:
        tarikh = item.tarikh
        tarikh1 = tarikh.split("/")
        year = tarikh1[0]
        month = tarikh1[1]
        item.delete()
        tedad_day_by_staff = Hoghoogh.calculate_day_by_staff(staff)
        Tolid.calculate_tolid_all(year, month, staff)
        Sarparasti.update_sarparastha(tedad_day_by_staff, year, month, staff)
    # item_amar.delete()
    messages.error(request, "کلیه اطلاعات مربوطه با موفقیت حذف شد")
    return HttpResponseRedirect(reverse_lazy('amar', kwargs={'pk': pk}))


@login_required()
@user_passes_test(check_is_active)
def check_hoghoogh_table(request, staff):
    hoghooghexist = Hoghoogh.objects.filter(staff_id=staff.pk)
    if hoghooghexist:
        pass
    else:
        pass


@login_required()
@user_passes_test(check_is_active)
def get_year_month(request, staff):
    year_month = []
    settinghoghoogh = SettingHoghoogh.objects.filter(location=staff.location).first()
    num_day = settinghoghoogh.num_day
    tarikh = settinghoghoogh.start_end_hoghoogh.split('/')
    year = str(tarikh[0])
    month = str(tarikh[1])
    year_month.append(year)
    year_month.append(month)
    return year_month


@login_required()
@user_passes_test(check_is_active)
def taeed_all_hoghoogh(request, pk):
    context = dict()
    has_location = Location.objects.filter(company=request.user.company)
    if check_is_location(has_location, pk):
        location = Location.objects.filter(pk=pk).first()
        context['location'] = location
        staff_info = Staff.objects.filter(location=location)
        settinghoghoogh = SettingHoghoogh.objects.filter(location=pk).first()
        num_day = settinghoghoogh.num_day
        tarikh = settinghoghoogh.start_end_hoghoogh.split('/')
        year = int(tarikh[0])
        month = int(tarikh[1])

        list_hoghoogh = Hoghoogh.objects.filter(year=year, month=month, location_id=pk)
        if list_hoghoogh:
            texti = " کلیه حقوق ماه " + str(month) + " در سال " + str(year) + " بروزرسانی گردید "
            messages.info(request, texti)
            for taeed in list_hoghoogh:
                result = all_accept_hoghoogh(request, taeed.staff_id, location.pk)
                taeed.sum_calculate = result[0]
                taeed.sum_all = result[1]
                taeed.days = result[2]
                taeed.bime = result[3]
                taeed.karaee = result[4]
                taeed.amar = result[5]
                taeed.pele_price = result[6]
                taeed.sarparasti = result[7]
                taeed.total_pay = result[8]
                taeed.save()
        else:
            texti = "هنوز اطلاعاتی برای بروزرسانی وجود ندارد!"
            messages.error(request, texti)
        return HttpResponseRedirect(reverse_lazy('staff-list', kwargs={'pk': location.pk}))
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required()
@user_passes_test(check_is_active)
def checklist_staff_amar(request, pk):
    context = dict()
    g = 0
    staff = Staff.objects.filter(pk=pk).first()
    location = staff.location
    fix_salary = staff.fix_salary
    context['staff'] = staff
    context['location'] = location
    settinghoghoogh = SettingHoghoogh.objects.filter(location=staff.location).first()
    context['settinghoghoogh'] = settinghoghoogh
    tarikh3 = settinghoghoogh.start_end_hoghoogh.split('/')
    year3 = int(tarikh3[0])

    month3 = int(tarikh3[1])

    hoghooghexist = Hoghoogh.objects.filter(staff_id=staff.pk, year=year3, month=month3)

    if hoghooghexist:
        hoghoogh = hoghooghexist.first()
        context['hoghoogh'] = hoghoogh
        amar = Amar.objects.filter(staff_id=pk).select_related('listprice').all().order_by('tarikh')
        if Q(amar.exists()) | Q(fix_salary > 0):
            context['sarparasti'] = 0
            context['day_sarparasti'] = 0
            context['one_sarparasti_price'] = 0
            year = hoghoogh.year
            context['year'] = year
            month = hoghoogh.month
            context['month'] = month
            mosaede = hoghoogh.mosaede
            tashvighi = hoghoogh.tashvighi
            vam = hoghoogh.vam
            context['mosaede'] = mosaede
            context['tashvighi'] = tashvighi
            context['vam'] = vam
            context['bime_day'] = settinghoghoogh.price_bime_in_day
            if fix_salary > 0:
                context['sumamar'] = 0
                context['sumitemprice'] = 0
                context['amar'] = {}
                context['day_ok'] = 26
                context['fix_salary_staff'] = fix_salary
                context['darsad_pele'] = 0
                context['price_darsad_pele'] = 0
                check_bime = staff.insurance
                check_bime_status = staff.insurance_status
                if check_bime:
                    context['check_bime'] = "دارد"
                    if check_bime_status:
                        price_bime_sum = 26 * settinghoghoogh.price_bime_in_day
                        context['check_bime_status'] = "دارد"
                    else:
                        price_bime_sum = 0
                        context['check_bime_status'] = "ندارد"
                        context['bime_day'] = 0
                else:
                    price_bime_sum = 0
                    context['check_bime'] = "ندارد"
                    context['bime_day'] = 0
                context['price_bime_sum'] = price_bime_sum
                a = fix_salary
                b = price_bime_sum
                c = vam
                d = mosaede
                e = tashvighi
                sum_first = a - b - c - d + e
                context['sum_first'] = sum_first
                context['sum_pay'] = sum_first

                role = staff.role
                if role == 1:
                    print('edari')
                    context['role'] = "ندارد"
                    price_darsad_pele = 0
                elif role == 2:
                    print('kargar')
                    context['role'] = "ندارد"
                else:
                    print('sarparast')
                    context['role'] = "دارد"
                    context['sarparasti'] = 0
                    context['day_sarparasti'] = 0
                    context['one_sarparasti_price'] = 0
                    price_darsad_pele = 0
            else:
                sumamar = amar.aggregate(sum_calculate=Sum(F('price') * F('tedad')))
                context['amar'] = amar
                result_day = []
                for res in amar:
                    result_day.append(res.tarikh)
                day_ok = len(list(set(result_day)))
                context['day_ok'] = day_ok

                fix_salary_staff = staff.fix_salary
                context['fix_salary_staff'] = fix_salary_staff

                context['sumamar'] = sumamar['sum_calculate']+fix_salary_staff
                context['sumitemprice'] = sumamar['sum_calculate']
                pele_one_day = settinghoghoogh.pele_one_day
                pele_two_day = settinghoghoogh.pele_two_day
                pele_three_day = settinghoghoogh.pele_three_day
                pele_one_darsad = settinghoghoogh.pele_one_darsad
                pele_two_darsad = settinghoghoogh.pele_two_darsad
                pele_three_darsad = settinghoghoogh.pele_three_darsad
                if (day_ok <= pele_one_day):
                    darsad_pele = 0
                elif (day_ok > pele_one_day and day_ok <= pele_two_day):
                    darsad_pele = pele_one_darsad
                elif (day_ok > pele_two_day and day_ok <= pele_three_day):
                    darsad_pele = pele_two_darsad
                elif (day_ok > pele_three_day):
                    darsad_pele = pele_three_darsad
                context['darsad_pele'] = darsad_pele
                price_darsad_pele = int(sumamar['sum_calculate']*darsad_pele/100)
                context['price_darsad_pele'] = price_darsad_pele
                check_bime = staff.insurance
                check_bime_status = staff.insurance_status
                if check_bime:
                    context['check_bime'] = "دارد"
                    if check_bime_status:
                        price_bime_sum = day_ok * settinghoghoogh.price_bime_in_day
                        context['check_bime_status'] = "دارد"
                    else:
                        price_bime_sum = day_ok * 0
                        context['check_bime_status'] = "ندارد"
                        context['bime_day'] = 0
                else:
                    price_bime_sum = day_ok * 0
                    context['check_bime'] = "ندارد"
                    context['bime_day'] = 0
                role = staff.role
                if role == 1:
                    print('edari')
                    context['role'] = "ندارد"
                    price_darsad_pele = 0
                elif role == 2:
                    print('kargar')
                    context['role'] = "ندارد"
                elif role == 3:
                    print('sarparast')
                    context['role'] = "دارد"
                    sum_price_sarparast = Sarparasti.calculate_sarparasti(year, month, staff, location.id)
                    context['sarparasti'] = sum_price_sarparast[2]
                    context['day_sarparasti'] = sum_price_sarparast[0]
                    context['one_sarparasti_price'] = sum_price_sarparast[1]
                    price_darsad_pele = 0
                    g = sum_price_sarparast[2]
                    print(g)
                else:
                    print('hichi')
                context['price_bime_sum'] = price_bime_sum
                a = sumamar['sum_calculate'] + fix_salary_staff
                b = price_bime_sum
                c = vam
                d = mosaede
                e = tashvighi
                sum_first = a - b - c - d + e + g
                context['sum_first'] = sum_first
                context['sum_pay'] = sum_first + price_darsad_pele
        else:
            messages.error(request, "هنوز اطلاعاتی بابت حقوق برای ایشان درج نشده است")
            return HttpResponseRedirect(reverse_lazy('staff-list', kwargs={'pk': location.pk}))
    else:
        messages.error(request, "هنوز اطلاعاتی بابت حقوق برای ایشان درج نشده است")
        return HttpResponseRedirect(reverse_lazy('staff-list', kwargs={'pk': location.pk}))
    return render(request, 'hoghoogh/checklist.html', context=context)


@login_required()
@user_passes_test(check_is_active)
def add_hoghogh_first(request, pk):

    staff = Staff.objects.filter(pk=pk).first()
    location_pk = staff.location.pk
    location_exist = Location.objects.filter(pk=location_pk)
    location = location_exist.first()
    hoghooghexist = Hoghoogh.objects.filter(staff_id=staff.pk)
    if hoghooghexist:
        hoghooghexist = hoghooghexist.first()
        form = forms.HoghooghFormFirst(request.POST, instance=hoghooghexist)
    else:
        form = forms.HoghooghFormFirst(request.POST)

    if form.is_valid():
        hoghoogh_first = form.save(commit=False)
        hoghoogh_first.staff = staff
        hoghoogh_first.location = location
        hoghoogh_first.sum_calculate = 0
        hoghoogh_first.sum_all = 0
        hoghoogh_first.days = 0
        hoghoogh_first.bime = 0
        hoghoogh_first.karaee = 0
        hoghoogh_first.pele_price = 0
        hoghoogh_first.sarparasti = 0
        hoghoogh_first.total_pay = 0
        hoghoogh_first.amar = {}
        hoghoogh_first.save()
        messages.info(request, "اطلاعات تکمیلی با موفقیت بروزرسانی شد")
        return HttpResponseRedirect(reverse_lazy('amar', kwargs={'pk': staff.pk}))

    messages.info(request, "اطلاعات تکمیلی بدون تغییر باقی ماند")
    return HttpResponseRedirect(reverse_lazy('amar', kwargs={'pk': staff.pk}))


@login_required()
@user_passes_test(check_is_active)
def update_sarparast_check_role(request, year, month, staff):

    sarparasti = Sarparasti.objects.filter(year=year).filter(month=month).filter(staff_id=staff.pk)
    if sarparasti:
        oldsarparasti = sarparasti.first()
        oldsarparasti.role = staff.role
        oldsarparasti.save()


@login_required()
@user_passes_test(check_is_active)
def all_accept_hoghoogh(request, pk, location_id):
    result = []
    g = 0
    u = 0
    karaee = 0
    am = {}

    staff = Staff.objects.filter(pk=pk).first()
    location = staff.location
    fix_salary = staff.fix_salary
    settinghoghoogh = SettingHoghoogh.objects.filter(location=staff.location).first()
    tarikh3 = settinghoghoogh.start_end_hoghoogh.split('/')
    year3 = int(tarikh3[0])
    month3 = int(tarikh3[1])
    hoghooghexist = Hoghoogh.objects.filter(staff_id=staff.pk, year=year3, month=month3, location_id=location_id)
    if hoghooghexist:
        hoghoogh = hoghooghexist.first()
        amar = Amar.objects.filter(staff_id=pk).select_related('listprice').all().order_by('tarikh')
        serializer = AmarSerializer(amar, many=True)
        am = serializer.data
        if Q(amar.exists()) | Q(fix_salary > 0):
            sarparasti = 0
            day_sarparasti = 0
            one_sarparasti_price = 0
            year = hoghoogh.year
            month = hoghoogh.month
            mosaede = hoghoogh.mosaede
            tashvighi = hoghoogh.tashvighi
            vam = hoghoogh.vam
            bime_day = settinghoghoogh.price_bime_in_day
            if fix_salary > 0:
                sumamar = 0
                sumitemprice = 0
                amar = {}
                day_ok = 26
                darsad_pele = 0
                price_darsad_pele = 0
                check_bime = staff.insurance
                check_bime_status = staff.insurance_status
                if check_bime:
                    if check_bime_status:
                        price_bime_sum = 26 * settinghoghoogh.price_bime_in_day
                    else:
                        price_bime_sum = 0
                        bime_day = 0
                else:
                    price_bime_sum = 0
                    bime_day = 0
                price_bime_sum = price_bime_sum
                a = fix_salary
                b = price_bime_sum
                c = vam
                d = mosaede
                e = tashvighi
                sum_first = a - b - c - d + e
                sum_first = sum_first
                sum_pay = sum_first
                role = staff.role
                if role == 1:
                    print('edari')
                    price_darsad_pele = 0
                elif role == 2:
                    print('kargar')
                else:
                    print('sarparast')
                    sarparasti = 0
                    day_sarparasti = 0
                    one_sarparasti_price = 0
                    price_darsad_pele = 0
            else:
                sumamar = amar.aggregate(sum_calculate=Sum(F('price') * F('tedad')))
                result_day = []
                for res in amar:
                    result_day.append(res.tarikh)
                day_ok = len(list(set(result_day)))
                fix_salary_staff = staff.fix_salary
                sumamar2 = int(sumamar['sum_calculate'])+fix_salary_staff
                pele_one_day = settinghoghoogh.pele_one_day
                pele_two_day = settinghoghoogh.pele_two_day
                pele_three_day = settinghoghoogh.pele_three_day
                pele_one_darsad = settinghoghoogh.pele_one_darsad
                pele_two_darsad = settinghoghoogh.pele_two_darsad
                pele_three_darsad = settinghoghoogh.pele_three_darsad
                if (day_ok <= pele_one_day):
                    darsad_pele = 0
                elif (day_ok > pele_one_day and day_ok <= pele_two_day):
                    darsad_pele = pele_one_darsad
                elif (day_ok > pele_two_day and day_ok <= pele_three_day):
                    darsad_pele = pele_two_darsad
                elif (day_ok > pele_three_day):
                    darsad_pele = pele_three_darsad

                if darsad_pele > 0:
                    price_darsad_pele = int(sumamar['sum_calculate']*darsad_pele/100)
                else:
                    price_darsad_pele = 0

                print(price_darsad_pele)
                check_bime = staff.insurance
                check_bime_status = staff.insurance_status
                if check_bime:
                    if check_bime_status:
                        price_bime_sum = day_ok * settinghoghoogh.price_bime_in_day
                    else:
                        price_bime_sum = day_ok * 0
                        bime_day = 0
                else:
                    price_bime_sum = day_ok * 0
                    bime_day = 0
                role = staff.role
                if role == 1:
                    print('edari')
                    price_darsad_pele = 0
                elif role == 2:
                    print('kargar')
                elif role == 3:
                    print('sarparast')
                    # first check update sarparasti
                    tedad_day_by_staff = Hoghoogh.calculate_day_by_staff(staff)
                    Sarparasti.update_sarparastha(tedad_day_by_staff, year, month, staff)
                    # second calculate sarparasti
                    sum_price_sarparast = Sarparasti.calculate_sarparasti(year, month, staff, location_id)
                    sarparasti = sum_price_sarparast[2]
                    day_sarparasti = sum_price_sarparast[0]
                    one_sarparasti_price = sum_price_sarparast[1]
                    g = sum_price_sarparast[2]
                    price_darsad_pele = 0
                else:
                    print('hichi2')
                u = sumamar['sum_calculate']
                a = sumamar['sum_calculate'] + fix_salary_staff
                b = price_bime_sum
                c = vam
                d = mosaede
                e = tashvighi
                sum_first = a - b - c - d + e + g
                sum_pay = sum_first + price_darsad_pele
                karaee = int(sum_pay / day_ok)
    result.append(u)
    result.append(a)
    result.append(day_ok)
    result.append(b)
    result.append(karaee)
    result.append(am)
    result.append(price_darsad_pele)
    result.append(g)
    result.append(sum_pay)
    return result



@login_required()
@user_passes_test(check_is_active)
def archive_hoghoogh_delete_before(request, pk):
    has_location = Location.objects.filter(company=request.user.company)

    if check_is_location(has_location, pk):
        location = Location.objects.filter(pk=pk).first()
        settinghoghoogh = SettingHoghoogh.objects.filter(location=pk).first()
        tarikh = settinghoghoogh.start_end_hoghoogh.split('/')
        year = int(tarikh[0])
        month = int(tarikh[1])
        # delete all amar inja bayad anjam beshe
        delete_amar_and_archive(request, pk, year, month)
        hoghoogh_archive(request, pk, year, month)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required()
@user_passes_test(check_is_active)
def hoghoogh_archive(request, pk, year, month):
    location = Location.objects.filter(pk=pk).first()
    hoghooghexist = Hoghoogh.objects.filter(location=location, year=year, month=month)
    if hoghooghexist:
        with transaction.atomic():
            for hoghoogh in hoghooghexist:
                staff = hoghoogh.staff
                location = hoghoogh.location
                sum_calculate = hoghoogh.sum_calculate
                sum_all = hoghoogh.sum_all
                days = hoghoogh.days
                pele_price = hoghoogh.pele_price
                total_pay = hoghoogh.total_pay
                sarparasti = hoghoogh.sarparasti
                mosaede = hoghoogh.mosaede
                vam = hoghoogh.vam
                bime = hoghoogh.bime
                tashvighi = hoghoogh.tashvighi
                year = hoghoogh.year
                month = hoghoogh.month
                karaee = hoghoogh.karaee
                amar = hoghoogh.amar
                hoghoogh_archive = HoghooghArchive(staff=staff, sum_calculate=sum_calculate, sum_all=sum_all, days=days,
                                                    pele_price=pele_price, total_pay=total_pay, location=location,
                                                    sarparasti=sarparasti, mosaede=mosaede, vam=vam, bime=bime,
                                                    tashvighi=tashvighi, year=year, month=month, karaee=karaee,
                                                    amar=amar)
                hoghoogh_archive.save()
            hoghooghexist.delete()
            messages.info(request, "لیست حقوق مورد نظر آرشیو شد!")
    else:
        messages.info(request, "متاسفانه لیستی برای آرشیو یافت نشد!")


@login_required()
@user_passes_test(check_is_active)
def delete_amar_and_archive(request, pk, year, month):
    location = Location.objects.filter(pk=pk).first()
    listprices = ListPrice.objects.filter(location_id=pk)
    with transaction.atomic():
        amar_archive_for_delete = AmarArchive.objects.filter(year=year, month=month, location=location)
        amar_archive_for_delete.delete()
        for listprice in listprices:
            name = listprice.name
            price = listprice.price
            amars = Amar.objects.filter(location_id=pk).filter(listprice_id=listprice.id)
            tedad_first = amars.aggregate(sum_tedad=Sum(F('tedad')))
            tedad_second = tedad_first['sum_tedad']
            tedad = Coalesce(tedad_second, 0)
            type = listprice.value_type
            amar_archive = AmarArchive(name=name, price=price, tedad=tedad, type=type,
                                       year=year, month=month, location_id=pk)
            amar_archive.save()
        amar_asli_for_delete = Amar.objects.filter(location_id=pk)
        amar_asli_for_delete.delete()


