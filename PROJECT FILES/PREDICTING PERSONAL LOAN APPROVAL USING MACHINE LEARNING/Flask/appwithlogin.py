from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
#from flask_socketio import SocketIO, emit
import bcrypt
import numpy as np
import pickle
import pandas


app = Flask(__name__)

model = pickle.load(open(r'gb.pkl', 'rb'))
scale = pickle.load(open(r'scale1.pkl','rb'))
app.config['SECRET_KEY']='secretrraa'
app.config['MONGO_DBNAME'] = 'PPLAUML'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/users'
#socketio=SocketIO(app)
#@socketio.on('disconnect')
#def disconnect_user():
#   session.clear()
#session.permanent=False

mongo = PyMongo(app)

@app.route('/')
#session.pop('username',None)
def index():
    #session.clear()
    if 'username' in session:
        #username = session['username']
        return 'You are logged in as ' + session['username'] + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"+"<br>" + "<b><a href = '/home'>click here to go to home page</a></b>"
        #return render_template('home.html')
    #else:
        #return render_template('index.html')
    #return "You are not logged in <br><a href = '/login'>" + "click here to log in</a>"
    return render_template('index.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

#app code here
@app.route('/predict',methods=["POST","GET"]) # rendering the html template
def predict() :
    if 'username' in session:
        #session.pop('username', None)
        return render_template("input.html")
    return render_template('register.html')

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
    print(prediction)
   
    if (prediction == 0):
       return render_template("output.html",result ="Loan will not be Approved")
    else:
       return render_template("output.html",result = "Loan will  be Approved")
     # showing the prediction results in a UI


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)

#session.clear()
#session.pop('username', None)