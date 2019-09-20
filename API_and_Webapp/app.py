from flask import Flask, abort, jsonify, request, render_template
from sklearn.externals import joblib
import numpy as np
import pandas as pd
import json

resale_predictor = joblib.load('resale_value_predictor.pkl')


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api',methods=['POST'])
def get_delay():
    result=request.form

    user_input = {'Milage': int(result['Milage']),
                  'Year': int(result['Year']),
                  'Model': result['Model'], 
                  'Fuel': result['Fuel']  
                 }

    print(user_input)
    
    user_df = pd.DataFrame(user_input,index=[0])
    dummy_df = pd.read_csv("dummy_data.csv")
    cols_to_transform = ['Model','Fuel']
    col_list = dummy_df.columns


    user_df = pd.get_dummies(columns=cols_to_transform, data=user_df, prefix_sep="_")
    dummy_df, user_df = dummy_df.align(user_df,join='outer',axis=1)
    user_df = user_df[col_list]
    user_df.fillna(0,inplace=True)
    print(user_df.shape)
    prediction = resale_predictor.predict(user_df)
    print(prediction)

    return json.dumps({'resale_value': int(prediction[0])});
    # return render_template('result.html',prediction=price_pred)

if __name__ == '__main__':
    app.run(port=8080, debug=True)






