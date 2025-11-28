from src.model_settings import ModelSettings
from src.scoring_engine import ScoringEngine
from src.tariff_recommender import TariffRecommender


# داده تستی
data = {
    "target_budget": 5_000_000_000,
    "predicted_invoice_count": 20_000_000,
    "min_safe_n": 250,
    "max_quality_n": 700
}

# تنظیمات مدل
settings = ModelSettings(
    budget_weight=0.5,
    health_weight=0.3,
    quality_weight=0.2,
    min_health_score=0.5,
    min_quality_score=0.5,
    budget_tolerance=0.1
)

# موتور محاسباتی
engine = ScoringEngine(settings)

# توصیه‌گر
recommender = TariffRecommender(engine)

# لیست nهای قابل تست
n_values = [200, 250, 300, 350, 400]

best_n = recommender.run(n_values, data)

print("n های تست شده:", n_values)
print("بهترین n:", best_n)
