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
                  query = f'''INSERT INTO fuelentry (Date, Fuel_ID, Mach_ID, Fuel_Val) VALUES ('{str(row[0])}',{int(row[1])},{int(row[2])},{int(row[3])})'''
                  print(query)
                  cur.execute(query)
                  mysql.connection.commit()

            return json.dumps({'message': 'success'}), 200

if __name__ == "__main__":
    app.run(debug=True)





##FUELENTRY - 
#query = f'''INSERT INTO fuelentry (Date, Fuel_ID, Mach_ID, Fuel_Val) VALUES ('{str(row[0])}',{int(row[1])},{int(row[2])},{int(row[3])})'''

#FIELDENTRY - WITHOUT PLUCK/CULT (DATE/JOB/MND)
#query = f'''INSERT INTO FIELDENTRY (Date, Job_ID, Mnd_Val) VALUES ('{str(row[0])}',{int(row[1])},{int(row[2])})'''

