# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import joblib
from prettytable import PrettyTable



app = Flask(__name__)

model = joblib.load("Population_data_cluster.pkl")

df = pd.DataFrame()

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
# Route for handling the login page logic
@app.route('/login.html', methods=['GET', 'POST'])
def login():

    error = None
    if request.method == 'POST':
        if request.form['username'] != 'popcluster' or request.form['password'] != 'popcluster':
            error = 'Invalid Credentials. Please try again.'
        else:
            return render_template('Tablee.html',)
    return render_template('login.html', error=error)
    
@app.route('/predict',methods=['POST'])
def predict():
    global df
    
    #input_features = [int(x) for x in request.form.values()]
    #features_value = np.array(input_features)
    indians = request.form['indians']
    foreigners = request.form['foreigners']
    indian_male = request.form['indians_male']
    indian_female = request.form['indian_females']
    foreigns_male = request.form['foreigners_male']
    foreigners_female = request.form['foreigners_females']
    other  =  request.form['Others']       
    output = model.predict([[indians,foreigners,indian_male,indian_female,foreigns_male,foreigners_female,other]])[0]
    alert="Submission Successfull Please Scroll Down for results"
    # # #validate input hours
    # if (indians=="" or foreigners=="" or foreigners=="" or indian_male=="" or indian_female=="" or foreigns_male=="" or foreigners_female=="" or other=="" ):
    #     return render_template('index.html', prediction_text='Missing Values : All fields are mandatory to fill')

    

    
    #input and predicted value store in df then save in csv file
    df= pd.concat([df,pd.DataFrame({'Indians':indians,'Foreigners':foreigners,
                                    'Indians male':indian_male,'Indian Females':indian_female,
                                    'Foreigners Male':foreigns_male,'Foreigners Females':foreigners_female,
                                    'Others':other,
                                    'Predicted Output':[output]})],ignore_index=True)
    print(df)   
    df.to_csv('smp_data_from_app.csv')

   
        # open csv file 
    a = open("smp_data_from_app.csv", 'r') 
    
    # read the csv file 
    a = a.readlines() 
    
    # Seperating the Headers 
    l1 = a[0] 
    l1 = l1.split(',') 
    
    # headers for table 
    t = PrettyTable([l1[0],l1[1],l1[2],l1[3],l1[4],l1[5],l1[6],l1[7],l1[8]]) 
    
    # Adding the data 
    for i in range(1, len(a)) : 
        t.add_row(a[i].split(',')) 
    code = t.get_html_string(attributes={"name":"my_table", "class":"red_table", "style":"border:2px solid black"}) 
    html_file = open('templates/Tablee.html', 'w') 
    html_file = html_file.write(code) 




    

    return render_template('index.html', prediction_text=f"Cluster : {output} out of 3"+ f" FOR Indians : {indians}, Foreigners : {foreigners}, Indians male : {indian_male},Indian Females : {indian_female}, Foreigners Male : {foreigns_male}, Foreigners Females : {foreigners_female},Others : {other} ",alert=alert)


if __name__ == "__main__":
    app.run(debug=True)
    
