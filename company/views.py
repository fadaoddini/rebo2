from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from company import forms
from company.forms import LocationForm, StaffForm
from company.models import Warehouse, CustomerBalance, TransferWarehouse, Company, Location, Staff
from company.utils import check_is_location, check_is_staff
from hoghoogh.models import Amar, SettingHoghoogh, Sarparasti, Tolid, Hoghoogh, HoghooghArchive


def customer_list(request):
    return HttpResponse("customer list")


def get_report(request):
    customers = Warehouse.get_report()

    for customer in customers:
        context = ''.join(f"balance is : {customer.balance} - and num transaction is : {customer.transfer_count}")

    return HttpResponse(context)


def get_report_by_customer(request, pk):
    customer = Warehouse.get_report_by_customer(pk)
    context = ''.join(f"balance is : {customer['balance']} - and num transaction is : {customer['transaction_count']}")

    return HttpResponse(context)


def add_balance_customer(request, pk, typedate):
    result = CustomerBalance.record_customer_by_id_balance(pk, typedate)

    return HttpResponse(f"add balance by user : {pk} -- {typedate} -- {result} ")


@login_required()
@require_http_methods(request_method_list=['GET'])
@user_passes_test(lambda u: u.is_active)
def add_balance_all_customer(request):
    CustomerBalance.record_all_customer_balance()
    return HttpResponse(f"record all customer balance result")


def transfer_transaction(request, sender, receiver, typedate, quantity, driver):
    instance = TransferWarehouse.transfer(sender, receiver, typedate, quantity, driver)
    return HttpResponse(f"{instance}")


@login_required
@require_http_methods(request_method_list=['POST'])
def create_company(request):
    form = forms.CompanyForm(request.POST, request.FILES)

    if form.is_valid():
        information = form.save(commit=False)
        information.user = request.user
        information.is_active = False
        information.save()
        return HttpResponseRedirect(reverse_lazy('index'))

    messages.error(request, "اطلاعات ارسال شده توسط شما مطابق انتظار ما نبود! لطفا مجددا تلاش نمائید")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
def location_list(request):
    context = dict()
    company = Company.objects.filter(user=request.user).first()
    context['locations'] = Location.objects.filter(company=company)
    form_location = LocationForm()
    context['form_location'] = form_location
    return render(request, 'location/listlocation.html', context=context)


@login_required
def add_location(request):
    company = Company.objects.filter(user=request.user).first()
    form = forms.LocationForm(request.POST)
    if form.is_valid():
        location = form.save(commit=False)
        location.company = company
        location.save()
        return HttpResponseRedirect(reverse_lazy('location-list'))

    messages.error(request, "اطلاعات ارسال شده توسط شما مطابق انتظار ما نبود! لطفا مجددا تلاش نمائید")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
def staff_list(request, pk):
    context = dict()
    has_location = Location.objects.filter(company=request.user.company)
    if check_is_location(has_location, pk):
        location = Location.objects.filter(pk=pk).first()
        context['location'] = location
        staff_info = Staff.objects.filter(location=location)
        context['staffs'] = staff_info

        return render(request, 'staff/liststaff.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
def create_staff(request, pk):
    context = dict()
    has_location = Location.objects.filter(company=request.user.company)
    if check_is_location(has_location, pk):
        location = Location.objects.filter(pk=pk).first()
        context['location'] = location
        context['pk'] = pk
        form_staff = StaffForm()
        context['form_staff'] = form_staff
        return render(request, 'staff/addstaff.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
def edit_staff(request, pk):
    context = dict()
    has_staff = Location.objects.filter(company=request.user.company)
    if check_is_staff(has_staff, pk):
        staff_choose = Staff.objects.filter(pk=pk).first()
        context['staff_choose'] = staff_choose
        context['location'] = staff_choose.location
        form_staff = StaffForm(instance=staff_choose)
        context['form_staff'] = form_staff
        settinghoghoogh = SettingHoghoogh.objects.filter(location=staff_choose.location).first()
        tarikh = settinghoghoogh.start_end_hoghoogh.split('/')
        year = int(tarikh[0])
        month = int(tarikh[1])
        update_sarparast_check_role(request, year, month, staff_choose)
        edit_amar_after_change_role(request, staff_choose.pk)
        return render(request, 'staff/editstaff.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required()
def update_sarparast_check_role(request, year, month, staff):
    sarparasti = Sarparasti.objects.filter(year=year).filter(month=month).filter(staff_id=staff.pk)
    if sarparasti:
        oldsarparasti = sarparasti.first()
        oldsarparasti.role = staff.role
        oldsarparasti.save()


@login_required()
def edit_amar_after_change_role(request, pk):
    staff = Staff.objects.filter(pk=pk).first()
    location = staff.location
    return HttpResponseRedirect(reverse_lazy('staff-list', kwargs={'pk': location.pk}))


@login_required
def add_staff(request, pk):
    has_location = Location.objects.filter(company=request.user.company)
    if check_is_location(has_location, pk):
        location = Location.objects.filter(pk=pk).first()
        form = forms.StaffForm(request.POST)
        if form.is_valid():
            staff1 = form.save(commit=False)
            staff1.location = location
            staff1.save()
            messages.info(request, "نیروی جدید با موفقیت ثبت شد")
            return HttpResponseRedirect(reverse_lazy('add-staff', kwargs={'pk': pk}))

        return HttpResponseRedirect(reverse_lazy('staff-list', kwargs={'pk': location.pk}))
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
def update_staff(request, pk):
    has_staff = Location.objects.filter(company=request.user.company)
    if check_is_staff(has_staff, pk):
        staff_u = Staff.objects.filter(pk=pk).first()
        pk_location = staff_u.location.pk
        form = forms.StaffForm(request.POST, instance=staff_u)
        if form.is_valid():
            form.save()
            messages.info(request, f"{staff_u.name} {staff_u.family} با موفقیت ویرایش شد ")
            return HttpResponseRedirect(reverse_lazy('staff-list', kwargs={'pk': pk_location}))

        messages.error(request, "اطلاعات ارسال شده توسط شما مطابق انتظار ما نبود! لطفا مجددا تلاش نمائید")
        return HttpResponseRedirect(reverse_lazy('staff-list', kwargs={'pk': pk_location}))
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
def delete_staff(request, pk):
    has_staff = Location.objects.filter(company=request.user.company)
    if check_is_staff(has_staff, pk):
        staff_u = Staff.objects.filter(pk=pk).first()
        pk_location = staff_u.location.pk
        staff_u.delete()
        messages.info(request, f"{staff_u.name} {staff_u.family} با موفقیت حذف شد ")
        return HttpResponseRedirect(reverse_lazy('staff-list', kwargs={'pk': pk_location}))
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
def archive_all_hoghoogh(request, pk):
    context = dict()
    has_location = Location.objects.filter(company=request.user.company)
    if check_is_location(has_location, pk):
        hoghooghs = Hoghoogh.objects.filter(location_id=pk)
        sum_pay_all = hoghooghs.aggregate(sum_pay_all=Sum(F('total_pay')))
        context['hoghooghs'] = hoghooghs
        context['sum_pay_all'] = sum_pay_all['sum_pay_all']
        return render(request, 'location/archive_hoghoogh.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))


@login_required
def archive_all_hoghoogh_all(request, pk):
    context = dict()
    has_location = Location.objects.filter(company=request.user.company)
    if check_is_location(has_location, pk):
        hoghooghs = HoghooghArchive.objects.filter(location_id=pk)
        sum_pay_all = hoghooghs.aggregate(sum_pay_all=Sum(F('total_pay')))
        context['hoghooghs'] = hoghooghs
        context['sum_pay_all'] = sum_pay_all['sum_pay_all']
        return render(request, 'location/archive_hoghoogh.html', context=context)
    messages.error(request, "شما مرتکب تقلب شده اید، مراقب باشید امتیازات منفی ممکن است حساب کاربری شما را مسدود کند!")
    return HttpResponseRedirect(reverse_lazy('index'))



