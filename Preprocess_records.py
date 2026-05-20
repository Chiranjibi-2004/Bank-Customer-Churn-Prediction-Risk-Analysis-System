import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score

# Loads the data 
df = pd.read_csv('./Customer-Churn-Records.csv')

# drop the near 0 relation column and also drop the Complain column this was the higly corelated column that cause the leakage of predictionn
df = df.drop(['RowNumber','CustomerId','Surname','Complain'],
             axis =1) 

# Handel categorical Columns 
maping = {'DIAMOND':3,
         'GOLD':2,
         'PLATINUM':1,
         'SILVER':0}
df['Card Type'] =  df['Card Type'].map(maping)

ohe=OneHotEncoder()
encoder = ohe.fit_transform(df[['Gender']])
encoded_df = pd.DataFrame(encoder.toarray(),
                           columns=ohe.get_feature_names_out(),
                           index= df[['Gender']].index)

encoder_Geography= ohe.fit_transform(df[['Geography']])
Geography_df= pd.DataFrame(encoder_Geography.toarray(),
                           columns = ohe.get_feature_names_out(),
                           index=df[['Geography']].index)

# Now concat both data frame
df = pd.concat([df,encoded_df,Geography_df],
               axis= 1)
df =df.drop(['Geography','Gender'],
            axis =1)

# Separate the feature and targets
df_copy = df.copy()
feature= df_copy.drop('Exited',axis =1)
target = df_copy['Exited']

# Spliting
feature_train,feature_test,target_train,target_test = train_test_split(
    feature,
    target,
    random_state=42,
    test_size=0.2) # split in 80-20 ratio

# Scalling the Data
# Binary data was already in the form of 0-1 So Scale the Continuous data only 
# We are not scalle the target_train data because it has already in the form of '0' & '1'
s_d = ['CreditScore',
       'Age',
       'Tenure',
       'Balance',
       'NumOfProducts',
       'EstimatedSalary',
       'Satisfaction Score',
       'Card Type',
       'Point Earned']  # selected for scalling that need to scale

scaler = StandardScaler()
# scale your train data
feature_train[s_d] = scaler.fit_transform(feature_train[s_d])
# scale your test data 
feature_test[s_d] = scaler.transform(feature_test[s_d])

# print(feature_train)

# Check the cross-validation
def crossvalscore(model_name,feature,target):
    scores = cross_val_score(
        model_name,
        feature,
        target,
        cv=5,
        scoring='roc_auc'
    )
    return scores.mean()

# Train the model

print("--- LOGISTIC REGRESSION RESULTS ---")
lr_model = LogisticRegression(random_state=42)
lr_model.fit(feature_train, target_train)

lr_preds = lr_model.predict(feature_test)
lr_probs = lr_model.predict_proba(feature_test)[:, 1]

print(f"Accuracy: {accuracy_score(target_test, lr_preds):.4f}")
print(f"ROC-AUC Score: {roc_auc_score(target_test, lr_probs):.4f}")
print(f"Cross_val_score: {crossvalscore(lr_model,feature_train,target_train):.4f}")
print("\nClassification Report:")
print(classification_report(target_test, lr_preds))


print("--- DECESSION TREE CLASSIFIER RESULTS ---")
dts_model = DecisionTreeClassifier(random_state=42,
                                   min_samples_leaf=10,
                                   max_depth=5)
dts_model.fit(feature_train, target_train)

dts_preds = dts_model.predict(feature_test)
dts_probs = dts_model.predict_proba(feature_test)[:, 1]

print(f"Accuracy: {accuracy_score(target_test, dts_preds):.4f}")
print(f"ROC-AUC Score: {roc_auc_score(target_test, dts_probs):.4f}")
print(f"Cross_val_score: {crossvalscore(dts_model,feature_train,target_train):.4f}")
print("\nClassification Report:")
print(classification_report(target_test, dts_preds))


print("--- RANDOM FOREST RESULTS ---")
rf_model = RandomForestClassifier(random_state=42,class_weight='balanced')
rf_model.fit(feature_train, target_train)

rf_preds = rf_model.predict(feature_test)
rf_probs = rf_model.predict_proba(feature_test)[:, 1]

print(f"Accuracy: {accuracy_score(target_test, rf_preds):.4f}")
print(f"ROC-AUC Score: {roc_auc_score(target_test, rf_probs):.4f}")
print(f"Cross_val_score: {crossvalscore(rf_model,feature_train,target_train):.4f}")
print("\nClassification Report:")
print(classification_report(target_test, rf_preds))



# Using GridSearchCV find the best parameters

from sklearn.model_selection import GridSearchCV

print("\n--- TUNING RANDOM FOREST WITH GRIDSEARCHCV ---")

# 1. Define the parameter grid
# We keep it focused so it runs reasonably fast while testing key architectural tweaks
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [5, 8, 12],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [2, 4, 10],
    'class_weight': ['balanced']  # Keeping your balanced setting for class imbalance
}

# 2. Initialize the base model
rf_base = RandomForestClassifier(random_state=42)

# 3. Setup GridSearch with 5-fold cross-validation, optimizing for ROC-AUC
grid_search = GridSearchCV(
    estimator=rf_base, 
    param_grid=param_grid, 
    cv=5, 
    scoring='roc_auc', 
    n_jobs=-1,        # Uses all available CPU cores to speed up training
    verbose=1         # Shows progress text
)

# 4. Fit the grid search to your training data
grid_search.fit(feature_train, target_train)

# 5. Extract the best model and parameters
best_rf_model = grid_search.best_estimator_
print(f"\nBest Hyperparameters Found: {grid_search.best_params_}")

# 6. Evaluate the optimized model on your test set
best_rf_preds = best_rf_model.predict(feature_test)
best_rf_probs = best_rf_model.predict_proba(feature_test)[:, 1]

print("\n--- OPTIMIZED RANDOM FOREST RESULTS ---")
print(f"Accuracy: {accuracy_score(target_test, best_rf_preds):.4f}")
print(f"ROC-AUC Score: {roc_auc_score(target_test, best_rf_probs):.4f}")
print(f"Cross_val_score: {crossvalscore(best_rf_model, feature_train, target_train):.4f}")
print("\nClassification Report:")
print(classification_report(target_test, best_rf_preds))

