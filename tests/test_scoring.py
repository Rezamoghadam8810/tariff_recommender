from src.model_settings import ModelSettings
from src.scoring_engine import ScoringEngine

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

# موتور امتیازدهی
engine = ScoringEngine(settings)

# تست n=300
result = engine.evaluate(300, data)

print("--------------")
print("خروجی EvaluationResult:")
print(result)
print("--------------")
print("جزئیات:")
print("n =", result.n)
print("score_budget =", result.score_budget)
print("score_health =", result.score_health)
print("score_quality =", result.score_quality)
print("score_total =", result.score_total)
