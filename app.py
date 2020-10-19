import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
from SendEmail.sendEmail import EmailSender
from config_reader import ConfigReader
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    #int_features = [22582, 2, 170, 90.0, 120, 80, 1, 1, 1, 1, 1, 31]
    i = 0
    myList = []
    for x in request.form.values():
        if i == 0:
            name = x
        elif i == 1:
            email = x
        else:
            myList.append(x)
        i=i+1


    int_features = [int(x) for x in myList]
    int_features[0] = int_features[0]*365
    data = int_features[3] / (int_features[2] / 100) ** 2
    int_features.append(data)
    final_features = pd.DataFrame([int_features])
    prediction = model.predict(final_features)
    email_sender = EmailSender()

    email_file = open("email-templates/email-template-district.html", "r")
    email_message = email_file.read()
    if prediction[0] == 0:
        email_pred = "Hey! you are healthy. keep going on..Check your email for more information"
    else:
        email_pred = "Hey! you are more likely to have a cardio vascular outbreak. Take care. Check your email or the below link for more information"
    email_sender.sendEmailDistrict(name, email, email_message, email_pred)
    if prediction[0] == 0:
        return render_template('index.html',
                               prediction_text='Hey! you seem not to have any cardio issues. you are healthy!. keep going on..')



    return render_template('index.html', prediction_text='Hey! you are more likely to have a cardio vascular outbreak. Take care of your health. For more details about the disease check the below link or your email')


if __name__ == "__main__":
    #port = int(os.getenv('PORT', 5000))
    #print("Starting app on port %d" % port)
    app.run(debug=True)#, port=5000, host='0.0.0.0')
   #app.run(host='0.0.0.0', port=8080)
    #app.run(debug=True)
