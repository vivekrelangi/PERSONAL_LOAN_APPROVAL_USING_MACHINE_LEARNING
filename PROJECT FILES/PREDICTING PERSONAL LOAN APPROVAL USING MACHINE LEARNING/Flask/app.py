import numpy as np
import pickle
import pandas
import os
from flask import Flask, request, render_template


app = Flask(__name__)#, template_folder='template'
#file = open(r'rdf.pkl','rb')
#model = pickle.load(open(r'rdf.pkl', 'rb'))
model = pickle.load(open(r'gb.pkl', 'rb'))
#model = pickle.load(file)
scale = pickle.load(open(r'scale1.pkl','rb'))

@app.route('/') # rendering the html template
def home():
    return render_template('home.html') #to access the home page.
@app.route('/predict',methods=["POST","GET"]) # rendering the html template
def predict() :
    return render_template("input.html")

@app.route('/submit',methods=["POST","GET"])# route to show the predictions in a web UI
def submit():
    #  reading the inputs given by the user
    input_feature=[int(x) for x in request.form.values() ]  
    #input_feature = np.transpose(input_feature)
    input_feature=[np.array(input_feature)]
    print(input_feature)
    names = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'ApplicantIncome',
       'CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History','Property_Area']
    data = pandas.DataFrame(input_feature,columns=names)
    print(data)
    
    #data_scaled = scale.fit_transform(data)
    #data = pandas.DataFrame(,columns=names)

    

     # predictions using the loaded model file
    prediction=model.predict(data)
    print(prediction)
    prediction = int(prediction)
    print(type(prediction))
   
    if (prediction == 0):
       return render_template("output.html",result ="Loan will not be Approved")
    else:
       return render_template("output.html",result = "Loan will  be Approved")
     # showing the prediction results in a UI
if __name__=="__main__":
    
    app.run(host='0.0.0.0', port=8000,debug=True)    # running the app
    port=int(os.environ.get('PORT',5000))
    app.run(debug=False)
