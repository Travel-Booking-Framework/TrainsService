from django.db import models


class Station(models.Model):
    """Station Table"""
    station_name = models.CharField(max_length=255)  # نام ایستگاه
    station_city = models.CharField(max_length=255)  # شهر ایستگاه
    station_province = models.CharField(max_length=255)  # استان ایستگاه

    def __str__(self):
        return f"{self.station_name} ({self.station_city}, {self.station_province})"


class RailwayCompany(models.Model):
    """Railway Company Table"""
    railway_name = models.CharField(max_length=255)  # نام شرکت
    railway_description = models.TextField()  # توضیحات شرکت
    refund_policy = models.TextField()  # قوانین استرداد بلیط
    railway_logo = models.ImageField(upload_to='railway_company_logos/', blank=True, null=True)  # لوگوی شرکت

    def __str__(self):
        return self.railway_name


class TrainHall(models.Model):
    """TrainHall Table"""
    hall_name = models.CharField(max_length=255)  # نام سالن
    hall_description = models.TextField(blank=True, null=True)  # توضیحات سالن

    def __str__(self):
        return self.hall_name


class Train(models.Model):
    """Train Table"""
    TRAIN_TYPES = [
        ('4_coupe', 'Coupe 4-seater'),  # کوپه‌ای ۴ نفره
        ('bus', 'Bus-style'),          # اتوبوسی
        ('6_coupe', 'Coupe 6-seater'), # کوپه‌ای ۶ نفره
    ]

    train_number = models.CharField(max_length=50, unique=True)  # شماره قطار
    departure_datetime = models.DateTimeField()  # تاریخ و ساعت حرکت
    arrival_datetime = models.DateTimeField()  # تاریخ و ساعت رسیدن
    departure_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='departures')  # ایستگاه مبدا
    arrival_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='arrivals')  # ایستگاه مقصد
    railway_company = models.ForeignKey(RailwayCompany, on_delete=models.CASCADE)  # شرکت حمل‌ونقل ریلی
    train_type = models.CharField(max_length=20, choices=TRAIN_TYPES)  # نوع قطار
    capacity = models.IntegerField()  # ظرفیت قطار
    hall = models.ForeignKey(TrainHall, on_delete=models.CASCADE)  # نوع سالن
    stars = models.IntegerField(default=3)  # تعداد ستاره‌های قطار
    base_price = models.BigIntegerField()  # قیمت پایه
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # مالیات به صورت درصد
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # تخفیف به صورت درصد

    def __str__(self):
        return f"{self.train_number} ({self.train_type})"

    @property
    def final_price(self):
        """
        Calculate Final Price with tax & discount
        """
        discounted_price = self.base_price * (1 - (self.discount / 100))
        final_price = discounted_price * (1 + (self.tax / 100))
        return round(final_price)