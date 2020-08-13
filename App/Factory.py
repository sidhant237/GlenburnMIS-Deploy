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
      d11 = "'" + str((datetime.datetime.strptime(d1, '%Y-%m-%d') - relativedelta(years=1))).split(' ')[0] + "'"
      d1 = "'" + d1 + "'"
      d0 = "'2020-07-01'"  # start date current year
      d00 = "'2019-03-01'"  # start date last year
      
      cur = mysql.connection.cursor()     
      rv = []
      ##TEA MADE
      # [TM TODAY]
      val = "TMENTRY.TM_VAL "
      tab = "TMENTRY"
      cur.execute(f'''select {val} from {tab} where TM_DATE = {d1} ''')
      rv.append(cur.fetchall()[0][0])

      # [TM TODATE]
      val1 = "sum(TMENTRY.TM_VAL)"
      tab1 = "TMENTRY"
      cur.execute(f'''select {val1} from {tab1} where TM_DATE >= {d0} AND TM_DATE <= {d1} ''')
      rv.append(cur.fetchall()[0][0])

      # [TM TODATE LAST YEAR]
      val2 = "sum(TMENTRY.TM_VAL)"
      tab2 = "TMENTRY"
      cur.execute(f'''select {val2} from {tab2} where TM_DATE >= {d00} AND TM_DATE <= {d11} ''')
      rv.append(cur.fetchall()[0][0])

      # [RECOVERY % TODAY
      val3 = " ROUND(SUM(FIELDENTRY.GL_VAL)/SUM(TMENTRY.TM_VAL),4) * 100 "
      tab3 = "TMENTRY , FIELDENTRY"
      joi3 = "(TMENTRY.TM_DATE = FIELDENTRY.DATE) and (TMENTRY.TM_DATE="
      cur.execute(f'''select {val3} from {tab3} where {joi3}{d1})''')
      rv.append(cur.fetchall()[0][0])

      # [RECOVERY % TO DATE
      val4 = " ROUND(SUM(FIELDENTRY.GL_VAL)/SUM(TMENTRY.TM_VAL),4) * 100 "
      tab4 = 'TMENTRY , FIELDENTRY'
      joi4 = "(TMENTRY.TM_DATE = FIELDENTRY.DATE) and (TMENTRY.TM_DATE>="
      cur.execute(f'''select {val4} from {tab4} where {joi4}{d0}) and (TMENTRY.TM_DATE<={d1})''')
      rv.append(cur.fetchall()[0][0])      

      column_headers =  ['TMToday', 'TMTodate', 'TMTodateLY', 'RecoveryToday', 'RecoveryTodate']
      json_data = []
      json_data.append(dict(zip(column_headers, rv)))



#9## GREENLEAF FACTORY

      cur = mysql.connection.cursor()
      
      #DIV NAME
      vala = "DIVTAB.DIV_NAME"
      taba = "DIVTAB, SECTAB, FIELDENTRY"
      joia = "(FIELDENTRY.SEC_ID=SECTAB.SEC_ID) AND (SECTAB.DIV_ID = DIVTAB.DIV_ID)"
      joba = "FIELDENTRY.JOB_ID = 1"
      cur.execute(f'''select {vala} from {taba} where {joia} AND {joba} and date = {d1} GROUP BY SECTAB.DIV_ID''')
      rva = cur.fetchall()

      # GL TODAY
      vala1 = "SUM(FIELDENTRY.GL_VAL)"
      taba1 = "DIVTAB, SECTAB, FIELDENTRY"
      joia1 = "(FIELDENTRY.SEC_ID=SECTAB.SEC_ID) AND (SECTAB.DIV_ID = DIVTAB.DIV_ID)"
      joba1 = "FIELDENTRY.JOB_ID = 1"
      cur.execute(f'''select {vala1} from {taba1} where {joia1} AND {joba1} and date = {d1} GROUP BY SECTAB.DIV_ID''')
      rva1 = cur.fetchall()

      #GL TODAY LAST YEA1R
      vala2 = "SUM(FIELDENTRY.GL_VAL)"
      taba2 = "FIELDENTRY, DIVTAB, SECTAB"
      joia2 = "(FIELDENTRY.SEC_ID=SECTAB.SEC_ID) AND (SECTAB.DIV_ID = DIVTAB.DIV_ID)"
      joba2 = "FIELDENTRY.JOB_ID = 1"
      cur.execute(f'''select {vala2} from {taba2} where {joia2} AND {joba2} and date = {d11} GROUP BY SECTAB.DIV_ID''')
      rva2 = cur.fetchall()

      #FINE LEAF% TODAYS GL
      vala3 = "sum(FL_PER)"
      taba3 = "FLENTRY, DIVTAB"
      joia3 = "(FLENTRY.DIV_ID = DIVTAB.DIV_ID)"
      cur.execute(f'''select {vala3} from {taba3} where {joia3} and date = {d1} GROUP BY DIVTAB.DIV_ID''')
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
      cur.execute(f"SELECT SUM(SORTENTRY.SORT_KG) FROM SORTENTRY WHERE date ={d1} ")
      rv = cur.fetchall()

      #SUM-ALLGRADES-DATE
      cur.execute(f"SELECT SUM(SORTENTRY.SORT_KG) FROM SORTENTRY WHERE date ={d1} ")
      rv3 = cur.fetchall()

      #SUM-PERGRADE-DATERANGE
      cur.execute(f"SELECT SUM(SORTENTRY.SORT_KG) FROM SORTENTRY, TEAGRADETAB WHERE SORTENTRY.TEAGRADE_ID = TEAGRADETAB.TEAGRADE_ID and date ={d1} group by TEAGRADETAB.TEAGRADE_NAME ")
      rv1 = cur.fetchall()

      #PERGRADE-DATE
      cur.execute(f"SELECT SUM(SORTENTRY.SORT_KG) FROM SORTENTRY, TEAGRADETAB WHERE SORTENTRY.TEAGRADE_ID = TEAGRADETAB.TEAGRADE_ID and date ={d1} group by TEAGRADETAB.TEAGRADE_NAME ")
      rv4 = cur.fetchall()      

      #GRADE-NAME
      cur.execute(f"SELECT TEAGRADETAB.TEAGRADE_NAME FROM SORTENTRY, TEAGRADETAB WHERE SORTENTRY.TEAGRADE_ID = TEAGRADETAB.TEAGRADE_ID and date ={d1}group by TEAGRADETAB.TEAGRADE_NAME ")
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

      json_data2 = []    
      column_headers = ['Grade','PercentToday','PercentTodate']

      for row in zzz:
            json_data2.append(dict(zip(column_headers,row)))
      

      json_comp = {} 
      json_comp['TeaMade'] = json_data
      json_comp['Greenleaf'] = json_data1
      json_comp['GradePer'] =json_data2
      return json.dumps(json_comp)