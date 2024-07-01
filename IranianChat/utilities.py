from datetime import datetime
from jdatetime import datetime as jdatetime
import pytz


def convert_to_shamsi(miladi_date_str):
    # تنظیم منطقه زمانی به ایران
    iran_tz = pytz.timezone('Asia/Tehran')

    # تبدیل رشته تاریخ میلادی به شی datetime با منطقه زمانی ایران
    miladi_date = datetime.fromisoformat(miladi_date_str).astimezone(iran_tz)

    # تبدیل تاریخ میلادی به تاریخ شمسی
    shamsi_date = jdatetime.fromgregorian(datetime=miladi_date)

    # استخراج ساعت و دقیقه
    shamsi_hour = shamsi_date.hour
    shamsi_minute = shamsi_date.minute

    # فرمت‌بندی تاریخ شمسی به "سال/ماه/روز ساعت:دقیقه"
    shamsi_date_str = f'{shamsi_date.year}/{shamsi_date.month}/{shamsi_date.day} - {shamsi_hour:02d}:{shamsi_minute:02d}'

    return shamsi_date_str
