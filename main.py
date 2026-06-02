import pandas as pd
from sklearn.model_selection import train_test_split,cross_val_score,GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,roc_auc_score,classification_report

# LOAD DATA
def load_data(path):
    df = pd.read_csv(path)
    return df

# DROP UNNECESSARY COLUMNS
def clean_data(df):
    drop_columns = ['RowNumber',
                    'CustomerId',
                    'Surname',
                    'Complain']
    df = df.drop(columns=drop_columns)
    return df

# CARD TYPE MAPPING
def map_card_type(df):
    mapping = {'DIAMOND':3,
               'GOLD':2,
               'PLATINUM':1,
               'SILVER':0}
    df['Card Type'] = df['Card Type'].map(mapping)
    return df


# SPLIT FEATURES AND TARGET
def separate_feature_target(df):
    X = df.drop('Exited', axis=1)
    y = df['Exited']
    return X, y

# TRAIN TEST SPLIT
def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y)
    return X_train, X_test, y_train, y_test

# CREATE PREPROCESSOR
def create_preprocessor():
    numeric_features = ['CreditScore',
                        'Age',
                        'Tenure',
                        'Balance',
                        'NumOfProducts',
                        'EstimatedSalary',
                        'Satisfaction Score',
                        'Card Type',
                        'Point Earned']
    
    categorical_features = ['Gender',
                            'Geography']

    # Numeric Pipeline
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    # Categorical Pipeline
    categorical_transformer = Pipeline(
        steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder(handle_unknown='ignore'))])

    # Column Transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])
    return preprocessor

# CREATE MODEL PIPELINE
def create_pipeline(model):
    preprocessor = create_preprocessor()
    pipeline = Pipeline(
        steps=[
            ('preprocessor', preprocessor),
            ('model', model)])
    return pipeline


# CROSS VALIDATION
def calculate_cross_validation(model, X_train, y_train):
    scores = cross_val_score(model,
                             X_train,
                             y_train,
                             cv=5,
                             scoring='roc_auc',
                             n_jobs=-1)
    return scores.mean()

# MODEL EVALUATION
def evaluate_model(model, X_train, X_test, y_train, y_test, model_name):
    print(f"--- {model_name} ---")

    # Train
    model.fit(X_train, y_train)

    # Prediction
    y_pred = model.predict(X_test)

    # Probability prediction
    y_prob = model.predict_proba(X_test)[:, 1]

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    cv_score = calculate_cross_validation(model, X_train, y_train)

    # Print Results
    print(f"Accuracy       : {accuracy:.4f}")
    print(f"ROC-AUC Score  : {roc_auc:.4f}")
    print(f"Cross Val Score: {cv_score:.4f}")
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred))

    return model


# GRID SEARCH FOR RANDOM FOREST
def tune_random_forest(X_train, y_train):
    rf_pipeline = create_pipeline(RandomForestClassifier(random_state=42))
    param_grid = {'model__n_estimators': [100, 200],
                  'model__max_depth': [5, 8, 12],
                  'model__min_samples_split': [2, 5, 10],
                  'model__min_samples_leaf': [2, 4, 10],
                  'model__class_weight': ['balanced']}

    grid_search = GridSearchCV(estimator=rf_pipeline,
                               param_grid=param_grid,
                               cv=5,
                               scoring='roc_auc',
                               n_jobs=-1,
                               verbose=1)
    grid_search.fit(X_train, y_train)
    print("\nBest Parameters:")
    print(grid_search.best_params_)
    return grid_search.best_estimator_


# MAIN FUNCTION
def main():
    # Load Data
    df = load_data('./Customer-Churn-Records.csv')

    # Clean Data
    df = clean_data(df)

    # Map Card Type
    df = map_card_type(df)

    # Feature / Target
    X, y = separate_feature_target(df)

    # Train Test Split
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Save Train & Test data 
    train_data = X_train.copy()
    train_data['Exited'] = y_train
    
    test_data = X_test.copy()
    test_data['Exited'] = y_test

    train_data.to_csv('./train.csv',index =False)
    test_data.to_csv('./test.csv',index =False)
    print('train.csv and test.csv saved successfully . ')

    # LOGISTIC REGRESSION
    lr_pipeline = create_pipeline(
        LogisticRegression(random_state=42,max_iter=1000))
    evaluate_model(lr_pipeline,
                   X_train,
                   X_test,
                   y_train,
                   y_test,
                   "LOGISTIC REGRESSION RESULTS")

    # DECISION TREE
    dt_pipeline = create_pipeline(
        DecisionTreeClassifier(random_state=42,
                               max_depth=5,
                               min_samples_leaf=10))
    evaluate_model(dt_pipeline,
                   X_train,
                   X_test,
                   y_train,
                   y_test,
                   "DECISION TREE RESULTS")

    # RANDOM FOREST
    rf_pipeline = create_pipeline(
        RandomForestClassifier(random_state=42,class_weight='balanced'))
    evaluate_model(rf_pipeline,
                   X_train,
                   X_test,
                   y_train,
                   y_test,
                   "RANDOM FOREST RESULTS")

    # GRID SEARCH RANDOM FOREST
    print("\nTUNING RANDOM FOREST...\n")
    best_rf_model = tune_random_forest(X_train, y_train)
    evaluate_model(best_rf_model,
                   X_train,
                   X_test,
                   y_train,
                   y_test,
                   "OPTIMIZED RANDOM FOREST RESULTS")
    


    # SAVE MODEL
    import joblib
    joblib.dump(best_rf_model, 'churn_model.pkl')


if __name__ == "__main__":
    main()

