from celery import shared_task
from django.utils import timezone

from transport.models import TransportReq


@shared_task
def deactivate_expired_requests():
    """
    این تسک درخواست‌هایی که expire_time آن‌ها گذشته است را غیرفعال می‌کند.
    """
    now = timezone.now()  # زمان فعلی را دریافت می‌کند
    expired_requests = TransportReq.objects.filter(expire_time__lt=now, status=TransportReq.ACTIVE)  # پیدا کردن درخواست‌های منقضی شده
    count = expired_requests.update(status=TransportReq.INACTIVE)  # به‌روزرسانی وضعیت آن‌ها به INACTIVE
    return f'{count} requests have been deactivated.'  # بازگرداندن تعداد درخواست‌های غیرفعال‌شده

# باید اینو اجرا کنم در linux
# celery -A rebo worker --loglevel=info
# celery -A rebo beat --loglevel=info
