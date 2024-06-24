from datetime import datetime

from jdatetime import datetime as jdatetime


def convert_to_shamsi(miladi_date_str):
    # تبدیل رشته تاریخ میلادی به شی datetime
    miladi_date = datetime.strptime(miladi_date_str, "%Y-%m-%d %H:%M:%S.%f%z")

    # تبدیل تاریخ میلادی به تاریخ شمسی
    shamsi_date = jdatetime.fromgregorian(datetime=miladi_date)

    # ترجمه نام ماه از انگلیسی به فارسی
    month_names = {
        'Farvardin': '1',
        'Ordibehesht': '2',
        'Khordad': '3',
        'Tir': '4',
        'Mordad': '5',
        'Shahrivar': '6',
        'Mehr': '7',
        'Aban': '8',
        'Azar': '9',
        'Dey': '10',
        'Bahman': '11',
        'Esfand': '12'
    }

    # تبدیل نام ماه به فارسی
    shamsi_month_name = month_names[shamsi_date.strftime('%B')]

    # استخراج ساعت و دقیقه
    shamsi_hour = shamsi_date.hour
    shamsi_minute = shamsi_date.minute

    # فرمت‌بندی تاریخ شمسی به "روز ماه سال ساعت:دقیقه"
    shamsi_date_str = f'{shamsi_date.year}/{shamsi_date.month}/{shamsi_date.month}  {shamsi_date.hour}:{shamsi_date.minute}'

    return shamsi_date_str
