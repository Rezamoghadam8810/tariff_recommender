from src.model_settings import ModelSettings
from src.scoring_engine import ScoringEngine
from src.tariff_recommender import TariffRecommender

from test_company_snapshot import CompanySnapshot


settings= ModelSettings(
    weight_budget=0.5,
    weight_health=0.3,
    weight_quality=0.2,
    target_budget=5_000_000_000,
    min_margin=0.20,
    n_min=200,
    n_max=500
)



company_a =CompanySnapshot(100_000,
                           30_000_000,
                           18_000_000,
                           10_000_000,
                           6_000_000,
                           5_000_000,
                           3_500_000,
                           2_000_000,
                           800_000,
                           98_000,
                           2_000)
company_b=CompanySnapshot(15000,4500000,3000000,2000000,1500000,500000,350000,150000,100000,14400,600)
company_c=CompanySnapshot(300000,60000000,45000000,20000000,12000000,9000000,7000000,4000000,1500000,285000,15000)

companies=[company_a,company_b,company_c]

engine=ScoringEngine(settings)
recommender=TariffRecommender(settings,engine)

n_values = range(200, 501, 10)

best_result, all_results = recommender.find_nest_n(companies,n_values)

print("Best n:", best_result.n)
print("Best total score:", best_result.score_total)


