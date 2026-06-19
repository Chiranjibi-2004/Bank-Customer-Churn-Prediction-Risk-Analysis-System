import pandas as pd
import joblib

# Load the model 
model = joblib.load('churn_model.pkl')

# Load the test Data
def Load_New_Data(data_path):
    new_data =pd.read_csv(data_path)
    return new_data

data = Load_New_Data('test.csv')

new_data = data.drop('Exited',axis=1)

# Predict and probability of data 
prediction = model.predict(new_data)
# print(prediction)
probability = model.predict_proba(new_data)[:,1]
# print(probability)

# save to a csv file 
data['Prediction'] = prediction
data['Probability'] = probability

data.to_csv('Predicted_data.csv',index =False)
print('File saved as ---- Predicted_data.csv')