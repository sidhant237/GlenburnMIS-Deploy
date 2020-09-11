from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
import json, datetime, os, csv
from App import app, mysql


@app.route('/upload',methods=['POST'])
@cross_origin()
def upload_csv_file():
      cur = mysql.connection.cursor()

      if request.method == "POST":
            file = request.files['file']
            if file:
                  #saving file in the localstorage
                  file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file.filename)
                  file.save(file_path)

            #opening file for writing
            csv_data = csv.reader(open(file_path))
            for row in csv_data:
                  query = f'''INSERT INTO fieldentry (Date, fieldentry.GL_Val, Job_ID, Sec_ID) VALUES ('{str(row[0])}',{int(row[1])},{int(row[2])},{int(row[3])})'''
                  print(query)
                  cur.execute(query)
                  mysql.connection.commit()

            return json.dumps({'message': 'success'}), 200


@app.route('/pluckentry',methods=['POST'])
@cross_origin()
def pluckentry():
      cur = mysql.connection.cursor()

      if request.method == "POST":
            file = request.files['file']
            if file:
                  #saving file in the localstorage
                  file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file.filename)
                  file.save(file_path)

            #opening file for writing
            csv_data = csv.reader(open(file_path))
            for row in csv_data:
                  query = f'''Insert Into FieldEntry (Date,Job_ID,Sec_ID,Squ_ID,Mnd_Val,Area_Val,GL_Val,Pluck_Int) Values ('{str(row[0])}',{int(row[1])},{int(row[2])},{int(row[3])},{float(row[4])},{float(row[5])},{int(row[6])},{int(row[7])})'''
                  print(query)
                  cur.execute(query)
                  mysql.connection.commit()

            return json.dumps({'message': 'success'}), 200


@app.route('/cultentry',methods=['POST'])
@cross_origin()
def cultentry():
      cur = mysql.connection.cursor()

      if request.method == "POST":
            file = request.files['file']
            if file:
                  #saving file in the localstorage
                  file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file.filename)
                  file.save(file_path)

            #opening file for writing
            csv_data = csv.reader(open(file_path))
            for row in csv_data:
                  query = f'''INSERT INTO FieldEntry (FieldEntry.Date, FieldEntry.GL_Val, FieldEntry.Job_ID, FieldEntry.Sec_ID) VALUES ('{str(row[0])}',{int(row[1])},{int(row[2])},{int(row[3])})'''
                  #query = f'''Insert Into FieldEntry (Date,Job_ID,Sec_ID,Squ_ID,Mnd_Val,Area_Val) Values ('{str(row[0])}',{int(row[1])},{int(row[2])},{int(row[3])},{int(row[4])},{float(row[5])})'''
                  print(query)
                  cur.execute(query)
                  mysql.connection.commit()

            return json.dumps({'message': 'success'}), 200


@app.route('/jobentry',methods=['POST'])
@cross_origin()
def jobentry():
      cur = mysql.connection.cursor()

      if request.method == "POST":
            file = request.files['file']
            if file:
                  #saving file in the localstorage
                  file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file.filename)
                  file.save(file_path)

            #opening file for writing
            csv_data = csv.reader(open(file_path))
            for row in csv_data:
                  query = f'''Insert Into FieldEntry (Date,Job_ID,Mnd_Val) Values ('{str(row[0])}',{int(row[1])},{int(row[2])})'''
                  print(query)
                  cur.execute(query)
                  mysql.connection.commit()

            return json.dumps({'message': 'success'}), 200


@app.route('/tmentry',methods=['POST'])
@cross_origin()
def tmentry():
      cur = mysql.connection.cursor()

      if request.method == "POST":
            file = request.files['file']
            if file:
                  #saving file in the localstorage
                  file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file.filename)
                  file.save(file_path)

            #opening file for writing
            csv_data = csv.reader(open(file_path))
            for row in csv_data:
                  query = f'''Insert Into TMEntry (TM_Date,TM_Val) Values ('{str(row[0])}',{int(row[1])})'''
                  print(query)
                  cur.execute(query)
                  mysql.connection.commit()

            return json.dumps({'message': 'success'}), 200


@app.route('/fuelentry',methods=['POST'])
@cross_origin()
def fuelentry():
      cur = mysql.connection.cursor()

      if request.method == "POST":
            file = request.files['file']
            if file:
                  #saving file in the localstorage
                  file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file.filename)
                  file.save(file_path)

            #opening file for writing
            csv_data = csv.reader(open(file_path))
            for row in csv_data:
                  query = f'''Insert Into FuelEntry (Date, Fuel_ID, Mach_ID, Fuel_Val) Values ('{str(row[0])}',{int(row[1])},{int(row[2])},{int(row[3])})'''
                  print(query)
                  cur.execute(query)
                  mysql.connection.commit()

            return json.dumps({'message': 'success'}), 200



@app.route('/sortentry',methods=['POST'])
@cross_origin()
def sortentry():
      cur = mysql.connection.cursor()

      if request.method == "POST":
            file = request.files['file']
            if file:
                  #saving file in the localstorage
                  file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file.filename)
                  file.save(file_path)

            #opening file for writing
            csv_data = csv.reader(open(file_path))
            for row in csv_data:
                  query = f'''Insert Into SortEntry (Date,TeaGrade_ID,Sort_Kg) Values ('{str(row[0])}',{int(row[1])},{int(row[2])})'''
                  print(query)
                  cur.execute(query)
                  mysql.connection.commit()

            return json.dumps({'message': 'success'}), 200


@app.route('/flentry',methods=['POST'])
@cross_origin()
def flentry():
      cur = mysql.connection.cursor()

      if request.method == "POST":
            file = request.files['file']
            if file:
                  #saving file in the localstorage
                  file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file.filename)
                  file.save(file_path)

            #opening file for writing
            csv_data = csv.reader(open(file_path))
            for row in csv_data:
                  query = f'''Insert Into FLEntry (Date,Div_ID,FL_Per) Values ('{str(row[0])}',{int(row[1])},{int(row[2])})'''
                  print(query)
                  cur.execute(query)
                  mysql.connection.commit()

            return json.dumps({'message': 'success'}), 200





@app.route('/update-date',methods=['GET', 'POST'])
@cross_origin()
def update_dates():
    date = "'" + (str(request.args.get("date"))) + "'"
    cur = mysql.connection.cursor()
    cur.execute(f'''UPDATE Dates SET Date={date}''')
    mysql.connection.commit()

    return json.dumps({'message': 'success'})




if __name__ == "__main__":
    app.run(debug=True)


##FUELENTRY - 
#query = f'''INSERT INTO fuelentry (Date, Fuel_ID, Mach_ID, Fuel_Val) VALUES ('{str(row[0])}',{int(row[1])},{int(row[2])},{int(row[3])})'''

#FIELDENTRY - WITHOUT PLUCK/CULT (DATE/JOB/MND)
#query = f'''INSERT INTO FIELDENTRY (Date, Job_ID, Mnd_Val) VALUES ('{str(row[0])}',{int(row[1])},{int(row[2])})'''
################
#PluckEntry
#query = f'''Insert Into FieldEntry (Date,Job_ID,Sec_ID,Squ_ID,Mnd_Val,Area_Val,GL_Val,Pluck_Int) Values ('{str(row[0])}',{int(row[1])},{int(row[2])},{int(row[3])},{int(row[4])},{int(row[5])},{int(row[6])},{int(row[7])},{int(row[8])})'''

#CultEntry
#query = f'''Insert Into FieldEntry (Date,Job_ID,Sec_ID,Squ_ID,Mnd_Val,Area_Val) Values ('{str(row[0])}',{int(row[1])},{int(row[2])},{int(row[3])},{int(row[4])},{int(row[5])},{int(row[6])})'''

#JobEntry
#query = f'''Insert Into FieldEntry (Date,Job_ID,Mnd_Val) Values ('{str(row[0])}',{int(row[1])},{int(row[2])})'''

#TMEntry
#query = f'''Insert Into TMEntry (TM_Date,TM_Val) Values ('{str(row[0])}',{int(row[1])})'''

#FuelEntry
#query = f'''Insert Into fuelentry (Date, Fuel_ID, Mach_ID, Fuel_Val) Values ('{str(row[0])}',{int(row[1])},{int(row[2])},{int(row[3])})'''

#Sort Entry
#query = f'''Insert Into SortEntry (Date,TeaGrade_ID,Sort_Kg) Values ('{str(row[0])}',{int(row[1])},{int(row[2])})'''

#FL Entry
#query = f'''Insert Into FLEntry (Date,Div_ID,FL_Per) Values ('{str(row[0])}',{int(row[1])},{int(row[2])})'''