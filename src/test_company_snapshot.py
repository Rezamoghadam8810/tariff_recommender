from company_snapshot import CompanySnapshot


company_a =CompanySnapshot(100000,30000000,180000000,100000000,6000000,5000000,3500000,2000000,800000,98000,2000)
company_b=CompanySnapshot(15000,4500000,3000000,2000000,1500000,500000,350000,150000,100000,14400,600)
company_c=CompanySnapshot(300000,60000000,45000000,20000000,12000000,9000000,7000000,4000000,1500000,285000,15000)

n =300

print("A margin:", company_a.margin_new(n))
print("A success:", company_a.success_rate())
print("B success:", company_b.success_rate())
print("C success:", company_c.success_rate())
