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
            d1 = "2020-09-15"
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
            glyest = ['/']
      elif rv3[0][0] == 0:
            glyest = ['/']
      else:
            glyest = rv3[0]


      #[TM TODAY] - FOR RECOVERY%
      val = "TMEntry.TM_Val "
      tab = "TMEntry"
      cur.execute(f'''select {val} from {tab} where TM_Date = {d1} ''')
      rv1 = cur.fetchall()
      if not rv1[0][0]:
            tmtoday = ['/']
      elif rv1[0][0] == 0:
            tmtoday = ['/']
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
      if glyest[0] == '/' or tmtoday[0] == '/':
            rv.append('/')
      else:
            rectoday = round((tmtoday[0] / glyest[0])*100,2)
            rv.append(rectoday)

      #RECOVERY% TODAY - APPENDED
      zz = round((xx[0]/yy[0])*100,2)
      rv.append(zz)   

      column_headers =  ['TMToday', 'TMTodate', 'TMTodateLY','Difference', 'RecoveryToday', 'RecoveryTodate']

      json_data = []
      json_data.append(dict(zip(column_headers, rv)))
      



#9## GREENLEAF FACTORY

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
                  x = '/'
            groww.append(x)

      kroww = []
      for x in krow:
            if not x:
                  x = '/'
            kroww.append(x)

      sroww = []
      for x in srow:
            if not x:
                  x = '/'
            sroww.append(x)


      czip = []
      czip.append(groww)  
      czip.append(kroww)
      czip.append(sroww)

      json_data1 = []
      column_headers = ['Division','GLToday','GLTodayLY','GLTodate','GLTodateLY','FineLeaf','FineLeafLY']
      for row in czip:
            json_data1.append(dict(zip(column_headers, row)))


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
                  zz.append('/')
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
      

      json_comp = {} 
      json_comp['TeaMade'] = json_data
      json_comp['Greenleaf'] = json_data1
      json_comp['GradePer'] =json_data5
      return json.dumps(json_comp)