bond_urls=list(set(bond_urls))

'https://puentenet.com/puente/tirsBonosGraficoPublicoAction!tirsBonosGrafico.action'

gov_arg_urls={
'AE48': 'Argentinien-_RepublikDL-Bonds_201848-Bond-2048-US040114HR43'
'AA46': 'Argentinien-_RepublikDL-Bonds_1746_SerC_P1-Bond-2046-US040114GY03'
'AC17': 'Argentinien-_RepublikDL-Bonds_201717-2117_RegS-Bond-2117-USP04808AN44'
}

gov_arg_cf={
'AE48': {'dates':[], 'cf':[]},
'AA46': {'dates':[], 'cf':[]},
'AC17': {'dates':[], 'cf':[]},
}

from datetime import datetime
datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
datetime_object

from dateutil import parser

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
},
'AE48':{
'issue_date':'2018-01-11',
'maturity_date':'2048-01-11',
'months':['01','7'],
'days':['22'],
'coupon':3.44
},

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

dates, cf= regular_bonds_cf_gen(issue_date, maturity_date, months, days, coupon)
for bond, params in gov_arg_params.items():
    issue_date, maturity_date, months, days, coupon= params.values()
    dates, cf= regular_bonds_cf_gen(issue_date, maturity_date, months, days, coupon)
    gov_arg_cf[bond]['dates']=dates
    gov_arg_cf[bond]['cf']=cf




gov_arg_cf['AE48']
