from datetime import datetime

from jdatetime import datetime as jdatetime


def convert_to_shamsi(miladi_date_str):
    # تبدیل رشته تاریخ میلادی به شی datetime
    miladi_date = datetime.fromisoformat(miladi_date_str)

    # تبدیل تاریخ میلادی به تاریخ شمسی
    shamsi_date = jdatetime.fromgregorian(datetime=miladi_date)

    # استخراج ساعت و دقیقه
    shamsi_hour = shamsi_date.hour
    shamsi_minute = shamsi_date.minute

    # فرمت‌بندی تاریخ شمسی به "سال/ماه/روز ساعت:دقیقه"
    shamsi_date_str = f'{shamsi_date.year}/{shamsi_date.month}/{shamsi_date.day} - {shamsi_hour:02d}:{shamsi_minute:02d}'

    return shamsi_date_str
