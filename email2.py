from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
from App import app, mysql, mail
import json, datetime
from flask_mail import Message
import pandas as pd
from dateutil.relativedelta import relativedelta


@app.template_filter('total')
def total(data, column):
    total = 0
    print(data)
    for item in data:
        total += item[column]
    return total

#9m
@app.route('/testemail', methods=['GET', 'POST'])
@cross_origin()
def email():
    d1 = request.args.get("start")
    email_data, current_date = email_report(d1)
    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.year) + str("/") + str(o.month) + str("/") + str(o.day)

    send_mail(email_data, current_date)
    return json.dumps({'message': 'success'})


def email_report(d1):
    cur = mysql.connection.cursor()
    d1 = "'2020-08-24'"
    d2 = "'2020-08-30'"

    # UP LIMIT
    con = "ROUND((sum(GL_Val)/sum(Mnd_Val)),1)"
    tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab,PruneTab"
    joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID AND PruneTab.Prune_Type = SecTab.Prune_Type"
    job = "(FieldEntry.Job_ID = 1 )"
    cur.execute(f'''select {con} from {tab} where {joi} and date >= {d1} AND date <= {d2} and {job} and SecTab.Prune_Type = 1''')
    rv = cur.fetchall()[0][0]
    uplimit = (rv * .8)

    # DS LIMIT
    con = "ROUND((sum(GL_Val)/sum(Mnd_Val)),1)"
    tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab,PruneTab"
    joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID AND PruneTab.Prune_Type = SecTab.Prune_Type"
    job = "(FieldEntry.Job_ID = 1 )"
    cur.execute(f'''select {con} from {tab} where {joi} and date >= {d1} AND date <= {d2} and {job} and SecTab.Prune_Type = 2''')
    rv = cur.fetchall()[0][0]
    dslimit = (rv * .8)

    # CA LIMIT
    con = "ROUND((sum(GL_Val)/sum(Mnd_Val)),1)"
    tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab,PruneTab"
    joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID AND PruneTab.Prune_Type = SecTab.Prune_Type"
    job = "(FieldEntry.Job_ID = 1 )"
    cur.execute(f'''select {con} from {tab} where {joi} and date >= {d1} AND date <= {d2} and {job} and SecTab.Prune_Type = 3''')
    rv = cur.fetchall()[0][0]
    calimit = (rv * .8)
    
    #UP OUTLIER
    con = "PruneTab.Prune_Name, SecTab.Sec_Name"
    val = "FieldEntry.Mnd_Val, FieldEntry.GL_Val, FieldEntry.Area_Val"
    fom = "ROUND((GL_Val/Mnd_Val),1), ROUND((GL_Val/Area_Val),1),ROUND((Mnd_Val/Area_Val),1)"
    con2 = "FieldEntry.Pluck_Int"
    tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab,PruneTab"
    joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID AND PruneTab.Prune_Type = SecTab.Prune_Type"
    job = "(FieldEntry.Job_ID = 1 )"
    cur.execute(f'''select {con} , {val} , {fom} ,{con2} from {tab} where {joi} and date= {d1} and ROUND((GL_Val/Mnd_Val),1) <= {uplimit}  and {job} and SecTab.Prune_Type = 1''')
    row_headers = ['Prune','Section_Name', 'Mandays', 'Greenleaf', 'AreaCovered', 'GlMnd', 'GlHa', 'MndHa','PluckInt']
    rv1 = cur.fetchall()
    upoutlier = []
    for result in rv1:
        upoutlier.append(dict(zip(row_headers , result)))

    #DS OUTLIER
    con = "PruneTab.Prune_Name, SecTab.Sec_Name"
    val = "FieldEntry.Mnd_Val, FieldEntry.GL_Val, FieldEntry.Area_Val"
    fom = "ROUND((GL_Val/Mnd_Val),1), ROUND((GL_Val/Area_Val),1),ROUND((Mnd_Val/Area_Val),1)"
    con2 = "FieldEntry.Pluck_Int"
    tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab,PruneTab"
    joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID AND PruneTab.Prune_Type = SecTab.Prune_Type"
    job = "(FieldEntry.Job_ID = 1 )"
    cur.execute(f'''select {con} , {val} , {fom} ,{con2} from {tab} where {joi} and date= {d1} and ROUND((GL_Val/Mnd_Val),1) <= {dslimit}  and {job} and SecTab.Prune_Type = 2''')
    row_headers = ['Prune','Section_Name', 'Mandays', 'Greenleaf', 'AreaCovered', 'GlMnd', 'GlHa', 'MndHa','PluckInt']
    rv1 = cur.fetchall()
    dsoutlier = []
    for result in rv1:
        dsoutlier.append(dict(zip(row_headers , result)))

    #CA OUTLIER
    con = "PruneTab.Prune_Name, SecTab.Sec_Name"
    val = "FieldEntry.Mnd_Val, FieldEntry.GL_Val, FieldEntry.Area_Val"
    fom = "ROUND((GL_Val/Mnd_Val),1), ROUND((GL_Val/Area_Val),1),ROUND((Mnd_Val/Area_Val),1)"
    con2 = "FieldEntry.Pluck_Int"
    tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab,PruneTab"
    joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID AND PruneTab.Prune_Type = SecTab.Prune_Type"
    job = "(FieldEntry.Job_ID = 1 )"
    cur.execute(f'''select {con} , {val} , {fom} ,{con2} from {tab} where {joi} and date= {d1} and ROUND((GL_Val/Mnd_Val),1) <= {calimit}  and {job} and SecTab.Prune_Type = 3''')
    row_headers = ['Prune','Section_Name', 'Mandays', 'Greenleaf', 'AreaCovered', 'GlMnd', 'GlHa', 'MndHa','PluckInt']
    rv1 = cur.fetchall()
    caoutlier = []
    for result in rv1:
        caoutlier.append(dict(zip(row_headers , result)))

    #ALL
    con = "PruneTab.Prune_Name, SecTab.Sec_Name"
    val = "FieldEntry.Mnd_Val, FieldEntry.GL_Val, FieldEntry.Area_Val"
    fom = "ROUND((GL_Val/Mnd_Val),1), ROUND((GL_Val/Area_Val),1),ROUND((Mnd_Val/Area_Val),1)"
    con2 = "FieldEntry.Pluck_Int"
    tab = "FieldEntry,SquTab,Jobtab,SecTab,DivTab,PruneTab"
    joi = "FieldEntry.Squ_ID = SquTab.Squ_ID AND FieldEntry.Job_ID=Jobtab.Job_ID AND FieldEntry.Sec_ID=SecTab.Sec_ID AND DivTab.Div_ID=SecTab.Div_ID AND PruneTab.Prune_Type = SecTab.Prune_Type"
    job = "(FieldEntry.Job_ID = 1 )"
    cur.execute(f'''select {con} , {val} , {fom} ,{con2} from {tab} where {joi} and date= {d1} and {job} ORDER BY SecTab.Prune_Type DESC, (GL_Val/Area_Val) DESC ''')

    row_headers = ['Prune','Section_Name', 'Mandays', 'Greenleaf', 'AreaCovered', 'GlMnd', 'GlHa', 'MndHa','PluckInt']
    rv = cur.fetchall()
    json_data3 = []

    def sids_converter(o):
        if isinstance(o, datetime.date):
                return str(o.month) + str("/") + str(o.day)

    for result in rv:
        json_data3.append(dict(zip(row_headers , result)))
    
    returndata = {}
    returndata['All'] = json_data3
    returndata['UPOutlier'] = upoutlier
    returndata['DSOutlier'] = dsoutlier
    returndata['CAOutlier'] = caoutlier

    return returndata, d1




def send_mail(email_data, current_date):
    current_date = datetime.datetime.strptime(current_date[1:11], '%Y-%m-%d')
    subject = "Garden Report " + current_date.strftime('%b %d %Y') 
    #recipients = ['spteaplanter@gmail.com','anshuman239@gmail.com','palzolama@gmail.com','alokeroytea@gmail.com','glenburn1859@yahoo.co.in','sidhant237@gmail.com'] # 'sidhant237@gmail.com' 
    recipients = ['sidhant237@gmail.com']
    body = "Good Day, \n\n Your Daily report file is here. \n\n Thank you."
    msg = Message(subject=subject, body=body, recipients=recipients, sender="from@example.com")
    msg.html = render_template('index2.html', data = email_data, date=current_date)
 
    return mail.send(msg)