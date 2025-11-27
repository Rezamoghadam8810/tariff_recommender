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


    def evaluate(self, n, companies):
        """
        محاسبه امتیازهای تعرفه n با استفاده از داده‌های واقعی شرکت‌ها
        """

        # -----------------------------------------------------
        # 1) ستون بودجه
        # -----------------------------------------------------
        payout_total = sum(c.invoice_revenue_new(n) for c in companies)

        diff = abs(payout_total - self.settings.target_budget)
        score_budget = max(0, 1 - diff / self.settings.target_budget)

        # -----------------------------------------------------
        # 2) ستون سلامت مالی شرکت‌ها
        #    health_i = تابعی از margin_new(n)
        # -----------------------------------------------------
        min_margin = self.settings.min_margin

        company_health_scores = []
        company_weights = []

        for c in companies:
            margin = c.margin_new(n)

            if margin <= 0:
                health = 0
            elif margin >= min_margin:
                health = 1
            else:
                health = margin / min_margin

            company_health_scores.append(health)
            company_weights.append(c.invoice_count)

        # میانگین وزن‌دار سلامت
        if sum(company_weights) == 0:
            score_health = 0
        else:
            score_health = sum(h * w for h, w in zip(company_health_scores, company_weights)) / sum(company_weights)

        # -----------------------------------------------------
        # 3) ستون کیفیت (success_rate)
        # -----------------------------------------------------
        success_rates = [c.success_rate() for c in companies]
        invoice_weights = [c.invoice_count for c in companies]

        if sum(invoice_weights) == 0:
            score_quality = 0
        else:
            score_quality = sum(sr * w for sr, w in zip(success_rates, invoice_weights)) / sum(invoice_weights)

        # -----------------------------------------------------
        # 4) ستون نهایی
        # -----------------------------------------------------
        score_total = (
            self.settings.weight_budget * score_budget +
            self.settings.weight_health * score_health +
            self.settings.weight_quality * score_quality
        )

        # -----------------------------------------------------
        # 5) خروجی
        # -----------------------------------------------------
        return EvaluationResult(
            n=n,
            score_budget=score_budget,
            score_health=score_health,
            score_quality=score_quality,
            score_total=score_total,
            extra={"payout_total": payout_total}
        )
