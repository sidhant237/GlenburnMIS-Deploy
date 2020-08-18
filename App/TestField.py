import datetime
from dateutil.relativedelta import relativedelta

d1 = "2020-08-14"
d11 = "'" + str((datetime.datetime.strptime(d1, '%Y-%m-%d') - relativedelta(months=2))).split(' ')[0] + "'"
print(d11)