# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 18:21:39 2020

@author: Pragya Sinha
"""

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import logging
import pickle
import warnings
warnings.filterwarnings('ignore')

# initialize logging
LOG_FILE_NAME = 'complaint.txt'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=LOG_FILE_NAME,
                    filemode='w')

# load the saved 
filename='complaint_nb_model.pkl'
model_file = pickle.load(open(filename, 'rb'))


# initialize database
def db_connect():
    db_name = 'complaints.db'
    db_con = sqlite3.connect(db_name)
    logging.info('Connected to ' + db_name)
    db_con.execute("""CREATE TABLE IF NOT EXISTS complaints_info (
                first_name TEXT,
                last_name TEXT,
                city TEXT,
                country TEXT,
                Issue TEXT,
                department TEXT
                )"""
                   )
    return db_con

# function to write data to db
def write_complaint_data(complaints):
    conn = db_connect()
    cur = conn.cursor()
    # execute sql command
    sql = """INSERT INTO complaints_info(first_name,
          last_name,
          city,
          country, 
          Issue,
          department)
          values (?,?,?,?,?,?)"""

    cur.execute(sql, [x for x in complaints])
    print(sql)
    cur.execute("commit")
    refno = cur.lastrowid
    cur.close()
    conn.close()
    logging.info("DB commit successful")
    return refno


# REST API service
app = Flask(__name__)


@app.route('/', methods = ['POST','GET'])
def home():
    return render_template('home.html')


@app.route('/form1.html', methods=['POST', 'GET'])
def complaint_form():
    complaint_status = ""
    if request.method == 'POST':
        complaints = []
        try:
            logging.info("Capturing app data " + request.form['first_name'])
            complaints.append(request.form['first_name'])
            complaints.append(request.form['last_name'])
            complaints.append(request.form['city'])
            complaints.append(request.form['country'])
            complaints.append(request.form['issue'])
            
            department = complaints.append(str(model_file.predict([request.form['issue']])))
            
            
            logging.info(complaints)
            
            pred_complaint = request.form['issue']
            print(pred_complaint)
            
            department = model_file.predict([pred_complaint])
            print(department)
            
            refno = write_complaint_data(complaints)
            
            complaint_status = 'Your complaint with ID [ ' + str(refno) + '] is assigned to  ' + str(department)
            logging.info(complaint_status)
        except:
            complaint_status = 'Error!'
            logging.exception(complaint_status)
    return render_template('form1.html',complaint_status=complaint_status)

if __name__ == '__main__':
    app.run(debug=True)