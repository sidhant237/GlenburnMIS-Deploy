from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
from App import app, mysql, mail
import json, datetime
from flask_mail import Message
import pandas as pd
from dateutil.relativedelta import relativedelta

#9m
@app.route('/email', methods=['GET', 'POST'])
@cross_origin()
def email():
    email_data = factory()
    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    send_mail(email_data)
    return json.dumps({'message': 'success'})


def fuel_report():
    cur = mysql.connection.cursor()
    d1 = "'2020-07-01'"
    d2 = "'2020-07-02'"
    fuel_report_row_headers = ['Machine', 'FuelUsed' , 'TM', 'TMFuel']
    fuel_report_data = []
    con = " MachineTab.Mach_Name"
    fom = " sum(FuelEntry.Fuel_Val), sum(TM_Val), ROUND((SUM(TM_Val)/sum(FuelEntry.Fuel_Val)),2)"
    tab = "FuelEntry, MachineTab, FuelTab, TMEntry"
    joi = "FuelEntry.Fuel_ID = FuelTab.Fuel_ID AND FuelEntry.Mach_ID = MachineTab.Mach_ID AND TMEntry.TM_Date = FuelEntry.Date"
    cur.execute(f'''select {con} , {fom}  from {tab} where {joi} and date >= {d1} and date <= {d2} group by MachineTab.Mach_Name''')
    rv = cur.fetchmany(5)
    for row in rv:
        fuel_report_data.append(dict(zip(fuel_report_row_headers,row)))
    return fuel_report_data


def factory():
    cur = mysql.connection.cursor()
    d1 = request.args.get("start") #"2020-07-01"
    d11 = "'" + str((datetime.datetime.strptime(d1, '%Y-%m-%d') - relativedelta(years=1))).split(' ')[0] + "'"
    d1 = "'" + d1 + "'"
    d2 = "'2020-07-03'"

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
    cur.execute(f'''select {val1} from {tab1} where {joi1} AND {job1} and date = {d1} GROUP BY SecTab.Div_ID''')
    rv1 = cur.fetchall()

    #GL TODAY LAST YEA1R
    val2 = "SUM(FieldEntry.GL_Val)"
    tab2 = "FieldEntry, DivTab, SecTab"
    joi2 = "(FieldEntry.Sec_ID=SecTab.Sec_ID) AND (SecTab.Div_ID = DivTab.Div_ID)"
    job2 = "FieldEntry.Job_ID = 1"
    cur.execute(f'''select {val2} from {tab2} where {joi2} AND {job2} and date = {d11} GROUP BY SecTab.Div_ID''')
    rv2 = cur.fetchall()

    #FINE LEAF% TODAYS GL
    val3 = "sum(FL_Per)"
    tab3 = "FLEntry, DivTab"
    joi3 = "(FLEntry.Div_ID = DivTab.Div_ID)"
    cur.execute(f'''select {val3} from {tab3} where {joi3} and date = {d2} GROUP BY DivTab.Div_ID''')
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
    


#8m
    cur = mysql.connection.cursor()    
    rva = []

    d0 = "'2020-03-01'"  # start date current year
    d00 = "'2019-03-01'"  # start date last year
    d1 = "'" + (str(request.args.get("start"))) + "'"
    d11 = str((datetime.datetime.strptime(d1, '%Y-%m-%d') - relativedelta(years=1))).split(' ')[0]

    # [TM TODAY]
    vala = "TMEntry.TM_Val "
    taba = "TMEntry"
    cur.execute(f'''select {vala} from {taba} where TM_Date = {d1} ''')
    rva.append(cur.fetchall()[0][0])

    # [TM TODATE]
    vala1 = "sum(TMEntry.TM_Val)"
    taba1 = "TMEntry"
    cur.execute(f'''select {vala1} from {taba1} where TM_Date >= {d0} AND TM_Date <= {d1} ''')
    rva.append(cur.fetchall()[0][0])

    # [TM TODATE LAST YEAR]
    vala2 = "sum(TMEntry.TM_Val)"
    taba2 = "TMEntry"
    cur.execute(f'''select {vala2} from {taba2} where TM_Date >= {d00} AND TM_Date <= {d11} ''')
    rva.append(cur.fetchall()[0][0])

    # [RECOVERY % TODAY
    vala3 = " ROUND(SUM(FieldEntry.GL_Val)/SUM(TMEntry.TM_Val),4) * 100 "
    taba3 = "TMEntry , FieldEntry"
    joia3 = "(TMEntry.TM_Date = FieldEntry.Date) and (TMEntry.TM_Date="
    cur.execute(f'''select {vala3} from {taba3} where {joia3}{d1})''')
    rva.append(cur.fetchall()[0][0])

    # [RECOVERY % TO DATE
    vala4 = " ROUND(SUM(FieldEntry.GL_Val)/SUM(TMEntry.TM_Val),4) * 100 "
    taba4 = 'TMEntry , FieldEntry'
    joia4 = "(TMEntry.TM_Date = FieldEntry.Date) and (TMEntry.TM_Date>="
    cur.execute(f'''select {vala4} from {taba4} where {joia4}{d0}) and (TMEntry.TM_Date<={d1})''')
    rva.append(cur.fetchall()[0][0])

    column_headers = ['TMToday', 'TMTodate', 'TMTodateLY', 'RecoveryToday', 'RecoveryTodate']
    json_data1 = []
    json_data1.append(dict(zip(column_headers, rva)))


#10m

    curb = mysql.connection.cursor()
    d1 = "'" + (str(request.args.get("start"))) + "'"
    d2 = "'" + (str(request.args.get("end"))) + "'"

    curb.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry WHERE date >={d1} and date <={d2} ")
    rvb = curb.fetchall()

    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date >={d1} and date <={d2} group by TeaGradeTab.TeaGrade_Name ")
    rvb1 = cur.fetchall()

    cur.execute(f"SELECT TeaGradeTab.TeaGrade_Name FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date >={d1} and date <={d2} group by TeaGradeTab.TeaGrade_Name ")
    rvb2 = cur.fetchall()

    xb = [s[0] for s in rvb]
    yb = [i[0] for i in rvb1]
    wb = [str(u[0]) for u in rvb2]

    zb = []
    for number in yb:
        zb.append((round((number / x[0]),2)*100))

    zz = zip(wb,yb,zb)

    json_data2 = []    
    column_headers = ('Grade','Qnty','Percent')

    for row in zz:
        json_data2.append(dict(zip(column_headers,row)))
    

#5m

    cur = mysql.connection.cursor()
    #d1 = "'" + (str(request.args.get("start"))) + "'"
    #d2 = "'" + (str(request.args.get("end"))) + "'"
    d1 = "'2020-07-01'"
    d2 = "'2020-07-04'"

    conc = "Jobtab.Job_Name"
    valc = "SUM(FieldEntry.Mnd_Val)"
    tabc = "FieldEntry,Jobtab"
    joic = "FieldEntry.Job_ID=Jobtab.Job_ID"
    cur.execute(f'''select {conc} , {valc} from {tabc} where {joic} and date >={d1} and date <={d2} group by FieldEntry.Job_ID''')
    row_headers = ['Job_Name', 'Mandays']

    rvc = cur.fetchmany(5)
    json_data3 = []

    for result in rvc:
        json_data3.append(dict(zip(row_headers, result)))
    

    json_submit = {}
    json_submit['Greenleaf'] = json_data
    json_submit['TeaMade'] = json_data1
    json_submit['GradePercent'] = json_data2
    json_submit['Mandays'] = json_data3
    json_submit['Fuel_Report'] = fuel_report()
    return json_submit




def send_mail(email_data):
    subject = "Excel Report"
    recipients = ['joshyjoy999@gmail.com'] # 'sidhant237@gmail.com' 
    body = "Good Day, \n\n Your Daily report file is here. \n\n Thank you."
    msg = Message(subject=subject, body=body, recipients=recipients, sender="from@example.com")
    msg.html = render_template('index.html', data = email_data)
 
    return mail.send(msg)