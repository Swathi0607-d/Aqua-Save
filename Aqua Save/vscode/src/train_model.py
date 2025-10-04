import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

base = os.path.join(os.path.dirname(__file__), '..')
proc_path = os.path.join(base, 'data', 'processed_water.csv')
models_dir = os.path.join(base, 'models')
os.makedirs(models_dir, exist_ok=True)

 # Load
df = pd.read_csv(proc_path, parse_dates=['date'])

 # Encode household id
df['household_code'] = df['household_id'].astype('category').cat.codes
features = ['household_code', 'household_size', 'day', 'month','day_of_week', 'is_weekend']
target = 'water_liters'

 # Time-based split (80% earliest dates train)
cutoff = df['date'].quantile(0.8)
train = df[df['date'] <= cutoff]
test = df[df['date'] > cutoff]
X_train = train[features]
y_train = train[target]
X_test = test[features]
y_test = test[target]

 # Linear Regression (fast)
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

 # Small RandomForest (Green-AI)
rf = RandomForestRegressor(n_estimators=50, max_depth=8, n_jobs=2,random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

def metrics(y_true, y_pred):
    return {
        'MAE': mean_absolute_error(y_true, y_pred),
        'RMSE': mean_squared_error(y_true, y_pred) ** 0.5,
        'R2': r2_score(y_true, y_pred)
    }
        
print('LR metrics', metrics(y_test, y_pred_lr))
print('RF metrics', metrics(y_test, y_pred_rf))

 # Save models
joblib.dump(lr, os.path.join(models_dir, 'lr_model.joblib'))
joblib.dump(rf, os.path.join(models_dir, 'rf_model.joblib'))
print('Saved models to', models_dir)