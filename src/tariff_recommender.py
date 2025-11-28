from src.company_snapshot import CompanySnapshot
from .scoring_engine import ScoringEngine
from .model_settings import ModelSettings
from .impact_report import ImpactReport
class TariffRecommender:
    """
    انتخاب بهترین تعرفه n براساس مدل امتیازدهی واقعی.
    """

    def __init__(self,settings:ModelSettings,engine:ScoringEngine):
        self.settings =settings
        self.engine = engine

    def find_nest_n(self,companies,n_values=None):
        if n_values is None:
            n_values = range(self.settings.n_min,self.settings.n_max + 1)

        all_results=[]
        best_result=None

        for n in n_values:
            result= self.engine.evaluate(n,companies)
            all_results.append(result)

            if best_result is None or result.score_total > best_result.score_total:
                best_result=result

        return best_result,all_results

    def generate_impact_report(self,n,companies):
        company_results=[]

        for c in companies:
            result = {
                "name": c.name if hasattr(c, "name") else None,
                "total_revenue": c.total_revenue_new(n),
                "total_cost": c.total_cost(),
                "profit": c.profit_new(n),
                "margin": c.margin_new(n),
                "success_rate": c.success_rate()
            }
            company_results.append(result)

        # خلاصه سازمان
        payout_total = sum(c.invoice_revenue_new(n) for c in companies)
        avg_margin = sum(c.margin_new(n) for c in companies) / len(companies)
        avg_quality = sum(c.success_rate() for c in companies) / len(companies)

        org_summary = {
            "payout_total": payout_total,
            "avg_margin": avg_margin,
            "avg_quality": avg_quality
        }

        return ImpactReport(n, company_results, org_summary)





