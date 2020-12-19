# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import joblib
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

model = joblib.load("Population_data_cluster.pkl")

df = pd.DataFrame()

db = yaml.load(open("db.yaml"))
app.config["MYSQL_HOST"] = db["mysql_host"]
app.config["MYSQL_USER"] = db["mysql_user"]
app.config["MYSQL_PASSWORD"] = db["mysql_password"]
app.config["MYSQL_DB"] = db["mysql_db"]

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/index.html')
def home2():
    return render_template('index.html')
@app.route('/aboutProject.html')
def aboutP():
    return render_template('aboutProject.html')
@app.route('/screenSnaps.html')
def screenSnaps():
    return render_template('screenSnaps.html')
@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/predict',methods=['POST'])
def predict():
    global df
    
    #input_features = [int(x) for x in request.form.values()]
    #features_value = np.array(input_features)
    indians = request.form['indians']
    foreigners = request.form['foreigners']
    indian_male = request.form['indians_male']
    indian_female = request.form['indian_females']
    foreigners_male = request.form['foreigners_male']
    foreigners_female = request.form['foreigners_females']
    other  =  request.form['Others']       
    output = model.predict([[indians,foreigners,indian_male,indian_female,foreigners_male,foreigners_female,other]])[0]
    output+=1
    alert="Submission Successfull Please Scroll Down for results"

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(Indians, Foreigners, Indian_Males, Indian_Females, Foreigner_Males, Foreigner_Females, Others, Cluster) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(indians,foreigners,indian_male,indian_female,foreigners_male,foreigners_female,other,output))
    mysql.connection.commit()
    cur.close()
    # # #validate input hours
    # if (indians=="" or foreigners=="" or foreigners=="" or indian_male=="" or indian_female=="" or foreigns_male=="" or foreigners_female=="" or other=="" ):
    #     return render_template('index.html', prediction_text='Missing Values : All fields are mandatory to fill')

    

    
    #input and predicted value store in df then save in csv file
    df= pd.concat([df,pd.DataFrame({'Indians':indians,'Foreigners':foreigners,
                                    'Indians male':indian_male,'Indian Females':indian_female,
                                    'Foreigners Male':foreigners_male,'Foreigners Females':foreigners_female,
                                    'Others':other,
                                    'Cluster':[output]})],ignore_index=True)
    print(df)   
    df.to_csv('smp_data_from_app.csv')

    
#################################################################################################   

    return render_template('index.html', prediction_text=f"Cluster : {output} out of 3",stat= f" FOR Indians : {indians}, Foreigners : {foreigners}, Indians male : {indian_male},Indian Females : {indian_female}, Foreigners Male : {foreigners_male}, Foreigners Females : {foreigners_female},Others : {other} ",alert=alert)

# Route for handling the login page logic
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    userDetails = cur.fetchall()
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'popcluster' or request.form['password'] != 'popcluster':
            error = 'Invalid Credentials. Please try again.'
        else:
            return render_template('Table.html',userDetails=userDetails)
    return render_template('login.html', error=error)
    

if __name__ == "__main__":
    app.run(debug=True)
    
