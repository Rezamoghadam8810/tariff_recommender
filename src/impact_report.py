

class ImpactReport:
    """
    گزارش اثرگذاری تعرفه n روی شرکت‌ها و سازمان.
    این کلاس فقط داده را نگه می‌دارد (Data Holder)،
    هیچ محاسبه‌ای انجام نمی‌دهد.
    """

    def __init__(self, n, company_results, org_summary):
        """
        company_results: لیست دیکشنری برای هر شرکت
        org_summary: دیکشنری خلاصه سازمان
        """
        self.n = n
        self.company_results = company_results
        self.org_summary = org_summary

    def as_dict(self):
        return {
            "n": self.n,
            "company_results": self.company_results,
            "org_summary": self.org_summary
        }
