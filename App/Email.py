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
    d1 = request.args.get("start")
    email_data, current_date = email_report(d1)
    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    send_mail(email_data, current_date)
    return json.dumps({'message': 'success'})


def email_report(d1):
    cur = mysql.connection.cursor()    
    if not d1:
        d1 = '2020-10-30'
    d11 = "'" + str((datetime.datetime.strptime(d1, '%Y-%m-%d') - relativedelta(years=1))).split(' ')[0] + "'"
    d01 = "'" + str((datetime.datetime.strptime(d1, '%Y-%m-%d') - relativedelta(days=1))).split(' ')[0] + "'"
    d1 = "'" + d1 + "'"
    d0 = "'2020-03-01'"  # start date current year
    d00 = "'2019-03-01'"  # start date last year
    
    #DIVISIONWISE GREENLEAF
    grow = []
    krow = []
    srow = []
    
    #DIV NAME - SINGLE STATEMENT
    cur.execute(f'''SELECT DivTab.Div_name FROM DivTab WHERE DivTab.Div_ID = 1''')
    grow.append(cur.fetchall()[0][0])

    cur.execute(f'''SELECT DivTab.Div_name FROM DivTab WHERE DivTab.Div_ID = 2''')
    krow.append(cur.fetchall()[0][0])

    cur.execute(f'''SELECT DivTab.Div_name FROM DivTab WHERE DivTab.Div_ID = 3''')
    srow.append(cur.fetchall()[0][0])

    # GL TODAY
    val1 = "SUM(FieldEntry.GL_Val)"
    tab1 = "DivTab, SecTab, FieldEntry"
    joi1 = "(FieldEntry.Sec_ID=SecTab.Sec_ID) AND (SecTab.Div_ID = DivTab.Div_ID)"
    job1 = "FieldEntry.Job_ID = 1"
    
    cur.execute(f'''select {val1} from {tab1} where {joi1} AND {job1} and Date = {d1} and SecTab.Div_ID = 1''')
    grow.append(cur.fetchall()[0][0])
    
    cur.execute(f'''select {val1} from {tab1} where {joi1} AND {job1} and Date = {d1} and SecTab.Div_ID = 2''')
    krow.append(cur.fetchall()[0][0])
    
    cur.execute(f'''select {val1} from {tab1} where {joi1} AND {job1} and Date = {d1} and SecTab.Div_ID = 3''')
    srow.append(cur.fetchall()[0][0])
    


    #GL TODAY LAST YEA1R
    val2 = "sum(FieldEntry.GL_Val)"
    tab2 = "FieldEntry, DivTab, SecTab"
    joi2 = "(FieldEntry.Sec_ID=SecTab.Sec_ID) AND (SecTab.Div_ID = DivTab.Div_ID)"
    job2 = "FieldEntry.Job_ID = 1"
    
    cur.execute(f'''select {val2} from {tab2} where {joi2} AND {job2} and Date = {d11} and SecTab.Div_ID = 1''')
    grow.append(cur.fetchall()[0][0])

    cur.execute(f'''select {val2} from {tab2} where {joi2} AND {job2} and Date = {d11} and SecTab.Div_ID = 2''')
    krow.append(cur.fetchall()[0][0])

    cur.execute(f'''select {val2} from {tab2} where {joi2} AND {job2} and Date = {d11} and SecTab.Div_ID = 3''')
    srow.append(cur.fetchall()[0][0])


    # GL TODATE
    val1 = "SUM(FieldEntry.GL_Val)"
    tab1 = "DivTab, SecTab, FieldEntry"
    joi1 = "(FieldEntry.Sec_ID=SecTab.Sec_ID) AND (SecTab.Div_ID = DivTab.Div_ID)"
    job1 = "FieldEntry.Job_ID = 1"
    
    cur.execute(f'''select {val1} from {tab1} where {joi1} AND {job1} and Date >= {d0} and Date <= {d1} and SecTab.Div_ID = 1''')
    grow.append(cur.fetchall()[0][0])

    cur.execute(f'''select {val1} from {tab1} where {joi1} AND {job1} and Date >= {d0} and Date <= {d1} and SecTab.Div_ID = 2''')
    krow.append(cur.fetchall()[0][0])

    cur.execute(f'''select {val1} from {tab1} where {joi1} AND {job1} and Date >= {d0} and Date <= {d1} and SecTab.Div_ID = 3''')
    srow.append(cur.fetchall()[0][0])


    #GL TODATE LAST YEA1R
    val2 = "sum(FieldEntry.GL_Val)"
    tab2 = "FieldEntry, DivTab, SecTab"
    joi2 = "(FieldEntry.Sec_ID=SecTab.Sec_ID) AND (SecTab.Div_ID = DivTab.Div_ID)"
    job2 = "FieldEntry.Job_ID = 1"
    
    cur.execute(f'''select {val2} from {tab2} where {joi2} AND {job2} and Date >= {d00} and Date <= {d11} and SecTab.Div_ID = 1''')
    grow.append(cur.fetchall()[0][0])

    cur.execute(f'''select {val2} from {tab2} where {joi2} AND {job2} and Date >= {d00} and Date <= {d11} and SecTab.Div_ID = 2''')
    krow.append(cur.fetchall()[0][0])

    cur.execute(f'''select {val2} from {tab2} where {joi2} AND {job2} and Date >= {d00} and Date <= {d11} and SecTab.Div_ID = 3''')
    srow.append(cur.fetchall()[0][0])
    


    #FINE LEAF% TODAYS GL
    cur.execute(f'''select sum(FL_Per) from FLEntry, DivTab where (FLEntry.Div_ID = DivTab.Div_ID) and Date = {d1} and DivTab.Div_ID = 1''')
    grow.append(cur.fetchall()[0][0])

    cur.execute(f'''select sum(FL_Per) from FLEntry, DivTab where (FLEntry.Div_ID = DivTab.Div_ID) and Date = {d1} and DivTab.Div_ID = 2''')
    krow.append(cur.fetchall()[0][0])

    cur.execute(f'''select sum(FL_Per) from FLEntry, DivTab where (FLEntry.Div_ID = DivTab.Div_ID) and Date = {d1} and DivTab.Div_ID = 3''')
    srow.append(cur.fetchall()[0][0])


    #FINE LEAF% GL LY
    cur.execute(f'''select sum(FL_Per) from FLEntry, DivTab where (FLEntry.Div_ID = DivTab.Div_ID) and Date = {d11} and DivTab.Div_ID = 1''')
    grow.append(cur.fetchall()[0][0])

    cur.execute(f'''select sum(FL_Per) from FLEntry, DivTab where (FLEntry.Div_ID = DivTab.Div_ID) and Date = {d11} and DivTab.Div_ID = 2''')
    krow.append(cur.fetchall()[0][0])

    cur.execute(f'''select sum(FL_Per) from FLEntry, DivTab where (FLEntry.Div_ID = DivTab.Div_ID) and Date = {d11} and DivTab.Div_ID = 3''')
    srow.append(cur.fetchall()[0][0])

    groww = []
    for x in grow:
        if not x:
            x = 0
        groww.append(x)
    
    kroww = []
    for x in krow:
        if not x:
            x = 0
        kroww.append(x)

    sroww = []
    for x in srow:
        if not x:
            x = 0
        sroww.append(x)

    
    czip = []
    czip.append(groww)  
    czip.append(kroww)
    czip.append(sroww)

    json_data = []
    column_headers = ['Division','GLToday','GLTodayLY','GLTodate','GLTodateLY','FineLeaf','FineLeafLY']
    for row in czip:
        json_data.append(dict(zip(column_headers, row)))
    

    #8 TEAMADE##############
    cur = mysql.connection.cursor()
    
    rv = []
    # [TM TODAY]
    val = "TMEntry.TM_Val "
    tab = "TMEntry"
    cur.execute(f'''select {val} from {tab} where TM_Date = {d1} ''')
    a = cur.fetchall()
    if not a:
        a = [[0]]
    rv.append(a[0][0])

    # [TM TODATE] - APPENDED
    val1 = "sum(TMEntry.TM_Val)"
    tab1 = "TMEntry"
    cur.execute(f'''select {val1} from {tab1} where TM_Date >= {d0} AND TM_Date <= {d1} ''')
    rv.append(cur.fetchall()[0][0])

    # [TM TODATE LAST YEAR] - APPENDED
    val2 = "sum(TMEntry.TM_Val)"
    tab2 = "TMEntry"
    cur.execute(f'''select {val2} from {tab2} where TM_Date >= {d00} AND TM_Date <= {d11} ''')
    rv.append(cur.fetchall()[0][0])

    # [TM TODATE] -- FOR +/-
    val1 = "sum(TMEntry.TM_Val)"
    tab1 = "TMEntry"
    cur.execute(f'''select {val1} from {tab1} where TM_Date >= {d0} AND TM_Date <= {d1} ''')
    tmtd = cur.fetchall()

    # [TM TODATE LAST YEAR] -- FOR +/-
    val2 = "sum(TMEntry.TM_Val)"
    tab2 = "TMEntry"
    cur.execute(f'''select {val2} from {tab2} where TM_Date >= {d00} AND TM_Date <= {d11} ''')
    tmtdly = cur.fetchall()

    # +/- APPENDED
    a = [i[0] for i in tmtd]
    b = [i[0] for i in tmtdly]
    c = a[0] - b[0]
    rv.append(c)

    #[GL YEST] - FOR RECOVERY%
    val3 = "sum(FieldEntry.GL_Val)"
    tab3 = "FieldEntry"
    cur.execute(f'''select {val3} from {tab3} where Date = {d01}''')
    rv3 = cur.fetchall()
    if not rv3[0][0]:
        glyest = [0]
    elif rv3[0][0] == 0:
        glyest = [0]
    else:
        glyest = rv3[0]
    
    
    #[TM TODAY] - FOR RECOVERY%
    val = "TMEntry.TM_Val "
    tab = "TMEntry"
    cur.execute(f'''select {val} from {tab} where TM_Date = {d1} ''')
    rv1 = cur.fetchall()
    if not rv1[0][0]:
        tmtoday = [0]
    elif rv1[0][0] == 0:
        tmtoday = [0]
    else:
        tmtoday = rv1[0]
    

    #[GL TODATE] - FOR RECOVERY%
    val3 = "sum(FieldEntry.GL_Val)"
    tab3 = "FieldEntry"
    cur.execute(f'''select {val3} from {tab3} where Date >= {d0} and Date <= {d01}''')
    rv4 = cur.fetchall()
    yy = [i[0] for i in rv4]
    
    #[TM TODATE] - FOR RECOVERY%
    val1 = "sum(TMEntry.TM_Val)"
    tab1 = "TMEntry"
    cur.execute(f'''select {val1} from {tab1} where TM_Date >= {d0} AND TM_Date <= {d1} ''')
    rv2 = cur.fetchall()
    xx = [i[0] for i in rv2]


    #[Recovery today] - APPENDED
    if glyest[0] == 0 or tmtoday[0] == 0:
        rv.append(0)
    else:
        rectoday = round((tmtoday[0] / glyest[0])*100,2)
        rv.append(rectoday)

    #RECOVERY% TODAY - APPENDED
    zz = round((xx[0]/yy[0])*100,2)
    rv.append(zz)   

    column_headers =  ['TMToday', 'TMTodate', 'TMTodateLY','Difference', 'RecoveryToday', 'RecoveryTodate']
    
    json_data1 = []
    json_data1.append(dict(zip(column_headers, rv)))
    
##########MANDAYS########

#5

    cur = mysql.connection.cursor()
    
    con = "JobType.JobType_Name"
    val = "SUM(FieldEntry.Mnd_Val)"
    tab = "FieldEntry,Jobtab,JobType"
    joi = "FieldEntry.Job_ID=Jobtab.Job_ID And Jobtab.Job_Type=JobType.Job_Type"
    cur.execute(f'''select {con} , {val} from {tab} where {joi} and date ={d1} group by JobType.JobType_Name order by sum(FieldEntry.Mnd_Val) DESC ''')
    row_headers = ['Job_Name', 'Mandays']

    rv = cur.fetchall()
    if not rv:
        rv = [[0,0]]

    json_data2 = []

    for result in rv:
        json_data2.append(dict(zip(row_headers, result)))
    

    

##################
#test
    cur = mysql.connection.cursor()

    con = "PruneTab.Prune_Name, SecTab.Sec_Name"
    val = "FieldEntry.Mnd_Val, FieldEntry.GL_Val, FieldEntry.Area_Val"
    fom = "ROUND((GL_Val/Mnd_Val),1), ROUND((GL_Val/Area_Val),1),ROUND((Mnd_Val/Area_Val),1)"
    con2 = "FieldEntry.Pluck_Int"
    tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab,PruneTab"
    joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID AND PruneTab.Prune_Type = SecTab.Prune_Type"
    job = "(FieldEntry.Job_ID = 1 )"
    cur.execute(f'''select {con} , {val} , {fom} ,{con2} from {tab} where {joi} and date= {d1} and {job} ORDER BY SecTab.Prune_Type DESC, (GL_Val/Area_Val) DESC ''')

    row_headers = ['Prune','Section_Name', 'Mandays', 'Greenleaf', 'AreaCovered', 'GlMnd', 'GlHa', 'MndHa','PluckInt']
    rv = cur.fetchall()
    if not rv:
        rv = [[0,0,0,0,0,0,0,0,0]]
    json_data3 = []

    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.month) + str("/") + str(o.day)

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
    job = "(Jobtab.Job_Group = 2)"
    cur.execute(f'''select {con} , {val} , {fom} from {tab} where {joi} and date ={d1} and {job}''')
    rv = cur.fetchall()
    if not rv:
        rv = [[0,0,0,0,0,0]]

    row_headers = ['Job_Name','Division','Section_Name', 'Mandays', 'AreaCovered', 'MndArea' ]
    json_data4 = []

    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    for result in rv:
        json_data4.append(dict(zip(row_headers , result)))
    


######################
#GRADE%
#10## GRADE PER FACTORY

    cur = mysql.connection.cursor()

    #SUM-ALLGRADES-TODATE
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry WHERE date >= {d0} and date <={d1} ")
    rv = cur.fetchall()

    #SUM-ALLGRADES-TODAY
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry WHERE date ={d1} ")
    rv3 = cur.fetchall()
    xx = [s[0] for s in rv3]
    
    

    #SUM-PERGRADE-DATERANGE
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date >= {d0} and date <={d1} group by TeaGradeTab.TeaGrade_ID order by TeaGradeTab.TeaGrade_ID ASC")
    rv1 = cur.fetchall()

    #PERGRADE-TODAY
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date ={d1} group by TeaGradeTab.TeaGrade_ID order by TeaGradeTab.TeaGrade_ID ASC")
    rv4 = cur.fetchall()
    yy = []
    for n in rv4:
        if not n:
            n = [0]
        yy.append(n[0])


    #GRADEWISE KG TODAY
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date ={d1} and TeaGradeTab.TeaGrade_ID = 1 ")
    g1 = cur.fetchall()[0]
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date ={d1} and TeaGradeTab.TeaGrade_ID = 2 ")
    g2 = cur.fetchall()[0]
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date ={d1} and TeaGradeTab.TeaGrade_ID = 3 ")
    g3 = cur.fetchall()[0]
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date ={d1} and TeaGradeTab.TeaGrade_ID = 4 ")
    g4 = cur.fetchall()[0]
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date ={d1} and TeaGradeTab.TeaGrade_ID = 5 ")
    g5 = cur.fetchall()[0]
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date ={d1} and TeaGradeTab.TeaGrade_ID = 6 ")
    g6 = cur.fetchall()[0]
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date ={d1} and TeaGradeTab.TeaGrade_ID = 7 ")
    g7 = cur.fetchall()[0]
    
    glist = g1 + g2 + g3 + g4 + g5 + g6 + g7
    gtoday = []
    for n in glist:
        if not n:
            n = 0
        gtoday.append(n)    


    #GRADE-NAME
    cur.execute(f"SELECT TeaGradeTab.TeaGrade_Name FROM TeaGradeTab order by TeaGradeTab.TeaGrade_ID ASC")#and date ={d1}
    rv2 = cur.fetchall()

    
    x = [s[0] for s in rv]
    y = [i[0] for i in rv1]
    w = [str(u[0]) for u in rv2]

    z = []
    for number in y:
        z.append(round(((number / x[0])*100),2))

    zz = []

    if not xx[0]:
        for number in gtoday:
            zz.append(0)
    else:
        for number in gtoday:
            zz.append(round(((number / xx[0])*100),2))

    if not zz:
        zz = [0,0,0,0,0,0,0,0]

    zzz = zip(w,zz,z)

    json_data5 = []    
    column_headers = ['Grade','PercentToday','PercentTodate']

    for row in zzz:
        json_data5.append(dict(zip(column_headers,row)))
    

    ############
    #6
    cur = mysql.connection.cursor()

    con = " MachineTab.MACH_NAME"
    fom = " sum(FuelEntry.Fuel_Val), TMEntry.TM_Val, ROUND((SUM(FuelEntry.Fuel_Val)/TMEntry.TM_Val),2)"
    tab = "FuelEntry, MachineTab, FuelTab, TMEntry"
    joi = "FuelEntry.Fuel_ID = FuelTab.Fuel_ID AND FuelEntry.Mach_ID = MachineTab.Mach_ID AND TMEntry.TM_Date = FuelEntry.Date"
    cur.execute(f'''select {con} , {fom}  from {tab} where {joi} and Date = {d1} group by MachineTab.MACH_NAME''')
    rv = cur.fetchall()
    if not rv:
        rv = [[0,0,0,0]]

    row_headers = ['Machine', 'FuelUsed' , 'TM', 'TMFuel']
    json_data6 = []
    
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
    recipients = ['spteaplanter@gmail.com','anshuman239@gmail.com','palzolama@gmail.com','alokeroytea@gmail.com','glenburn1859@yahoo.co.in','sidhant237@gmail.com'] # 'sidhant237@gmail.com' 
    #recipients = ['sidhant237@gmail.com']
    body = "Good Day, \n\n Your Daily report file is here. \n\n Thank you."
    msg = Message(subject=subject, body=body, recipients=recipients, sender="from@example.com")
    msg.html = render_template('index.html', data = email_data, date=current_date)
 
    return mail.send(msg)