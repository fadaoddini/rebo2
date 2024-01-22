from django.db import models
from django.db.models import Sum, Q, Count, F
from django.db.models.functions import Coalesce

from company.models import Location, Staff


class SettingHoghoogh(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    price_bime_in_day = models.IntegerField(default=0)
    start_end_hoghoogh = models.CharField(max_length=32)
    num_day = models.IntegerField(default=31)
    darsad_all = models.IntegerField(default=0)
    darsad_sarparast = models.IntegerField(default=0)
    pele_one_day = models.IntegerField(default=0)
    pele_one_darsad = models.IntegerField(default=0)
    pele_two_day = models.IntegerField(default=0)
    pele_two_darsad = models.IntegerField(default=0)
    pele_three_day = models.IntegerField(default=0)
    pele_three_darsad = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'SettingHoghoogh'
        verbose_name_plural = 'SettingHoghooghs'

    def __str__(self):
        return f"{self.location}"


class ListPrice(models.Model):
    ACTIVE = True
    INACTIVE = False

    STATUS_LISTPRICE = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )

    DATES = 1
    ETC = 2

    VALUE_TYPE_LISTPRICE = (
        (DATES, 'dates'),
        (ETC, 'etc'),
    )
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='listprice')
    name = models.CharField(max_length=42)
    price = models.IntegerField()
    value_type = models.PositiveSmallIntegerField(choices=VALUE_TYPE_LISTPRICE, default=DATES)
    is_active = models.BooleanField(choices=STATUS_LISTPRICE, default=ACTIVE)

    class Meta:
        verbose_name = 'ListPrice'
        verbose_name_plural = 'ListPrices'

    def __str__(self):
        return f"{self.name}"


class Amar(models.Model):
    YES = True
    NO = False
    IS_SARPARAST = (
        (YES, 'yes'),
        (NO, 'no'),
    )
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="amar")
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='amar')
    listprice = models.ForeignKey(ListPrice, on_delete=models.CASCADE, related_name='amarlist')
    name = models.CharField(max_length=42)
    price = models.IntegerField()
    tedad = models.FloatField()
    type = models.CharField(max_length=42)
    is_sarparast = models.BooleanField(choices=IS_SARPARAST, default=YES)
    tarikh = models.CharField(max_length=42)

    class Meta:
        verbose_name = 'Amar'
        verbose_name_plural = 'Amars'

    def __str__(self):
        return f"{self.name}"


class AmarArchive(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="amarlocation")
    name = models.CharField(max_length=42)
    price = models.IntegerField()
    tedad = models.FloatField()
    type = models.CharField(max_length=42)
    year = models.CharField(max_length=10)
    month = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'AmarArchive'
        verbose_name_plural = 'AmarArchives'

    def __str__(self):
        return f"{self.name}"


class Hoghoogh(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="hoghooghs")
    sum_calculate = models.BigIntegerField()
    sum_all = models.BigIntegerField()
    days = models.IntegerField()
    pele_price = models.BigIntegerField(default=0)
    total_pay = models.BigIntegerField(default=0)
    sarparasti = models.BigIntegerField(default=0)
    mosaede = models.BigIntegerField(default=0)
    vam = models.BigIntegerField(default=0)
    bime = models.BigIntegerField(default=0)
    tashvighi = models.BigIntegerField(default=0)
    year = models.CharField(max_length=10)
    month = models.CharField(max_length=10)
    karaee = models.FloatField(default=0)
    amar = models.JSONField()

    class Meta:
        verbose_name = 'Hoghoogh'
        verbose_name_plural = 'Hoghooghs'

    def __str__(self):
        return f"{self.sum_calculate}"

    @classmethod
    def calculate_day_by_staff(cls, staff):
        day_ok = 0
        hoghooghexist = Hoghoogh.objects.filter(staff_id=staff.pk)
        if hoghooghexist:
            amar = Amar.objects.filter(staff_id=staff.pk).select_related('listprice').all().order_by('tarikh')
            result_day = []
            for res in amar:
                result_day.append(res.tarikh)
            day_ok = len(list(set(result_day)))
        return day_ok


class HoghooghArchive(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="hoghoogharchives")
    sum_calculate = models.BigIntegerField()
    sum_all = models.BigIntegerField()
    days = models.IntegerField()
    pele_price = models.BigIntegerField(default=0)
    total_pay = models.BigIntegerField(default=0)
    sarparasti = models.BigIntegerField(default=0)
    mosaede = models.BigIntegerField(default=0)
    vam = models.BigIntegerField(default=0)
    bime = models.BigIntegerField(default=0)
    tashvighi = models.BigIntegerField(default=0)
    year = models.CharField(max_length=10)
    month = models.CharField(max_length=10)
    karaee = models.FloatField(default=0)
    amar = models.JSONField()

    class Meta:
        verbose_name = 'HoghooghArchive'
        verbose_name_plural = 'HoghooghArchives'

    def __str__(self):
        return f"{self.sum_calculate}"


class Sarparasti(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    sum_day_sarparast = models.IntegerField(default=0)
    role = models.IntegerField(default=0)
    year = models.CharField(max_length=10)
    month = models.CharField(max_length=10)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='sarparast')

    class Meta:
        verbose_name = 'Sarparasti'
        verbose_name_plural = 'Sarparastiha'

    def __str__(self):
        return f"{self.staff} - {self.sum_day_sarparast}"

    @classmethod
    def calculate_tolid(cls, year_month):
        result = Sarparasti.objects.filter(year_month=year_month).annotate(
            sum_final_tolid=Sum(F('sum_all_tolid'))
        )
        return result

    @classmethod
    def calculate_sarparasti(cls, year, month, staff, location_id_id):
        result_sarparasti = []
        sum_price_sarparasti = 0
        all_day_sarparastha = 0
        location_id = staff.location_id
        paksazi = Sarparasti.objects.filter(~Q(role=3))
        paksazi.delete()
        sarparasti = Sarparasti.objects.filter(year=year).filter(month=month).filter(role=3)

        if sarparasti:
            settinghoghoogh = SettingHoghoogh.objects.filter(location=staff.location).first()
            darsad_sarparast = settinghoghoogh.darsad_sarparast
            sarparst = sarparasti.filter(staff_id=staff.pk).first()
            day_sarparast = sarparst.sum_day_sarparast
            all_day_sarparastha = sarparasti.aggregate(sum_all_day=Sum(F('sum_day_sarparast')))
            all_days = all_day_sarparastha['sum_all_day']

            tolid = Tolid.objects.filter(year=year, month=month, location_id=location_id)
            if tolid:
                final_tolid = tolid.first()
                sum_tolid_all = final_tolid.sum_tolid
                sum_tolid_calculate = sum_tolid_all * darsad_sarparast / 100

                one_price_sarparasti = sum_tolid_calculate / all_days

                sum_price_sarparasti = day_sarparast * one_price_sarparasti
        result_sarparasti.append(day_sarparast)
        result_sarparasti.append(int(one_price_sarparasti))
        result_sarparasti.append(int(sum_price_sarparasti))
        return result_sarparasti

    @classmethod
    def update_sarparastha(cls, ok_day, year, month, staff):
        location_id = staff.location_id
        sarparasti = Sarparasti.objects.filter(year=year).filter(month=month).filter(staff_id=staff.pk).filter(role=3)

        if sarparasti:
            oldsarparasti = sarparasti.first()
            oldsarparasti.sum_day_sarparast = ok_day
            oldsarparasti.role = staff.role
            oldsarparasti.save()
        else:
            newsarparasti = Sarparasti(sum_day_sarparast=ok_day, year=year, month=month, staff_id=staff.pk,
                                       location_id=location_id, role=staff.role)
            newsarparasti.save()


class Tolid(models.Model):
    sum_tolid = models.BigIntegerField(default=0)
    year = models.CharField(max_length=10)
    month = models.CharField(max_length=10)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='tolid')

    class Meta:
        verbose_name = 'Tolid'
        verbose_name_plural = 'Tolids'

    def __str__(self):
        return f"{self.sum_tolid} - {self.year}- {self.month}"

    @classmethod
    def calculate_tolid_all(cls, year, month, staff):
        location_id = staff.location_id
        tolid = Tolid.objects.filter(year=year, month=month, location_id=location_id)
        if tolid:
            oldtolid = tolid.first()
            amar = Amar.objects.filter(type='dates')
            if amar:
                amar2 = amar.select_related('listprice').all().order_by('tarikh')
                amar3 = amar2.aggregate(sum_all=Sum(F('price') * F('tedad')))
                oldtolid.sum_tolid = amar3['sum_all']
            else:
                oldtolid.sum_tolid = 0
            oldtolid.save()
            oldtolid.sum_tolid
        else:
            amar = Amar.objects.filter(type='dates')

            if amar:
                amar2 = amar.select_related('listprice').all().order_by('tarikh')
                amar3 = amar2.aggregate(sum_all=Sum(F('price') * F('tedad')))
                new_sum_tolid = amar3['sum_all']

            else:
                new_sum_tolid = 0

            newtolid = Tolid(sum_tolid=new_sum_tolid, year=year, month=month, location_id=location_id)
            newtolid.save()
            newtolid.sum_tolid







