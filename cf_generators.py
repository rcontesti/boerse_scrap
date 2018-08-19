from datetime import datetime
datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
datetime_object
from dateutil import parser
import pickle



"""gov_arg_cf={
'AE48': {'dates':[], 'cf':[]},
'AA46': {'dates':[], 'cf':[]},
'AC17': {'dates':[], 'cf':[]},
}"""



#regular bond params
gov_arg_params={
'AA46':{
'issue_date':'2016-04-22',
'maturity_date':'2046-04-22',
'months':['04','10'],
'days':['22'],
'coupon':3.35
},
'AC17':{
'issue_date':'2017-06-28',
'maturity_date':'2117-06-28',
'months':['06','12'],
'days':['28'],
'coupon':3.56
},
'AE48':{
'issue_date':'2018-01-11',
'maturity_date':'2048-01-11',
'months':['01','7'],
'days':['22'],
'coupon':3.44
}
}

#regular bonds cf gen
def regular_bonds_cf_gen(issue_date, maturity_date, months, days, coupon):
    lista=[str(y)+'/'+m+'/'+d for d in days for m in months for y in range(parser.parse(issue_date).year,parser.parse(maturity_date).year+1)]
    dates=[parser.parse(l) for l in lista]
    dates=sorted(dates)
    dates=[ date  for date in dates if ( date>=parser.parse(issue_date) and date<=parser.parse(maturity_date))]
    cf=[coupon]*len(dates)
    cf[0]=0
    cf[-1]+=100
    return dates, cf



params=gov_arg_params
cash_flows={}
for bond, p in params.items():
    dates, cf= regular_bonds_cf_gen(p['issue_date'], p['maturity_date'], p['months'], p['days'], p['coupon'])
    cash_flows[bond]={'Date': dates, 'cf': cf}


pickle.dump(cash_flows, open('cash_flows.p','wb'))
