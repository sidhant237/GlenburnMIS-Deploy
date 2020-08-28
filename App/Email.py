from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
from App import app, mysql, mail
import json, datetime
from flask_mail import Message
import pandas as pd
from dateutil.relativedelta import relativedelta



@app.template_filter('total')
def total(data, column):
    total = 0
    print(data)
    for item in data:
        total += item[column]
    return total

#9m
@app.route('/email-report', methods=['GET', 'POST'])
@cross_origin()
def email():
    email_data, current_date = email_report()
    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    send_mail(email_data, current_date)
    return json.dumps({'message': 'success'})


def email_report():
    cur = mysql.connection.cursor()
    d1 = request.args.get("start")
    if not d1:
      d1 = '2020-08-26'
    d11 = "'" + str((datetime.datetime.strptime(d1, '%Y-%m-%d') - relativedelta(years=1))).split(' ')[0] + "'"
    d01 = "'" + str((datetime.datetime.strptime(d1, '%Y-%m-%d') - relativedelta(days=1))).split(' ')[0] + "'"
    d1 = "'" + d1 + "'"
    d0 = "'2020-03-01'"  # start date current year
    d00 = "'2019-03-01'"  # start date last year
    
    #DIV NAME
    val = "DivTab.Div_name"
    tab = "DivTab, SecTab, FieldEntry"
    joi = "(FieldEntry.Sec_ID=SecTab.Sec_ID) AND (SecTab.Div_ID = DivTab.Div_ID)"
    job = "FieldEntry.Job_ID = 1"
    cur.execute(f'''select {val} from {tab} where {joi} AND {job} and date = {d1} GROUP BY SecTab.Div_ID''')
    rv = cur.fetchall()

    # GL TODAY
    val1 = "SUM(FieldEntry.GL_Val)"
    tab1 = "DivTab, SecTab, FieldEntry"
    joi1 = "(FieldEntry.Sec_ID=SecTab.Sec_ID) AND (SecTab.Div_ID = DivTab.Div_ID)"
    job1 = "FieldEntry.Job_ID = 1"
    cur.execute(f'''select {val1} from {tab1} where {joi1} AND {job1} and Date = {d1} GROUP BY SecTab.Div_ID''')
    rv1 = cur.fetchall()

    #GL TODAY LAST YEA1R
    val2 = "sum(FieldEntry.GL_Val)"
    tab2 = "FieldEntry, DivTab, SecTab"
    joi2 = "(FieldEntry.Sec_ID=SecTab.Sec_ID) AND (SecTab.Div_ID = DivTab.Div_ID)"
    job2 = "FieldEntry.Job_ID = 1"
    cur.execute(f'''select {val2} from {tab2} where {joi2} AND {job2} and Date = {d11} GROUP BY SecTab.Div_ID''')
    rv2 = cur.fetchall()

    #FINE LEAF% TODAYS GL
    val3 = "sum(FL_Per)"
    tab3 = "FLEntry, DivTab"
    joi3 = "(FLEntry.Div_ID = DivTab.Div_ID)"
    cur.execute(f'''select {val3} from {tab3} where {joi3} and Date = {d1} GROUP BY DivTab.Div_ID''')
    rv3 = cur.fetchall()

    w = [i[0] for i in rv]
    x = [i1[0] for i1 in rv1]
    y = [i2[0] for i2 in rv2]
    z = [i3[0] for i3 in rv3]
    
    q = zip(w,x,y,z)
    json_data = []
    column_headers = ['Division','GLToday','GLTodayLY','FineLeaf']

    for row in q:
        json_data.append(dict(zip(column_headers, row)))
    

#8 TEAMADE##############

    cur = mysql.connection.cursor()
    rv = []

    # [TM TODAY]
    val = "TMEntry.TM_Val "
    tab = "TMEntry"
    cur.execute(f'''select {val} from {tab} where TM_Date = {d1} ''')
    rv.append(cur.fetchall()[0][0])

    # [TM TODATE]
    val1 = "sum(TMEntry.TM_Val)"
    tab1 = "TMEntry"
    cur.execute(f'''select {val1} from {tab1} where TM_Date >= {d0} AND TM_Date <= {d1} ''')
    rv.append(cur.fetchall()[0][0])

    # [TM TODATE LAST YEAR]
    val2 = "sum(TMEntry.TM_Val)"
    tab2 = "TMEntry"
    cur.execute(f'''select {val2} from {tab2} where TM_Date >= {d00} AND TM_Date <= {d11} ''')
    rv.append(cur.fetchall()[0][0])

    #[GL YEST]
    val3 = "sum(FieldEntry.GL_Val)"
    tab3 = "FieldEntry"
    cur.execute(f'''select {val3} from {tab3} where Date = {d01}''')
    rv3 = cur.fetchall()
    y = [i[0] for i in rv3]

    #[TM TODAY]
    val = "TMEntry.TM_Val "
    tab = "TMEntry"
    cur.execute(f'''select {val} from {tab} where TM_Date = {d1} ''')
    rv1 = cur.fetchall()
    x = [i[0] for i in rv1]

    #[GL TODATE]
    val3 = "sum(FieldEntry.GL_Val)"
    tab3 = "FieldEntry"
    cur.execute(f'''select {val3} from {tab3} where Date >= {d0} and Date <= {d01}''')
    rv4 = cur.fetchall()
    yy = [i[0] for i in rv4]
    
    #[TM TODATE]
    val1 = "sum(TMEntry.TM_Val)"
    tab1 = "TMEntry"
    cur.execute(f'''select {val1} from {tab1} where TM_Date >= {d0} AND TM_Date <= {d1} ''')
    rv2 = cur.fetchall()
    xx = [i[0] for i in rv2]

    #[Recovery today]
    z = round((x[0] / y[0])*100,2)
    rv.append(z)

    zz = round((xx[0]/yy[0])*100,2)
    rv.append(zz)   

    column_headers =  ['TMToday', 'TMTodate', 'TMTodateLY', 'RecoveryToday', 'RecoveryTodate']
    
    json_data1 = []
    json_data1.append(dict(zip(column_headers, rv)))
    
##########MANDAYS########

#5

    cur = mysql.connection.cursor()
    
    con = "Jobtab.JOB_NAME"
    val = "SUM(FieldEntry.Mnd_Val)"
    tab = "FieldEntry,Jobtab"
    joi = "FieldEntry.Job_ID=Jobtab.Job_ID"
    cur.execute(f'''select {con} , {val} from {tab} where {joi} and date >={d1} group by FieldEntry.Job_ID''')
    row_headers = ['Job_Name', 'Mandays']

    rv = cur.fetchmany(7)
    json_data2 = []

    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    for result in rv:
        json_data2.append(dict(zip(row_headers, result)))
    

################PLUCKDAILY
#3

    cur = mysql.connection.cursor()
    
    con = "DivTab.Div_name, SecTab.Sec_Name"
    val = "FieldEntry.Mnd_Val, FieldEntry.GL_Val, FieldEntry.Area_Val"
    fom = "ROUND((GL_Val/Mnd_Val),2), ROUND((GL_Val/Area_Val),2),ROUND((Mnd_Val/Area_Val),2)"
    tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab"
    joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID"
    job = "(FieldEntry.Job_ID = 1 )"
    cur.execute(f'''select {con} , {val} , {fom} from {tab} where {joi} and date ={d1} and {job}''')

    row_headers = ['Division','Section_Name', 'Mandays', 'Greenleaf', 'AreaCovered', 'GlMnd', 'GlHa', 'MndHa']
    rv = cur.fetchall()
    json_data3 = []


    def sids_converter(o):
            if isinstance(o, datetime.date):
                  return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    for result in rv:
            json_data3.append(dict(zip(row_headers , result)))



################
#CULT DAILY


    cur = mysql.connection.cursor()

    con = "Jobtab.JOB_NAME,DivTab.Div_name, SecTab.Sec_Name"
    val = "Mnd_Val, Area_Val"
    fom = "ROUND((Mnd_Val/Area_Val),2)"   
    tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab"
    joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID"
    job = "(FieldEntry.Job_ID = 2 or FieldEntry.Job_ID = 3 or FieldEntry.Job_ID = 4)"
    cur.execute(f'''select {con} , {val} , {fom} from {tab} where {joi} and date ={d1} and {job}''')
    rv = cur.fetchall()

    row_headers = ['Job_Name','Division','Section_Name', 'Mandays', 'AreaCovered', 'MndArea' ]
    json_data4 = []

    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    for result in rv:
        json_data4.append(dict(zip(row_headers , result)))
    


######################
#GRADE%
#10##

    cur = mysql.connection.cursor()

    #SUM-ALLGRADES-DATERANGE
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry WHERE date ={d1} ")
    rv = cur.fetchall()

          #SUM-ALLGRADES-DATE
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry WHERE date ={d1} ")
    rv3 = cur.fetchall()

          #SUM-PERGRADE-DATERANGE
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date ={d1} group by TeaGradeTab.TeaGrade_ID")
    rv1 = cur.fetchall()

          #PERGRADE-DATE
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date ={d1} group by TeaGradeTab.TeaGrade_ID ")
    rv4 = cur.fetchall()      

          #GRADE-NAME
    cur.execute(f"SELECT TeaGradeTab.TeaGrade_Name FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date ={d1}")
    rv2 = cur.fetchall()

    x = [s[0] for s in rv]
    xx = [s[0] for s in rv3]
    y = [i[0] for i in rv1]
    yy = [h[0] for h in rv4]
    w = [str(u[0]) for u in rv2]

    z = []
    for number in y:
          z.append((round((number / x[0]),2)*100))

    zz = []
    for number in yy:
          zz.append((round((number / xx[0]),2)*100))

    zzz = zip(w,zz,z)

    json_data5 = []    
    column_headers = ['Grade','PercentToday','PercentTodate']

    for row in zzz:
          json_data5.append(dict(zip(column_headers,row)))
    

    ############
    #6
    cur = mysql.connection.cursor()

    con = " MachineTab.MACH_NAME"
    fom = " sum(FuelEntry.Fuel_Val), sum(TM_Val), ROUND((SUM(TM_Val)/sum(FuelEntry.Fuel_Val)),2)"
    tab = "FuelEntry, MachineTab, FuelTab, TMEntry"
    joi = "FuelEntry.Fuel_ID = FuelTab.Fuel_ID AND FuelEntry.Mach_ID = MachineTab.Mach_ID AND TMEntry.TM_Date = FuelEntry.Date"
    cur.execute(f'''select {con} , {fom}  from {tab} where {joi} and Date = {d1} group by MachineTab.MACH_NAME''')
    rv = cur.fetchall()

    row_headers = ['Machine', 'FuelUsed' , 'TM', 'TMFuel']
    json_data6 = []

    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    for row in rv:
        json_data6.append(dict(zip(row_headers,row)))


    json_final = {}
    json_final['Greenleaf'] = json_data #4
    json_final['TeaMade'] = json_data1 #5
    json_final['Mandays'] = json_data2 #2
    json_final['Plucking'] = json_data3 #8
    json_final['Cultivation'] = json_data4 #5
    json_final['GradePer'] = json_data5 #3
    json_final['FuelReport'] = json_data6 #4

    return json_final, d1




def send_mail(email_data, current_date):
    current_date = datetime.datetime.strptime(current_date[1:11], '%Y-%m-%d')
    subject = "Garden Report " + current_date.strftime('%b %d %Y') 
    recipients = ['sidhant237@gmail.com'] # 'sidhant237@gmail.com' 
    body = "Good Day, \n\n Your Daily report file is here. \n\n Thank you."
    msg = Message(subject=subject, body=body, recipients=recipients, sender="from@example.com")
    msg.html = render_template('index.html', data = email_data, date=current_date)
 
    return mail.send(msg)