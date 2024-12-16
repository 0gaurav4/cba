from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import numpy as np
from joblib import load

load_model = load('static\model.pk')

app = Flask(__name__)
app.secret_key = 'supersecretmre'


@app.route('/')
def index():
    flash('Welcome to the Flask App', 'info')
    return render_template('index.html')

@app.route('/about')
def about():
    df = pd.read_csv('WorkData.csv')
    data = df.to_html(classes='table table-striped')
    return render_template('about.html', data=data)

import pandas as pd

@app.route('/analysis', methods=['GET','POST'])
def analysis():
    df = pd.read_csv('WorkData.csv')  # Add the correct path to your CSV file
    if request.method=='POST':
        age = request.form.get('age')
        inc = request.form.get('inc')
        score = request.form.get('score')
        #print(age,inc,score)
        inp=np.array([age,inc,score]).reshape(1,-1)
        pred=load_model.predict(inp)[0]
        #print(pred)
        if pred==0:
            output=f'Customers belongs the group {pred} : [with low income & low expenditure]'
            output1=f"Number of customers in group {pred} are : {df[df.group == 0].shape[0]}"
        elif pred==1:
            output=f'Customers belongs the group {pred} : [with high income & high expenditure]'
            output1=f"Number of customers in group {pred} are : {df[df.group == 1].shape[0]}"
        elif pred==2:
            output=f'Customers belongs the group {pred} : [with medium income & medium expenditure]'
            output1=f"Number of customers in group {pred} are : {df[df.group == 2].shape[0]}"
        elif pred==3:
            output=f'Customers belongs the group {pred} : [with high income & low expenditure]'
            output1=f"Number of customers in group {pred} are : {df[df.group == 3].shape[0]}"
        elif pred==4:
            output=f'Customers belongs the group {pred} : [with low income & medium expenditure]'
            output1=f"Number of customers in group {pred} are : {df[df.group == 4].shape[0]}"
        return render_template('analysis.html',output=output, output1=output1)
    return render_template('analysis.html')

@app.route('/results', methods=['GET','POST'])
def result():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)