class EvaluationResult:
    """
    نگه‌داری نتایج ارزیابی یک n مشخص.
    این کلاس هیچ محاسبه‌ای انجام نمی‌دهد.
    """

    def __init__(
        self,
        n: float,                # مقدار تعرفه تست‌شده
        score_budget: float,     # امتیاز بودجه
        score_health: float,     # امتیاز سلامت
        score_quality: float,    # امتیاز کیفیت
        score_total: float       # امتیاز کل
    ):
        self.n = n
        self.score_budget = score_budget
        self.score_health = score_health
        self.score_quality = score_quality
        self.score_total = score_total

    def __repr__(self):
        """نمایش خوانای نتیجه برای چاپ و دیباگ."""
        return (
            f"EvaluationResult(n={self.n}, "
            f"budget={self.score_budget:.3f}, "
            f"health={self.score_health:.3f}, "
            f"quality={self.score_quality:.3f}, "
            f"total={self.score_total:.3f})"
        )
