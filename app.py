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
    return render_template('about.html')

@app.route('/analysis', methods=['GET','POST'])
def analysis():
    if request.method=='POST':
        age = request.form.get('age')
        inc = request.form.get('inc')
        score = request.form.get('score')
        #print(age,inc,score)
        inp=np.array([age,inc,score]).reshape(1,-1)
        pred=load_model.predict(inp)[0]
        #print(pred)
        if pred==0:
            output='Customers with low income & low expenditure'
        elif pred==1:
            output='Customers with high income & high expenditure'
        elif pred==2:
            output='Customers with medium income & medium expenditure'
        elif pred==3:
            output='Customers with high income & low expenditure'
        elif pred==4:
            output='Customers with low income & high expenditure'
        return render_template('analysis.html',output=output)
    return render_template('analysis.html')

@app.route('/results', methods=['GET','POST'])
def result():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)