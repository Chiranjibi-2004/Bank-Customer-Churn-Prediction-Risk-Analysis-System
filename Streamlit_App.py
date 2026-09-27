import os
import streamlit as st
import pandas as pd
import joblib


# Load the trained model 
@st.cache_resource  # this execute the model faster....
def Load_model():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR,'churn_model.pkl')
    print(f"Loding model from --- {MODEL_PATH}")
    return joblib.load(MODEL_PATH)

model = Load_model()

## Create the App body

# Create title and markdowns .....
st.title('Bank Customer Churn Predictior')
st.markdown('''
This application predicts the most likely customer leaving the Bank (churning).
Fill in the details bellow to analyze indivisual risk or upload batch file.

''')

# Create the Sidebar for selection 
mode = st.sidebar.selectbox('Choose Analysis Mode 👇',['Single Customer','Batch Customer (.CSV)'])

# ------ Mode 1: Single Customer -------
if mode == 'Single Customer':
    st.subheader('Enter Customer Details')
        
    # Create Columns
    col1,col2,col3 = st.columns(3)

    with col1 :
        creditscore = st.number_input('Credit Score',min_value=0,max_value=1000,value=650)
        balance = st.number_input('Balance',min_value=0,value=5000,step=1000)
        estimeted_salary = st.number_input('Estimated Salary',min_value=0,value=75000,step=1500)
        
    with col2 :
        age = st.number_input('Age',min_value=18,max_value=100,value=40)
        tenure =st.slider('Tenure (Years)',min_value=0,max_value=10,value=5)
        num_products = st.slider('Number of Products',min_value=0,max_value=5,value=0)

    with col3:
        geography = st.selectbox('Geography',['France','Germany','Spain'])
        gender = st.selectbox('Gender',['Male','Female'])
        card_type = st.selectbox('Card Types',['DIAMOND','GOLD','SILVER','PLATINUM'])

    # Additional Binary matrics
    st.markdown('#### Aditional Information')
    col4,col5,col6 = st.columns(3)

    with col4:
        has_card = st.checkbox('Has Credit Card?',value=False)
    with col5:
        is_active_member = st.checkbox('Is Active Member?',value=False)
        
    with col6:
        satisfaction_score = st.slider('Satisfaction Score',min_value=1,max_value=5,value=3)

    point_earned = st.number_input('Point Earned',min_value=0,max_value=1000,value=500)

    # Convert mapping for Card type to match the training directry
    card_mapping = {'DIAMOND':3,
               'GOLD':2,
               'PLATINUM':1,
               'SILVER':0}


    # Map input data to our training columns
    input_data = pd.DataFrame([{
        'creditscore':creditscore,
        'geography':geography,
        'gender':gender,
        'age':age,
        'tenure':tenure,
        'balance':balance,
        'numofproducts':num_products,
        'hascrcard':1 if has_card else 0,
        'isactivemember':1 if is_active_member else 0,
        'estimatedsalary':estimeted_salary,
        'satisfaction_score':satisfaction_score,
        'card_type':card_mapping[card_type],
        'point_earned':point_earned
    }])

    st.markdown('---')


    # Set Predict button
    if st.button('Predict Churn Risks'):
        # Get Probability outpu from model
        probability = model.predict_proba(input_data)[0]
        churn_probability = probability[1]*100
        # Display Results
        st.subheader('Analysis Result')
        if churn_probability > 50:
            st.error(f'**High Risk**: This customer has a **{churn_probability:.2f}%** chance of leave the Bank.')
        else:
            st.success(f'**Low Risk**: This customer has a **{100 - churn_probability:.2f}%** chance of staying.')


# ------ Mode 2: Batch Customer Prediction -------
elif mode == 'Batch Customer (.CSV)':
    st.subheader('Bulk Prediction Dashboard')
    upload_file=st.file_uploader('Upload the **CSV** file that contain Customer records',type=['csv'])

    if upload_file is not None:
        data = pd.read_csv(upload_file)
        st.write('### Data Preview',data.head())    # Display the raw file data 

    # Generate the Prediction Button
    if st.button('Generate Prediction'):
        # Copy the Data
        clean_batch =data.copy()
        # In raw data if any other column are there drop the columns
        remove_col = ['RowNumber','CustomerId','Surname','Exited','Complain']
        for col in remove_col:
            if col in clean_batch.columns:
                clean_batch = clean_batch.drop(col,axis=1)
        
        # Map the Card Type 
        if 'Card Type' in clean_batch.columns and clean_batch['Card Type'].dtype =='str' :
            card_mapping = {'DIAMOND':3,
               'GOLD':2,
               'PLATINUM':1,
               'SILVER':0}
            clean_batch['Card Type'] = clean_batch['Card Type'].map(card_mapping)

        st.write('#### Cleaned Data',clean_batch.head())
        # Execute the prediction
        prediction = model.predict(clean_batch)
        probability = model.predict_proba(clean_batch)[:,1]

        # Append predictions to the original data
        data['Churn_Prediction'] = prediction
        data['Churn_Probability'] = probability

        st.write('#### Predicted Results/Status',data[['Churn_Prediction','Churn_Probability']].head())

        # Download For the Final Results
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label='Download Predicted data CSV',
            data=csv,
            file_name='Batch_Churn_Prediction.csv'
        )
