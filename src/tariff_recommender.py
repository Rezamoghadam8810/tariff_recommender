from .scoring_engine import ScoringEngine


class TariffRecommender:
    """
    مسئول انتخاب بهترین n از بین چندین مقدار.
    این کلاس خودش محاسبه انجام نمی‌دهد.
    فقط ScoringEngine را صدا می‌زند.
    """

    def __init__(self, engine: ScoringEngine):
        self.engine = engine  # موتور محاسباتی

    def run(self, n_values, data):
        """
        ورودی:
            n_values: لیست یا رنج nهای قابل تست
            data: داده واقعی شرکت‌ها
        خروجی:
            بهترین n
        """
        best_n = None
        best_score = -1

        # تست تک تک nها
        for n in n_values:
            result = self.engine.evaluate(n, data)

            if result.score_total > best_score:
                best_score = result.score_total
                best_n = n

        return best_n
