"""Reconcile supplied exports without claiming native workbook/SQL execution.
Usage: python scripts/check_snapshots.py PATH_TO_HR_CSV PATH_TO_GOLD_FOLDER
"""
import csv,hashlib,json,sys
from pathlib import Path
from collections import Counter
from decimal import Decimal

def read(p,delimiter=','):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=delimiter))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
hrfile=Path(sys.argv[1]);gold=Path(sys.argv[2]);hr=read(hrfile,';')
f=read(gold/'fact_sales.csv');p=read(gold/'dim_products.csv');c=read(gold/'dim_customers.csv')
products={r['product_key']:r for r in p};customers={r['customer_key']:r for r in c}
assert len(products)==len(p) and len(customers)==len(c)
assert all(r['product_key'] in products and r['customer_key'] in customers for r in f)
assert len({r['Employee_ID'] for r in hr})==len(hr)
sales=sum(Decimal(r['sales_amount'] or '0') for r in f);units=sum(int(r['quantity'] or 0) for r in f)
bikes=sum(Decimal(r['sales_amount'] or '0') for r in f if products[r['product_key']]['category']=='Bikes')
accessories=sum(int(r['quantity'] or 0) for r in f if products[r['product_key']]['category']=='Accessories')
missing=[r for r in f if not r['order_date'].strip()]
results={'review_date':'2026-11-13','method':'Python CSV reconciliation, not native SQL Server or Tableau execution','hr':{'rows':len(hr),'unique_employee_ids':len({r['Employee_ID'] for r in hr}),'active':sum(not r['Termdate'].strip() for r in hr),'terminated':sum(bool(r['Termdate'].strip()) for r in hr),'departments':dict(Counter(r['Department'] for r in hr)),'sha256':digest(hrfile)},'gold':{'sales_rows':len(f),'distinct_orders':len({r['order_number'] for r in f}),'customer_rows':len(c),'product_rows':len(p),'sales_amount':str(sales),'currency':'unspecified','units':units,'bikes_sales_share_pct':round(float(bikes/sales*100),2),'accessories_units_share_pct':round(accessories/units*100,2),'missing_order_date_rows':len(missing),'missing_date_sales':str(sum(Decimal(r['sales_amount'] or 0) for r in missing)),'unique_dimension_keys':True,'all_sales_match_one_customer_and_product':True,'join_preserves_rows_and_sales':True,'sha256':{name:digest(gold/name) for name in ['fact_sales.csv','dim_customers.csv','dim_products.csv']}}}
assert (results['hr']['rows'],results['hr']['active'],results['hr']['terminated'])==(8950,7984,966)
assert (len(f),results['gold']['distinct_orders'],sales,units)==(60398,27659,Decimal(29356250),60423)
print(json.dumps(results,indent=2))
