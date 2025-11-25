


class ModelSettings:
    """
    نگه‌داری وزن‌ها، آستانه‌ها و محدودیت‌های سیستم.
    این کلاس فقط اطلاعات ثابت مدل را نگه می‌دارد
    و هیچ محاسبه‌ای انجام نمی‌دهد.
    """

    def __init__(
        self,
        budget_weight: float,       # وزن اهمیت بودجه در امتیازدهی
        health_weight: float,       # وزن اهمیت سلامت مالی شرکت‌ها
        quality_weight: float,      # وزن اهمیت کیفیت خدمات
        min_health_score: float,    # حداقل امتیاز سلامت قابل‌قبول (زیر این مقدار خوب نیست)
        min_quality_score: float,   # حداقل امتیاز کیفیت قابل‌قبول
        budget_tolerance: float,    # میزان انحراف مجاز بودجه نسبت به مقدار مطلوب
        n_min: int = 1,             # حداقل n قابل آزمایش
        n_max: int = 1000           # حداکثر n قابل آزمایش
    ):
        # وزن‌ها
        self.budget_weight = budget_weight          # وزن ستون بودجه
        self.health_weight = health_weight          # وزن ستون سلامت
        self.quality_weight = quality_weight        # وزن ستون کیفیت

        # آستانه‌ها (Thresholds)
        self.min_health_score = min_health_score    # حداقل امتیاز سلامت پذیرفته‌شده
        self.min_quality_score = min_quality_score  # حداقل امتیاز کیفیت پذیرفته‌شده
        self.budget_tolerance = budget_tolerance    # تلورانس مجاز بودجه

        # محدوده n
        self.n_min = n_min                          # پایین‌ترین مقدار n که اجازه داریم تست کنیم
        self.n_max = n_max                          # بالاترین مقدار n قابل تست

    def validate_weights(self):
        """چک می‌کند جمع وزن‌ها دقیقاً 1 باشد تا مدل منطقی بماند."""
        total = (
            self.budget_weight +
            self.health_weight +
            self.quality_weight
        )
        if abs(total - 1.0) > 1e-6:
            raise ValueError(f"جمع وزن‌ها باید 1 باشد. مقدار فعلی: {total}")

    def as_dict(self):
        """برگرداندن تنظیمات به صورت دیکشنری (برای ذخیره/لاگ/دیباگ)."""
        return self.__dict__.copy()


