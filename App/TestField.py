from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
from App import app, mysql
import json, datetime
from dateutil.relativedelta import relativedelta

@app.route('/test',methods=['GET', 'POST'])
@cross_origin()
def cultivattset():
    cur = mysql.connection.cursor()
    d1 = "'2020-08-14'"
    d2 = "'2020-08-14'"

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
    cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date ={d2} group by TeaGradeTab.TeaGrade_ID")
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
    return json.dumps(json_data5)
