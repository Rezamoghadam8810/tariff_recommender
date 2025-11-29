import streamlit as st
import pandas as pd
import sys
import os

# مسیر ریشه پروژه
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.model_settings import ModelSettings
from src.company_snapshot import CompanySnapshot
from src.tariff_recommender import TariffRecommender
from src.scoring_engine import ScoringEngine


# ---------------------------------------------------------
# پاکسازی ستون‌های عددی (تبدیل رشته → عدد)
# ---------------------------------------------------------
def clean_numeric(df, cols):
    for col in cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace(" ", "", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df


# ---------------------------------------------------------
# تبدیل DataFrame اکسل → لیست CompanySnapshot
# ---------------------------------------------------------
def df_to_companies(df):
    companies = []

    for _, row in df.iterrows():
        companies.append(
            CompanySnapshot(
                name=row["نام شرکت معتمد"],
                year=row["سال"] if "سال" in df.columns else 1402,

                invoice_count=row["تعداد صورتحساب"],
                taxpayers_count=row["تعداد مودی"],

                invoice_revenue=row["درآمد صورتحساب"],
                invoice_cost=row["هزینه صورتحساب"],

                support_revenue=row["درآمد خدمات سامانه ای -پشتیبانی"],
                support_cost=row["هزینه خدمات سامانه ای -پشتیبانی"],

                equipment_revenue=row["درآمد فروش تجهیزات"],
                equipment_cost=row["هزینه فروش تجهیزات"],

                other_revenue=row["سایر درآمد ها"],
                other_cost=row["سایر هزینه ها"],

                success_count=row["تعداد صورتحساب موفق"],
                failed_count=row["تعداد صورتحساب ناموفق"],
            )
        )

    return companies


# ---------------------------------------------------------
# اجرای مدل برای یک n
# ---------------------------------------------------------
def run_model(companies, n, budget):
    settings = ModelSettings(
        weight_budget=0.5,
        weight_health=0.3,
        weight_quality=0.2,
        target_budget=budget,
        min_margin=0.1,
        n_min=100,
        n_max=50000
    )

    engine = ScoringEngine(settings)
    recommender = TariffRecommender(settings, engine)

    impact = recommender.generate_impact_report(n, companies)

    payout_total = impact.org_summary["payout_total"]
    avg_margin = impact.org_summary["avg_margin"]
    avg_quality = impact.org_summary["avg_quality"]

    rows = []
    for c in companies:
        rows.append({
            "نام شرکت": c.name,
            "درآمد جدید": c.total_revenue_new(n),
            "سود جدید": c.profit_new(n),
            "حاشیه سود جدید": c.margin_new(n),
            "نرخ موفقیت": c.success_rate(),
        })

    df_companies = pd.DataFrame(rows)

    summary = {
        "payout_total": payout_total,
        "avg_margin": avg_margin,
        "avg_quality": avg_quality,
        "n": n,
    }

    return summary, df_companies


# ---------------------------------------------------------
# رابط کاربری
# ---------------------------------------------------------
def main():
    st.set_page_config(layout="wide", page_title="Tariff Recommender")

    st.title("📊 سیستم توصیه‌گر تعرفه برای شرکت‌های معتمد")
    st.sidebar.header("ورودی‌ها")

    # ---------------------------------------------------------
    # Session State: ذخیره داده اکسل
    # ---------------------------------------------------------
    if "df" not in st.session_state:
        st.session_state.df = None

    # ---- بارگذاری فایل اکسل ----
    file = st.sidebar.file_uploader("فایل اکسل شرکت‌های معتمد", type=["xlsx"])

    if file is not None:
        df = pd.read_excel(file, sheet_name="Sheet1")

        numeric_cols = [
            "تعداد صورتحساب",
            "تعداد مودی",
            "درآمد صورتحساب",
            "هزینه صورتحساب",
            "درآمد خدمات سامانه ای -پشتیبانی",
            "هزینه خدمات سامانه ای -پشتیبانی",
            "درآمد فروش تجهیزات",
            "هزینه فروش تجهیزات",
            "سایر درآمد ها",
            "سایر هزینه ها",
            "تعداد صورتحساب موفق",
            "تعداد صورتحساب ناموفق",
        ]

        df = clean_numeric(df, numeric_cols)
        st.session_state.df = df  # ذخیره در session

    # اگر هنوز فایل بارگذاری نشده:
    if st.session_state.df is None:
        st.info("فایل اکسل را بارگذاری کنید.")
        return

    df = st.session_state.df

    # ---- ورودی‌های بودجه و n ----
    budget = st.sidebar.number_input(
        "بودجه هدف سازمان (ریال)",
        min_value=0,
        value=50_000_000_000,
        step=1_000_000_000,
        format="%d",
    )

    n = st.sidebar.slider(
        "انتخاب مقدار تعرفه  (ریال)",
        min_value=100,
        max_value=50000,
        value=100,
        step=100,
    )

    # ---- تبدیل DF → لیست شرکت‌ها ----
    companies = df_to_companies(df)

    # ---------------------------------------------------------
    # Tabs
    # ---------------------------------------------------------
    tab1, tab2 = st.tabs(["📈 تحلیل تعرفه انتخاب‌شده", "🏆 بهترین تعرفه"])

    # ----------------------
    # تب ۱: تحلیل n فعلی
    # ----------------------
    with tab1:
        summary, df_comp = run_model(companies, n, budget)

        st.subheader("خلاصه تحلیل")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("تعرفه انتخاب شده", f"{summary['n']:,}")
        c2.metric("کل پرداختی", f"{int(summary['payout_total']):,}")
        c3.metric("میانگین حاشیه سود", f"{summary['avg_margin']:.2%}")
        c4.metric("میانگین کیفیت", f"{summary['avg_quality']:.2f}")

        st.subheader("وضعیت شرکت‌ها")

        def highlight_by_margin(row):
            margin = row["حاشیه سود جدید"]
            if margin <= 0:
                return ["background-color: #ffcccc"] * len(row)
            else:
                return ["background-color: #ccffcc"] * len(row)

        st.dataframe(df_comp.style.apply(highlight_by_margin, axis=1), use_container_width=True)

    # ----------------------
    # تب ۲: بهترین n
    # ----------------------
    with tab2:
        st.subheader("🏆 بهترین تعرفه پیشنهادی مدل")

        settings = ModelSettings(
            weight_budget=0.5,
            weight_health=0.3,
            weight_quality=0.2,
            target_budget=budget,
            min_margin=0.1,
            n_min=100,
            n_max=50000
        )

        engine = ScoringEngine(settings)
        recommender = TariffRecommender(settings, engine)

        # این تابع را باید در کد backend اضافه کرده باشید:
        # def find_best_n(self, companies, n_values=None): return self.find_nest_n(companies, n_values)
        best_result, all_results = recommender.find_best_n(companies)

        b1, b2, b3, b4 = st.columns(4)
        b1.metric("بهترین تعرفه", f"{best_result.n:,}")
        b2.metric("امتیاز کل", f"{best_result.score_total:.4f}")
        b3.metric("امتیاز بودجه", f"{best_result.score_budget:.4f}")
        b4.metric("امتیاز کیفیت", f"{best_result.score_quality:.4f}")


if __name__ == "__main__":
    main()
