from datetime import date
import jdatetime

###py -m pip install jdatetime
##py -m pip install  DateTime
today = date.today()
print(today)
this_year = date.today().year
this_month = date.today().month
this_day = date.today().day
str_date = jdatetime.date.fromgregorian(day=this_day, month=this_month, year=this_year)
print(str_date )
print(jdatetime.date(day=this_day, month=this_month, year=this_year).togregorian())
