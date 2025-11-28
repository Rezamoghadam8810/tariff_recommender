class CompanySnapshot:
    """
    نماینده یک شرکت معتمد در یک سال مشخص.
    شامل داده خام + رفتارهای مالی (profit, margin, success_rate)
    """

    def __init__(
        self,
        invoice_count,
        invoice_revenue,
        invoice_cost,
        support_revenue,
        support_cost,
        equipment_revenue,
        equipment_cost,
        other_revenue,
        other_cost,
        success_count,
        failed_count
    ):
        # --- داده های خام شرکت ---
        self.invoice_count = invoice_count                   # تعداد صورتحساب‌ها
        self.invoice_revenue = invoice_revenue               # درآمد فعلی از صورتحساب
        self.invoice_cost = invoice_cost                     # هزینه‌های مربوط به صورتحساب

        self.support_revenue = support_revenue               # درآمد پشتیبانی
        self.support_cost = support_cost                     # هزینه پشتیبانی

        self.equipment_revenue = equipment_revenue           # درآمد تجهیزات
        self.equipment_cost = equipment_cost                 # هزینه تجهیزات

        self.other_revenue = other_revenue                   # سایر درآمدها
        self.other_cost = other_cost                         # سایر هزینه‌ها

        self.success_count = success_count                   # تعداد موفق
        self.failed_count = failed_count                     # تعداد ناموفق

    # -------------------------------
    # رفتارهای مالی بر اساس تعرفه جدید n
    # -------------------------------

    def invoice_revenue_new(self, n):
        """درآمد جدید شرکت از صورتحساب‌ها تحت تعرفه n"""
        return self.invoice_count * n

    def total_revenue_new(self, n):
        """درآمد کل شرکت تحت تعرفه جدید"""
        return (
            self.invoice_revenue_new(n)
            + self.support_revenue
            + self.equipment_revenue
            + self.other_revenue
        )

    def total_cost(self):
        """هزینه کل شرکت (ثابت نسبت به n)"""
        return (
            self.invoice_cost
            + self.support_cost
            + self.equipment_cost
            + self.other_cost
        )

    def profit_new(self, n):
        """سود شرکت تحت تعرفه n"""
        return self.total_revenue_new(n) - self.total_cost()

    def margin_new(self, n):
        """حاشیه سود تحت تعرفه n"""
        revenue = self.total_revenue_new(n)
        if revenue == 0:
            return 0
        return self.profit_new(n) / revenue

    def success_rate(self):
        """نرخ موفقیت شرکت (کیفیت)"""
        total = self.success_count + self.failed_count
        if total == 0:
            return 0
        return self.success_count / total




#
# class CompanySnapshot:
#     def __init__(self,
#                  number_invoice,
#                  number_of_moadi,
#                  invoice_revenue,
#                  invoce_cost,
#                  suport_revenue,
#                  cost_revenue,
#                  tools_revenue,
#                  tools_cost,
#                  other_revenue,
#                  other_cost,
#                  sucsess_invoice,
#                  failde_invoice,
#
#                  ):
#         self.number_invoice = number_invoice
#         self.number_of_moadi= number_of_moadi
#         self.invoice_revenue= invoice_revenue
#         self.invoce_cost= invoce_cost
#         self.suport_revenue= suport_revenue
#         self.suport_cost= cost_revenue
#         self.tools_revenue= tools_revenue
#         self.tools_cost= tools_cost
#         self.other_revenue= other_revenue
#         self.other_cost= other_cost
#         self.sucsess_invoice= sucsess_invoice
#         self.failde_invoice= failde_invoice
#
#
#     def invoice_renenue_new(self,n):
#         return n * self.number_invoice
#
#     def total_reveneue_new(self,n):
#         return (self.invoice_renenue_new(n)+
#                 self.suport_revenue+
#                 self.tools_revenue+
#                 self.other_revenue)
#
#     def total_cost(self):
#         return (self.suport_cost +
#                 self.tools_cost+
#                 self.invoce_cost+
#                 self.other_cost)
#
#     def profit_new(self,n):
#         return self.total_reveneue_new(n) - self.total_cost()
#
#
#     def margin_new(self,n):
#         revenue = self.total_reveneue_new(n)
#         if revenue == 0:
#             return 0
#
#         return self.profit_new(n) / revenue
#
#     def sucsess_rate(self):
#         total = self.sucsess_invoice + self.failde_invoice
#         if total ==0:
#             return 0
#         return self.sucsess_invoice / total