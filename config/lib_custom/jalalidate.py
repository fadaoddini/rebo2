import jdatetime


class MiladiToJalali:
    def __int__(self, timestamp_str):
        self.timestamp_str = timestamp_str
        super().__init__()

    @classmethod
    def to_jalali(cls, timestamp_str):
        timestamp_str = timestamp_str.split("T")
        tarikh = timestamp_str[0]
        tarikh = tarikh.split("-")
        year_tarikh = int(tarikh[0])
        month_tarikh = int(tarikh[1])
        day_tarikh = int(tarikh[2])
        zaman = timestamp_str[1][0:5]
        zaman = zaman.split(":")
        hour_zaman = zaman[0]
        minutes_zaman = zaman[1]

        test = jdatetime.date.fromgregorian(year=year_tarikh, month=month_tarikh, day=day_tarikh)
        tarikh_finished = test.strftime("%Y/%m/%d")
        hour_finished = hour_zaman+':'+minutes_zaman
        result = tarikh_finished + " ساعت " + hour_finished
        return result

    @classmethod
    def to_jalali_serializer(cls, new_time):
        timestamp_str = new_time.split(" ")
        tarikh = timestamp_str[0]
        tarikh = tarikh.split("-")
        year_tarikh = int(tarikh[0])
        month_tarikh = int(tarikh[1])
        day_tarikh = int(tarikh[2])
        zaman = timestamp_str[1][0:5]
        zaman = zaman.split(":")
        hour_zaman = zaman[0]
        minutes_zaman = zaman[1]
        #
        test = jdatetime.date.fromgregorian(year=year_tarikh, month=month_tarikh, day=day_tarikh)
        tarikh_finished = test.strftime("%Y/%m/%d")
        hour_finished = hour_zaman + ':' + minutes_zaman
        result = tarikh_finished + " ساعت " + hour_finished
        return result
