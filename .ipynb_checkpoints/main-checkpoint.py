import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
    OrdinalEncoder
)

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    roc_auc_score
)

# Load Dataset

df = pd.read_csv("./Customer-Churn-Records.csv")

# Drop Unnecessary Columns

df = df.drop(
    ['RowNumber', 'CustomerId', 'Surname', 'Complain'],
    axis=1
)

# Separate Features & Target

X = df.drop('Exited', axis=1)
y = df['Exited']

# Column Groups

# Numerical columns
numerical_cols = [
    'CreditScore',
    'Age',
    'Tenure',
    'Balance',
    'NumOfProducts',
    'EstimatedSalary',
    'Satisfaction Score',
    'Point Earned'
]

# One-hot encoding columns
onehot_cols = [
    'Gender',
    'Geography'
]

# Ordinal column
ordinal_cols = ['Card Type']

# Correct order
card_order = [['SILVER', 'PLATINUM', 'GOLD', 'DIAMOND']]

# Preprocessing

preprocessor = ColumnTransformer(
    transformers=[

        # Scale numerical features
        (
            'num',
            StandardScaler(),
            numerical_cols
        ),

        # One-hot encode categorical features
        (
            'cat',
            OneHotEncoder(drop='first', handle_unknown='ignore'),
            onehot_cols
        ),

        # Ordinal encoding
        (
            'ord',
            OrdinalEncoder(categories=card_order),
            ordinal_cols
        )
    ],

    remainder='passthrough'
)

# Create Pipeline

pipeline = Pipeline(steps=[

    ('preprocessing', preprocessor),

    ('model', RandomForestClassifier(
        random_state=42,
        class_weight='balanced'
    ))
])

# Train Test Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train Model

pipeline.fit(X_train, y_train)

# Predictions

y_pred = pipeline.predict(X_test)

y_prob = pipeline.predict_proba(X_test)[:, 1]

# Evaluation

print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f}")

print("\nClassification Report:\n")

print(classification_report(y_test, y_pred))