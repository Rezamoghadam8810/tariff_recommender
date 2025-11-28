from src.company_snapshot import CompanySnapshot
from .scoring_engine import ScoringEngine
from .model_settings import ModelSettings

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






        # if n_values is None:
        #     n_values=range(self.settings.n_min,self.settings.n_max + 1)
        #
        # results=[]
        # best_result = None
        #
        # for n in n_values:
        #     result=self.engine.evaluate(n, companies)
        #     results.append(result)
        #
        #     if best_result is None or result.score_total > best_result.score_total:
        #         best_result=result
        #
        # return best_result,result