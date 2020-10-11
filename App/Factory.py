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
      d1 = request.args.get("start") 
      if not d1:
            d1 = "2020-10-05"
      d11 = "'" + str((datetime.datetime.strptime(d1, '%Y-%m-%d') - relativedelta(years=1))).split(' ')[0] + "'"
      d01 = "'" + str((datetime.datetime.strptime(d1, '%Y-%m-%d') - relativedelta(days=1))).split(' ')[0] + "'"
      #     d11 = "'2020-08-22'"
      d1 = "'" + d1 + "'"
      d0 = "'2020-01-01'"  # start date current year
      d00 = "'2019-01-01'"  # start date last year
      cur = mysql.connection.cursor()
           
     
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
      cur1 = a[0][0]
      rv.append(cur1)
      
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

      # [TM TODATE] -- For difference
      val1 = "sum(TMEntry.TM_Val)"
      tab1 = "TMEntry"
      cur.execute(f'''select {val1} from {tab1} where TM_Date >= {d0} AND TM_Date <= {d1} ''')
      rv8 = cur.fetchall()

      # [TM TODATE LAST YEAR] -- For difference
      val2 = "sum(TMEntry.TM_Val)"
      tab2 = "TMEntry"
      cur.execute(f'''select {val2} from {tab2} where TM_Date >= {d00} AND TM_Date <= {d11} ''')
      rv9 = cur.fetchall()

      a = [i[0] for i in rv8]
      b = [i[0] for i in rv9]
      c = a[0] - b[0]
      rv.append(c)

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

      if not x:
            x = [0]
      if not xx:
            xx = [0]
      if not y:
            y = [0]
      if not yy:
            yy = [0]

      #[Recovery today]
      z = round((x[0] / y[0])*100,2)
      rv.append(z)

      zz = round((xx[0]/yy[0])*100,2)
      rv.append(zz) 

      column_headers =  ['TMToday', 'TMTodate', 'TMTodateLY','Difference', 'RecoveryToday', 'RecoveryTodate']
      
      json_data = []
      json_data.append(dict(zip(column_headers, rv)))
      



#9## GREENLEAF FACTORY

      cur = mysql.connection.cursor()
      
      #DIV NAME
      val = "DivTab.Div_name"
      tab = "DivTab, SecTab, FieldEntry"
      joi = "(FieldEntry.Sec_ID=SecTab.Sec_ID) AND (SecTab.Div_ID = DivTab.Div_ID)"
      job = "FieldEntry.Job_ID = 1"
      cur.execute(f'''select {val} from {tab} where {joi} AND {job}  GROUP BY SecTab.Div_ID''')#and date = {d1}
      rv = cur.fetchall()
     

      # GL TODAY
      val1 = "SUM(FieldEntry.GL_Val)"
      tab1 = "DivTab, SecTab, FieldEntry"
      joi1 = "(FieldEntry.Sec_ID=SecTab.Sec_ID) AND (SecTab.Div_ID = DivTab.Div_ID)"
      job1 = "FieldEntry.Job_ID = 1"
      cur.execute(f'''select {val1} from {tab1} where {joi1} AND {job1} and date = {d1} GROUP BY SecTab.Div_ID ORDER BY DivTab.Div_ID ASC''')
      rv1 = cur.fetchall()
      

      #GL TODAY LAST YEA1R
      val2 = "sum(FieldEntry.GL_Val)"
      tab2 = "FieldEntry, DivTab, SecTab"
      joi2 = "(FieldEntry.Sec_ID=SecTab.Sec_ID) AND (SecTab.Div_ID = DivTab.Div_ID)"
      job2 = "FieldEntry.Job_ID = 1"
      cur.execute(f'''select {val2} from {tab2} where {joi2} AND {job2} and Date = {d11} GROUP BY SecTab.Div_ID ORDER BY DivTab.Div_ID ASC''')
      rv2 = cur.fetchall()
      

      # GL TODATE
      val1 = "SUM(FieldEntry.GL_Val)"
      tab1 = "DivTab, SecTab, FieldEntry"
      joi1 = "(FieldEntry.Sec_ID=SecTab.Sec_ID) AND (SecTab.Div_ID = DivTab.Div_ID)"
      job1 = "FieldEntry.Job_ID = 1"
      cur.execute(f'''select {val1} from {tab1} where {joi1} AND {job1} and Date >= {d0} and Date <= {d1} GROUP BY SecTab.Div_ID ORDER BY DivTab.Div_ID ASC''')
      rv4 = cur.fetchall()
      

      #GL TODATE LAST YEA1R
      val2 = "sum(FieldEntry.GL_Val)"
      tab2 = "FieldEntry, DivTab, SecTab"
      joi2 = "(FieldEntry.Sec_ID=SecTab.Sec_ID) AND (SecTab.Div_ID = DivTab.Div_ID)"
      job2 = "FieldEntry.Job_ID = 1"
      cur.execute(f'''select {val2} from {tab2} where {joi2} AND {job2} and Date >= {d00} and Date <= {d11} GROUP BY DivTab.Div_ID ORDER BY DivTab.Div_ID ASC''')
      rv5 = cur.fetchall()
      
      
      #FINE LEAF% TODAYS GL
      val3 = "sum(FL_Per)"
      tab3 = "FLEntry, DivTab"
      joi3 = "(FLEntry.Div_ID = DivTab.Div_ID)"
      cur.execute(f'''select {val3} from {tab3} where {joi3} and Date = {d1} GROUP BY DivTab.Div_ID''')
      rv3 = cur.fetchall()
      

      #FINE LEAF% GL LY
      val3 = "sum(FL_Per)"
      tab3 = "FLEntry, DivTab"
      joi3 = "(FLEntry.Div_ID = DivTab.Div_ID)"
      cur.execute(f'''select {val3} from {tab3} where {joi3} and Date = {d11} GROUP BY DivTab.Div_ID''')
      rv6 = cur.fetchall()
      

      w = [i[0] for i in rv]
      x = [i1[0] for i1 in rv1]
      y = [i2[0] for i2 in rv2]
      z = [i3[0] for i3 in rv3]
      a = [i3[0] for i3 in rv4]
      b = [i3[0] for i3 in rv5]
      c = [i3[0] for i3 in rv6] 
      
      #if not w:
      #      w = [0]
      #if not x:
      #      x = [0,0,0]
      #if not y:
      #      y = [0,0,0]
      #if not z:
      #      z = [0,0,0]
      #if not c:
      #      c = [0,0,0]

      q = zip(w,x,y,a,b,z,c)
      json_data1 = []
      #column_headers = ['Division','GLToday','GLTodayLY','GLTodate','GLTodateLY','FineLeaf','FineLeafLY']

      #for row in q:
      #      json_data1.append(dict(zip(column_headers, row)))

      column_headers = ['1','2','3']
      json_data1.append(dict(zip(column_headers,rv6)))


#10## GRADE PER FACTORY

      cur = mysql.connection.cursor()

      #SUM-ALLGRADES-TODATE
      cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry WHERE date >= {d0} and date <={d1} ")
      rv = cur.fetchall()

            #SUM-ALLGRADES-DATE
      cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry WHERE date ={d1} ")
      rv3 = cur.fetchall()

            #SUM-PERGRADE-DATERANGE
      cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date >= {d0} and date <={d1} group by TeaGradeTab.TeaGrade_ID")
      rv1 = cur.fetchall()

            #PERGRADE-DATE
      cur.execute(f"SELECT SUM(SortEntry.Sort_Kg) FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID and date ={d1} group by TeaGradeTab.TeaGrade_ID ")
      rv4 = cur.fetchall()      

            #GRADE-NAME
      cur.execute(f"SELECT TeaGradeTab.TeaGrade_Name FROM SortEntry, TeaGradeTab WHERE SortEntry.TeaGrade_ID = TeaGradeTab.TeaGrade_ID ")#and date ={d1}
      rv2 = cur.fetchall()

      x = [s[0] for s in rv]
      xx = [s[0] for s in rv3]
      y = [i[0] for i in rv1]
      yy = [h[0] for h in rv4]
      w = [str(u[0]) for u in rv2]

      z = []
      for number in y:
            z.append(round(((number / x[0])*100),2))

      zz = []
      for number in yy:
            zz.append(round(((number / xx[0])*100),2))

      if not zz:
            zz = [0,0,0,0,0,0,0]

      zzz = zip(w,zz,z)

      json_data5 = []    
      column_headers = ['Grade','PercentToday','PercentTodate']

      for row in zzz:
            json_data5.append(dict(zip(column_headers,row)))
      

      json_comp = {} 
      #json_comp['TeaMade'] = json_data
      json_comp['Greenleaf'] = json_data1
      #json_comp['GradePer'] =json_data5
      return json.dumps(json_comp)