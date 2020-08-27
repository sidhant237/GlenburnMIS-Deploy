from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
from App import app, mysql
import json, datetime
from dateutil.relativedelta import relativedelta

cur = mysql.connection.cursor()
    
    con = "DivTab.Div_name, SecTab.Sec_Name"
    val = "FieldEntry.Mnd_Val, FieldEntry.GL_Val, FieldEntry.Area_Val"
    fom = "ROUND((GL_Val/Mnd_Val),2), ROUND((GL_Val/Area_Val),2),ROUND((Mnd_Val/Area_Val),2)"
    tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab"
    joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID"
    job = "(FieldEntry.Job_ID = 1 )"
    cur.execute(f'''select {con} , {val} , {fom} from {tab} where {joi} and date ={d1} and {job}''')

    row_headers = ['Division','Section_Name', 'Mandays', 'Greenleaf', 'AreaCovered', 'GlMnd', 'GlHa', 'MndHa']
    rv = cur.fetchall()
    json_data3 = []


    def sids_converter(o):
            if isinstance(o, datetime.date):
                  return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    for result in rv:
            json_data3.append(dict(zip(row_headers , result)))