from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
from App import app, mysql
from dateutil.relativedelta import relativedelta
import json, datetime




@app.route('/', methods=['GET'])
@cross_origin()
def home():
	return "Application running successfully"


@app.route('/cultdaily',methods=['GET', 'POST'])
@cross_origin()
def cultivationdaily():
    cur = mysql.connection.cursor()
    d1 = "'" + (str(request.args.get("start"))) + "'"
    d2 = "'" + (str(request.args.get("end"))) + "'"

    con = "FieldEntry.Date, Jobtab.Job_Name, DivTab.Div_Name, SecTab.Sec_Name, SquTab.Squ_Name"
    val = "Mnd_Val, Area_Val"
    fom = "ROUND((Mnd_Val/Area_Val),2)"
    tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab"
    joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID"
    job = "(FieldEntry.Job_ID = 2 or FieldEntry.Job_ID = 3 or FieldEntry.Job_ID = 4)"
    cur.execute(f'''select {con} , {val} , {fom} from {tab} where {joi} and date >={d1} and date <={d2} and {job}''')
    rv = cur.fetchall()

    row_headers = ['Date', 'Job_Name', 'Division', 'Section_Name', 'Squad_Name', 'Mandays', 'AreaCovered', 'Mnd_Area']
    json_data = []

    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    for result in rv:
        json_data.append(dict(zip(row_headers , result)))
    return json.dumps(json_data, default=sids_converter)


#2
@app.route('/cultgroup',methods=['GET', 'POST'])
@cross_origin()
def cultivationgroup():
    cur = mysql.connection.cursor()
    # d1 = "'" + (str(request.args.get("start"))) + "'"
    # d2 = "'" + (str(request.args.get("end"))) + "'"
    # grp = "'" + (str(request.args.get("grpby"))) + "'"
    d1 = "'2020-07-01'"
    d2 = "'2020-07-14'"
    grp = "'job'"

    print(type(d1), type(grp))

    if grp == "'job'":
        con = "Jobtab.Job_Name"
        val = "sum(FieldEntry.Mnd_Val)"
        val1 = "sum(FieldEntry.Area_Val)"
        fom = "ROUND((sum(FieldEntry.Mnd_Val))/(sum(FieldEntry.Area_Val)),2)"
        tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab"
        joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID"
        job = "(FieldEntry.Job_ID = 2 or FieldEntry.Job_ID = 3 or FieldEntry.Job_ID = 4)"
        cur.execute(f'''select {con} , {val} , {val1} , {fom}  from {tab} where {joi} and date >={d1} and date <={d2} and {job} group by FieldEntry.Job_ID''')
        rv = cur.fetchall()
        row_headers = ['Job_Name', 'Mandays', 'AreaCovered', 'MndArea']

    elif grp == "'section'":
        con = "SecTab.Sec_Name"
        val = "sum(FieldEntry.Mnd_Val)"
        val1 = "sum(FieldEntry.Area_Val)"
        fom = "ROUND((SUM(FieldEntry.Mnd_Val))/(SUM(FieldEntry.Area_Val)),2)"
        tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab"
        joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID"
        cur.execute(f'''select {con} , {val} , {val1} , {fom}  from {tab} where {joi} and date >={d1} and date <={d2} group by FieldEntry.Sec_ID''')
        rv = cur.fetchall()
        row_headers = ['Section_Name', 'Mandays', 'AreaCovered', 'MndArea']

    json_data = []

    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data, default=sids_converter)



#3
@app.route('/pluckdaily',methods=['GET', 'POST'])
@cross_origin()
def pluckingdaily():
    cur = mysql.connection.cursor()
    d1 = "'" + (str(request.args.get("start"))) + "'"
    d2 = "'" + (str(request.args.get("end"))) + "'"

    con = "FieldEntry.date, DivTab.Div_Name, SecTab.Sec_Name,SquTab.Squ_Name"
    val = "FieldEntry.Mnd_Val, FieldEntry.GL_Val, FieldEntry.Area_Val"
    fom = "ROUND((GL_Val/Mnd_Val),2), ROUND((GL_Val/Area_Val),2),ROUND((Mnd_Val/Area_Val),2)"
    con2 = "SecTab.Sec_Prune , SecTab.Sec_Jat, SecTab.Sec_Area"
    tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab"
    joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID"
    job = "(FieldEntry.Job_ID = 1 )"
    cur.execute(f'''select {con} , {val} , {fom} , {con2} from {tab} where {joi} and date >={d1} and date <={d2} and {job}''')

    row_headers = ['Date', 'Division','Section_Name', 'Squad_Name', 'Mandays', 'Greenleaf', 'AreaCovered', 'GlMnd', 'GlHa', 'MndHa','Prune','Jat', 'SecArea']
    rv = cur.fetchall()
    json_data = []

    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    for result in rv:
        json_data.append(dict(zip(row_headers , result)))
    return json.dumps(json_data, default=sids_converter)


#4
@app.route('/pluckgroup',methods=['GET', 'POST'])
@cross_origin()
def pluckinggroup():
    cur = mysql.connection.cursor()
    d1 = "'" + (str(request.args.get("start"))) + "'"
    d2 = "'" + (str(request.args.get("end"))) + "'"
    grp = "'" + (str(request.args.get("grpby"))) + "'"
    
    if grp == "'Section'":
        con = "SecTab.Sec_Name"
        val = "sum(FieldEntry.Mnd_Val), sum(FieldEntry.GL_Val), sum(FieldEntry.Area_Val)"
        fom = "ROUND((sum(GL_Val)/sum(Mnd_Val)),2), ROUND((sum(GL_Val)/sum(Area_Val)),2),ROUND((sum(Mnd_Val)/sum(Area_Val)),2)"
        tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab"
        joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID"
        job = "(FieldEntry.Job_ID = 1 )"
        cur.execute(f'''select {con} , {val} , {fom} from {tab} where {joi} and date >={d1} and date <={d2} and {job} group by SecTab.Sec_ID''')
        row_headers = ['Section_Name', 'Mandays', 'Greenleaf', 'AreaCovered', 'GLMnd', 'GLArea', 'MndArea']
        rv = cur.fetchall()

    if grp == "'Division'":
        con = "DivTab.Div_Name"
        val = "sum(FieldEntry.Mnd_Val), sum(FieldEntry.GL_Val), sum(FieldEntry.Area_Val)"
        fom = "ROUND((SUM(GL_Val)/SUM(Mnd_Val)),2), ROUND((sum(GL_Val)/sum(Area_Val)),2),ROUND((SUM(Mnd_Val)/SUM(Area_Val)),2)"
        tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab"
        joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID"
        job = "(FieldEntry.Job_ID = 1 )"
        cur.execute(f'''select {con} , {val} , {fom} from {tab} where {joi} and date >={d1} and date <={d2} and {job} group by SecTab.Div_ID''')
        row_headers = ['Division', 'Mandays', 'Greenleaf', 'AreaCovered', 'GLMnd', 'GLArea', 'MndArea']
        rv = cur.fetchall()

    if grp == "'Squad'":
        con = "SquTab.Squ_Name"
        val = "sum(FieldEntry.Mnd_Val), sum(FieldEntry.GL_Val), sum(FieldEntry.Area_Val)"
        fom = "ROUND((sum(GL_Val)/sum(Mnd_Val)),2), ROUND((sum(GL_Val)/sum(Area_Val)),2),ROUND((sum(Mnd_Val)/sum(Area_Val)),2)"
        tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab"
        joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID"
        job = "(FieldEntry.Job_ID = 1 )"
        cur.execute(f'''select {con} , {val} , {fom} from {tab} where {joi} and date >={d1} and date <={d2} and {job} group by SquTab.Squ_ID order by SquTab.Squ_Name asc''')

        row_headers = ['Squad', 'Mandays', 'Greenleaf', 'AreaCovered', 'GLMnd', 'GLArea', 'MndArea']
        rv = cur.fetchall()

    json_data = []
    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, default=sids_converter)


#5
@app.route('/mnddeploy',methods=['GET', 'POST'])
@cross_origin()
def mandaydeployment():
    cur = mysql.connection.cursor()
    d1 = "'" + (str(request.args.get("start"))) + "'"
    d2 = "'" + (str(request.args.get("end"))) + "'"

    con = "Jobtab.Job_Name"
    val = "SUM(FieldEntry.Mnd_Val)"
    tab = "FieldEntry,Jobtab"
    joi = "FieldEntry.Job_ID=Jobtab.Job_ID"
    cur.execute(f'''select {con} , {val} from {tab} where {joi} and date >={d1} and date <={d2} group by FieldEntry.Job_ID''')
    row_headers = ['Job_Name', 'Mandays']

    rv = cur.fetchall()
    json_data = []

    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, default=sids_converter)


#6
@app.route('/fuelreport',methods=['GET', 'POST'])
@cross_origin()
def fuelreport():
    cur = mysql.connection.cursor()
    d1 = "'" + (str(request.args.get("start"))) + "'"
    d2 = "'" + (str(request.args.get("end"))) + "'"

    con = " MachineTab.Mach_Name"
    fom = " sum(FuelEntry.Fuel_Val), sum(TM_Val), ROUND((SUM(TM_Val)/sum(FuelEntry.Fuel_Val)),2)"
    tab = "FuelEntry, MachineTab, FuelTab, TMEntry"
    joi = "FuelEntry.Fuel_ID = FuelTab.Fuel_ID AND FuelEntry.Mach_ID = MachineTab.Mach_ID AND TMEntry.TM_Date = FuelEntry.Date"
    cur.execute(f'''select {con} , {fom}  from {tab} where {joi} and date >= {d1} and date <= {d2} group by MachineTab.Mach_Name''')
    rv = cur.fetchall()

    row_headers = ['Machine', 'FuelUsed' , 'TM', 'TMFuel']
    json_data = []

    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    for row in rv:
        json_data.append(dict(zip(row_headers,row)))
    return json.dumps(json_data, default=sids_converter)  


#7 tea stock - removed from app


#8
@app.route('/teamade', methods=['GET', 'POST'])
@cross_origin()
def displayteamade():
    cur = mysql.connection.cursor()   
    rv = []

    d1 = request.args.get("start") 
    d11 = "'" + str((datetime.datetime.strptime(d1, '%Y-%m-%d') - relativedelta(years=1))).split(' ')[0] + "'"
    d1 = "'" + d1 + "'"
    d0 = "'2020-03-01'"  # start date current year
    d00 = "'2019-03-01'"  # start date last year


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

    # [RECOVERY % TODAY
    val3 = " ROUND(SUM(FieldEntry.GL_Val)/SUM(TMEntry.TM_Val),4) * 100 "
    tab3 = "TMEntry , FieldEntry"
    joi3 = "(TMEntry.TM_Date = FieldEntry.Date) and (TMEntry.TM_Date="
    cur.execute(f'''select {val3} from {tab3} where {joi3}{d1})''')
    rv.append(cur.fetchall()[0][0])

    # [RECOVERY % TO DATE
    val4 = " ROUND(SUM(FieldEntry.GL_Val)/SUM(TMEntry.TM_Val),4) * 100 "
    tab4 = 'TMEntry , FieldEntry'
    joi4 = "(TMEntry.TM_Date = FieldEntry.Date) and (TMEntry.TM_Date>="
    cur.execute(f'''select {val4} from {tab4} where {joi4}{d0}) and (TMEntry.TM_Date<={d1})''')
    rv.append(cur.fetchall()[0][0])

    def sids_converter(o):
        if isinstance(o, datetime.date):
            return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    column_headers = ['TM Today', 'TM Todate', 'TM Todate LY', 'Recovery % Today', 'Recovery% Todate']
    json_data = []
    json_data.append(dict(zip(column_headers, rv)))
    return json.dumps(json_data, default=sids_converter)


#9##
@app.route('/GL',methods=['GET', 'POST'])
@cross_origin()
def greenleaf():
    cur = mysql.connection.cursor()
    d1 = request.args.get("start") #"2020-07-01"
    d11 = "'" + str((datetime.datetime.strptime(d1, '%Y-%m-%d') - relativedelta(years=1))).split(' ')[0] + "'"
    d1 = "'" + d1 + "'"

    #DIV NAME
    val = "DivTab.Div_Name"
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
    cur.execute(f'''select {val3} from {tab3} where {joi3} and date = {d1} GROUP BY DivTab.Div_ID''')
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
    return json.dumps(json_data)



#10## - PART OF FACTORY AND DAILY REPORT, MAYBE
@app.route('/gradeper',methods=['GET', 'POST'])
@cross_origin()
def gradepercent():
    cur = mysql.connection.cursor()
    d1 = "'" + (str(request.args.get("start"))) + "'"
    d2 = "'" + (str(request.args.get("end"))) + "'"
    

    #SUM-ALLGRADES-DATERANGE
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry WHERE date >={d1} and date <={d2} ")
    rv = cur.fetchall()

    #SUM-ALLGRADES-DATE
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry WHERE date ={d1} ")
    rv3 = cur.fetchall()

    #SUM-PERGRADE-DATERANGE
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date >={d1} and date <={d2} group by TeaGradeTab.TeaGrade_Name ")
    rv1 = cur.fetchall()

    #PERGRADE-DATE
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date ={d1} group by TeaGradeTab.TeaGrade_Name ")
    rv4 = cur.fetchall()      

    #GRADE-NAME
    cur.execute(f"SELECT TeaGradeTab.TeaGrade_Name FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date >={d1} and date <={d2} group by TeaGradeTab.TeaGrade_Name ")
    rv2 = cur.fetchall()

    x = [s[0] for s in rv]
    xx = [s[0] for s in rv3]
    y = [i[0] for i in rv1]
    yy = [i[0] for i in rv4]
    w = [str(u[0]) for u in rv2]

    z = []
    for number in y:
        z.append((round((number / x[0]),2)*100))

    zz = []
    for number in yy:
        zz.append((round((number / x[0]),2)*100))

    zzz = zip(w,zz,z)

    json_data = []    
    column_headers = ['Grade','PercentToday','PercentTodate']

    for row in zzz:
        json_data.append(dict(zip(column_headers,row)))
    return json.dumps(json_data)

      
#11
@app.route('/invoicelist',methods=['GET', 'POST'])
@cross_origin()
def invoicelist():
    d1 = "'" + (str(request.args.get("start"))) + "'"
    d2 = "'" + (str(request.args.get("end"))) + "'"  
    cur = mysql.connection.cursor()
    con = "InvoiceEntry.Invoice_No, TeaGradeTab.TeaGrade_Name"
    val = "InvoiceEntry.Net_Wt , InvoiceEntry.Papersacks, InvoiceEntry.Packdate"
    tab = "InvoiceEntry,TeaGradeTab"
    joi = "InvoiceEntry.TeaGrade_ID=TeaGradeTab.TeaGrade_ID"
    cur.execute(f'''select {con} , {val} from {tab} where {joi} and InvoiceEntry.Packdate >={d1} and InvoiceEntry.Packdate <={d2}''')
    row_headers = ['InvNo','Grade', 'NetWt','Papersacks','Packdate']
    rv = cur.fetchall()
    json_data = []

    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data, default=sids_converter)



@app.route('/dates',methods=['GET'])
@cross_origin()
def get_dates():
    cur = mysql.connection.cursor()
    cur.execute("select * from Date")
    headers = ['table', 'start', 'end']
    rv = cur.fetchall()
    json_data = []

    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    for result in rv:
        json_data.append(dict(zip(headers, result)))
    return json.dumps(json_data, default=sids_converter)
