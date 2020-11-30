# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import joblib
from matplotlib import pyplot as plt


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

@app.route('/predict',methods=['POST'])
def predict():
    global df
    
    #input_features = [int(x) for x in request.form.values()]
    #features_value = np.array(input_features)
    
    # #validate input hours
    # if input_features[0] <0 or input_features[0] >24:
    #     return render_template('index.html', prediction_text='Please enter valid hours between 1 to 24 if you live on the Earth')
    indians = request.form['indians']
    foreigners = request.form['foreigners']
    indian_male = request.form['indians_male']
    indian_female = request.form['indian_females']
    foreigns_male = request.form['foreigners_male']
    foreigners_female = request.form['foreigners_females']
    other  =  request.form['Others']       
    output = model.predict([[indians,foreigners,indian_male,indian_female,foreigns_male,foreigners_female,other]])[0]

    
    #input and predicted value store in df then save in csv file
    df= pd.concat([df,pd.DataFrame({'Indians':indians,'Foreigners':foreigners,
                                    'Indians male':indian_male,'Indian Females':indian_female,
                                    'Foreigners Male':foreigns_male,'Foreigners Females':foreigners_female,
                                    'Others':other,
                                    'Predicted Output':[output]})],ignore_index=True)
    print(df)   
    df.to_csv('smp_data_from_app.csv')

    return render_template('index.html', prediction_text=f"Cluster : {output} out of 3 "+ f" FOR Indians : {indians}, Foreigners : {foreigners}, Indians male : {indian_male},Indian Females : {indian_female}, Foreigners Male : {foreigns_male}, Foreigners Females : {foreigners_female},Others : {other} ")


if __name__ == "__main__":
    app.run(debug=True)
    
