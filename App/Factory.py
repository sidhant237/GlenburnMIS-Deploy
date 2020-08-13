from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
from App import app, mysql
import json, datetime
from dateutil.relativedelta import relativedelta



##################################
#12 FACTORY
@app.route('/factory', methods=['GET', 'POST'])
@cross_origin()
def displayfactory():      
      d1 = request.args.get("start") #"2020-07-01"
      if not d1:
            d1 = "2020-07-01"
      d11 = "'" + str((datetime.datetime.strptime(d1, '%Y-%m-%d') - relativedelta(years=1))).split(' ')[0] + "'"
      d1 = "'" + d1 + "'"
      d0 = "'2020-07-01'"  # start date current year
      d00 = "'2019-03-01'"  # start date last year
      
      cur = mysql.connection.cursor()     
      rv = []
      ##TEA MADE
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
      joi4 = "(TMEntry.TM_Date = FieldEntry.DATE) and (TMEntry.TM_Date>="
      cur.execute(f'''select {val4} from {tab4} where {joi4}{d0}) and (TMEntry.TM_Date<={d1})''')
      rv.append(cur.fetchall()[0][0])      

      column_headers =  ['TMToday', 'TMToDate', 'TMToDateLY', 'RecoveryToday', 'RecoveryToDate']
      json_data = []
      json_data.append(dict(zip(column_headers, rv)))



#9## GREENLEAF FACTORY

      cur = mysql.connection.cursor()
      
      #DIV NAME
      vala = "DivTab.DIV_NAME"
      taba = "DivTab, SecTab, FieldEntry"
      joia = "(FieldEntry.Sec_ID=SecTab.Sec_ID) AND (SecTab.Div_Id = DivTab.Div_Id)"
      joba = "FieldEntry.JOB_ID = 1"
      cur.execute(f'''select {vala} from {taba} where {joia} AND {joba} and Date = {d1} GROUP BY SecTab.Div_Id''')
      rva = cur.fetchall()

      # GL TODAY
      vala1 = "SUM(FieldEntry.GL_Val)"
      taba1 = "DivTab, SecTab, FieldEntry"
      joia1 = "(FieldEntry.Sec_ID=SecTab.Sec_ID) AND (SecTab.Div_Id = DivTab.Div_Id)"
      joba1 = "FieldEntry.JOB_ID = 1"
      cur.execute(f'''select {vala1} from {taba1} where {joia1} AND {joba1} and Date = {d1} GROUP BY SecTab.Div_Id''')
      rva1 = cur.fetchall()

      #GL TODAY LAST YEA1R
      vala2 = "SUM(FieldEntry.GL_Val)"
      taba2 = "FieldEntry, DivTab, SecTab"
      joia2 = "(FieldEntry.Sec_ID=SecTab.Sec_ID) AND (SecTab.Div_Id = DivTab.Div_Id)"
      joba2 = "FieldEntry.JOB_ID = 1"
      cur.execute(f'''select {vala2} from {taba2} where {joia2} AND {joba2} and Date = {d11} GROUP BY SecTab.Div_Id''')
      rva2 = cur.fetchall()

      #FINE LEAF% TODAYS GL
      vala3 = "sum(FL_PER)"
      taba3 = "FLEntry, DivTab"
      joia3 = "(FLEntry.Div_Id = DivTab.Div_Id)"
      cur.execute(f'''select {vala3} from {taba3} where {joia3} and Date = {d1} GROUP BY DivTab.Div_Id''')
      rva3 = cur.fetchall()

      w = [i[0] for i in rva]
      x = [i1[0] for i1 in rva1]
      y = [i2[0] for i2 in rva2]
      z = [i3[0] for i3 in rva3]
      
      q = zip(w,x,y,z)
      json_data1 = []
      column_headers = ['Division','GLToday','GLTodayLY','FineLeaf']

      for row in q:
            json_data1.append(dict(zip(column_headers, row)))
      


#10## GRADE PER FACTORY

      cur = mysql.connection.cursor()

      #SUM-ALLGRADES-DATERANGE
      cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry WHERE date ={d1} ")
      rv = cur.fetchall()

            #SUM-ALLGRADES-DATE
      cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry WHERE date ={d1} ")
      rv3 = cur.fetchall()

            #SUM-PERGRADE-DATERANGE
      cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date >={d1}")
      rv1 = cur.fetchall()

            #PERGRADE-DATE
      cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date ={d1} group by TeaGradeTab.TeaGrade_Name ")
      rv4 = cur.fetchall()      

            #GRADE-NAME
      cur.execute(f"SELECT TeaGradeTab.TeaGrade_Name FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date >={d1}")
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

      json_data5 = []    
      column_headers = ['Grade','PercentToday','PercentTodate']

      for row in zzz:
            json_data5.append(dict(zip(column_headers,row)))
      

      json_comp = {} 
      json_comp['TeaMade'] = json_data
      json_comp['Greenleaf'] = json_data1
      json_comp['GradePer'] =json_data5
      return json.dumps(json_comp)