from fastapi import FastAPI
import joblib
from pydantic import BaseModel, Field
import pandas as pd
from typing import Literal
from fastapi.middleware.cors import CORSMiddleware

model = joblib.load('churn_model.pkl')

card_type_mapping = {
    "DIAMOND": 3,
    "GOLD": 2,
    "PLATINUM": 1,
    "SILVER": 0,
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"]
)


# A first pydentic model
class customer_data(BaseModel):
    creditscore        : int = Field(...,ge = 0,le = 1000)
    age                : int = Field(...,ge= 18, le= 100)
    tenure             : int = Field(...,ge= 0, le= 10)
    balance            : float = Field(...,ge= 0)
    numofproducts      : int = Field(...,ge= 0, le= 5)
    hascrcard          : int = Field(...,ge= 0 ,le= 1)
    isactivemember     : int = Field(...,ge= 0, le= 1)
    estimatedsalary    : float = Field(...,ge= 0 , le= 75000)
    satisfaction_score : int = Field(...,ge= 1, le= 5)
    card_type          : Literal['DIAMOND','GOLD','SILVER','PLATINUM']
    point_earned       : int = Field(...,ge= 0, le= 1000)
    gender             : Literal['Male','Female']
    geography          : Literal['France','Germany','Spain']


class PredictionResponse(BaseModel):
    predicted_result: int
    churn_probability: float
    stay_probability: float


# # Describe What we send back
# class PredictionResponse(BaseModel):
#     predicted_result : int


@app.get('/')
def greet():
    return 'Welcome Churn Predition'

@app.post('/predict' , response_model=PredictionResponse)
def predict(data : customer_data):
    inputs_row = pd.DataFrame([{
        'creditscore'         : data.creditscore,
        'age'                 : data.age,
        'tenure'              : data.tenure,
        'balance'             : data.balance,
        'numofproducts'       : data.numofproducts,
        'hascrcard'           : data.hascrcard,
        'isactivemember'      : data.isactivemember,
        'estimatedsalary'     : data.estimatedsalary,
        'satisfaction_score'  : data.satisfaction_score,
        'card_type'           : card_type_mapping[data.card_type],
        'point_earned'        : data.point_earned,
        'gender'              : data.gender,
        'geography'           : data.geography,
    }])


    # Prediction
    prediction = model.predict(inputs_row)[0]

    # Probability
    probability = model.predict_proba(inputs_row)[0]

    churn_probability = probability[1] * 100
    stay_probability = probability[0] * 100

    return PredictionResponse(
        predicted_result=int(prediction),
        churn_probability=round(churn_probability, 2),
        stay_probability=round(stay_probability, 2)
    )


    # prediction  = model.predict(inputs_row)[0]
    # # churn_probability = probability[1]*100
    # return PredictionResponse(predicted_result = prediction)