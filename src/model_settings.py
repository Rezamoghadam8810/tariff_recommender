class ModelSettings:
    """
    تنظیمات مدل امتیازدهی واقعی
    """

    def __init__(
        self,
        weight_budget: float,     # وزن ستون بودجه
        weight_health: float,     # وزن ستون سلامت
        weight_quality: float,    # وزن ستون کیفیت
        target_budget: float,     # بودجه هدف سازمان
        min_margin: float,        # حداقل حاشیه سود قابل قبول برای سلامت شرکت
        n_min: int = 1,           # حداقل مقدار n قابل تست
        n_max: int = 1000 ,        # حداکثر مقدار n قابل تست
        coverage_ratio:float =0.0
    ):
        self.weight_budget = weight_budget
        self.weight_health = weight_health
        self.weight_quality = weight_quality

        self.target_budget = target_budget
        self.min_margin = min_margin

        self.n_min = n_min
        self.n_max = n_max
        self.coverage_ratio = coverage_ratio

    def validate_weights(self):
        total = self.weight_budget + self.weight_health + self.weight_quality
        if abs(total - 1.0) > 1e-6:
            raise ValueError(f"جمع وزن‌ها باید 1 باشد. مقدار فعلی: {total}")

    def as_dict(self):
        return self.__dict__.copy()


