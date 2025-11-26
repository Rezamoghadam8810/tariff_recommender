from .evaluation_result import EvaluationResult
from .model_settings import ModelSettings


class ScoringEngine:
    """
    این کلاس مسئول تمام محاسبه‌های مدل است.
    n را می‌گیرد → امتیازها را حساب می‌کند → EvaluationResult می‌سازد.
    """

    def __init__(self, settings: ModelSettings):
        self.settings = settings          # دسترسی به وزن‌ها و آستانه‌های مدل


    def score_budget(self, n: float, data):
        """
        نسخهٔ ساده تستی:
        هرچه n به بودجه هدف نزدیک‌تر باشد → امتیاز بالاتر
        """
        target_budget = data["target_budget"]
        predicted_cost = data["predicted_invoice_count"] * n

        diff = abs(predicted_cost - target_budget)

        # تبدیل اختلاف به امتیاز 0 تا 1 (خیلی ساده)
        score = max(0.0, 1 - diff / target_budget)
        return score

    def score_health(self, n: float, data):
        """
        نسخهٔ ساده تستی:
        هرچه n کمتر به حد ضرر شرکت‌ها برسد → امتیاز بالاتر
        """
        min_safe_n = data["min_safe_n"]
        if n < min_safe_n:
            return 0.0
        return 1.0

    def score_quality(self, n: float, data):
        """
        نسخهٔ ساده تستی:
        هرچه n بالاتر باشد → امتیاز کیفیت بهتر
        """
        max_quality_n = data["max_quality_n"]
        return min(1.0, n / max_quality_n)


    def evaluate(self, n: float, data):
        """
        برای یک n مشخص:
        - سه امتیاز را حساب می‌کند
        - امتیاز کل را با وزن‌ها ترکیب می‌کند
        - یک EvaluationResult می‌سازد
        """
        # مرحله 1: محاسبه سه امتیاز پایه
        score_budget = self.score_budget(n, data)
        score_health = self.score_health(n, data)
        score_quality = self.score_quality(n, data)

        # مرحله 2: ترکیب وزن‌ها برای امتیاز کل
        total = (
            score_budget * self.settings.budget_weight +
            score_health * self.settings.health_weight +
            score_quality * self.settings.quality_weight
        )

        # مرحله 3: ساخت EvaluationResult
        return EvaluationResult(
            n=n,
            score_budget=score_budget,
            score_health=score_health,
            score_quality=score_quality,
            score_total=total
        )

