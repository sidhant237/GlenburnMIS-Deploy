from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
from App import app, mysql
import json, datetime
from dateutil.relativedelta import relativedelta


##################################
#12 FACTORY
@app.route('/test', methods=['GET', 'POST'])
@cross_origin()
def test():      
      d1 = request.args.get("start") 
      if not d1:
            d1 = "2020-08-18"
      d11 = "'" + str((datetime.datetime.strptime(d1, '%Y-%m-%d') - relativedelta(years=1))).split(' ')[0] + "'"
      d01 = "'" + str((datetime.datetime.strptime(d1, '%Y-%m-%d') - relativedelta(days=1))).split(' ')[0] + "'"
      d1 = "'" + d1 + "'"
      d0 = "'2020-01-01'"  # start date current year
      d00 = "'2019-01-01'"  # start date last year
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

      column_headers =  ['TMToday', 'TMToDate', 'TMToDateLY', 'RecoveryToday', 'RecoveryToDate']
      
      json_data = []
      json_data.append(dict(zip(column_headers, rv)))
      return json.dumps (json_data)
