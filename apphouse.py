
from flask import Flask, render_template, request
import requests
import pickle
import os
import pandas as pd
import numpy as np
import sklearn


app = Flask(__name__)
model = pickle.load(open('C:/Users/HP/deploy_olx_rental/rental_house_pred.pkl','rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('rental_house.html')

@app.route("/predict", methods=['POST'])
def predict():   
    if request.method == 'POST':

        TYPE  = str(request.form['type_'])
        BEDROOMS  = int(request.form['bedrooms'])
        BATHROOMS  = int(request.form['bathrooms'])
        FURNISHING  = str(request.form['furnishing'])
        POSTEDBY  = str(request.form['listed by'])
        TOTALAREA  = int(request.form['super builtup area (ft²)'])
        CARPETAREA = int(request.form['carpet area (ft²)'])
        CARPARKING = int(request.form['car parking'])
        FACING= str(request.form['facing'])
        FLOORNO = int(request.form['floor no'])
        TOTALFLOORS = int(request.form['total floors'])
        MAINTENANCE = int(request.form['maintenance (monthly)'])
        BACHELORS = str(request.form['bachelors allowed'])
        CITY = str(request.form['city'])
        STATE = str(request.form['state'])
        
        print(TYPE, BEDROOMS, BATHROOMS, FURNISHING, POSTEDBY,
       TOTALAREA, CARPETAREA, CARPARKING, FACING, FLOORNO, TOTALFLOORS, MAINTENANCE,
       BACHELORS, CITY, STATE)

        prediction=model.predict(np.array([[TYPE, BEDROOMS, BATHROOMS, FURNISHING, POSTEDBY,
       TOTALAREA, CARPETAREA, BACHELORS, MAINTENANCE, TOTALFLOORS,CARPARKING,FLOORNO,FACING,
        CITY,STATE]]))
        
        output=np.exp(prediction)
        output=round(output[0],1)
        if output<0:
            return render_template('rental_house.html',prediction="Sorry you cannot rent this House")
        else:
            return render_template('rental_house.html',prediction="You can rent the House at ₹ {} ".format(output))
    else:
        return render_template('rental_house.html')

if __name__ == "__main__":
   port = int(os.environ.get('PORT' , 5000))
   app.run(host='0.0.0.0', port=port)

