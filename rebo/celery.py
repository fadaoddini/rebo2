from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# تنظیم متغیر محیطی برای Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rebo.settings')

# ایجاد شیء Celery
app = Celery('rebo')


app.conf.beat_schedule = {
    'deactivate-expired-requests-every-hour': {
        'task': 'rebo.tasks.deactivate_expired_requests',
        'schedule': crontab(minute=0, hour='*/1'),  # اجرای وظیفه هر ساعت
    },
}

# بارگذاری تنظیمات از فایل settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# خودکارسازی پیدا کردن و ثبت task ها در کل برنامه
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
