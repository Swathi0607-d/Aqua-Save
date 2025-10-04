import numpy as np
import pandas as pd
import os

os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'data'),exist_ok=True)

def generate_synthetic(n_households=12, start='2023-01-01', end='2023-12-31',seed=42):
    
    np.random.seed(seed)
    dates = pd.date_range(start, end, freq='D')
    rows = []
    for h in range(1, n_households+1):
        base = np.random.uniform(80, 260) # baseline liters per person
        household_size = np.random.randint(1, 6)
        seasonal_strength = np.random.uniform(0.03, 0.20)
        for d in dates:
            dow = d.weekday()
            weekend = 1.1 if dow >= 5 else 1.0
            month = d.month
            season = 1.15 if month in [5,6,7,8,9] else 1.0
            temp_effect = 1 + seasonal_strength *(np.sin(2*np.pi*(d.timetuple().tm_yday)/365))
            noise = np.random.normal(0, 12)
            usage = max(10, base * household_size/3 * weekend * season *temp_effect + noise)
            rows.append({
                'date': d,
                'household_id': f'H{h:03d}',
                'household_size': household_size,
                'water_liters': round(usage, 2)
            })
    df = pd.DataFrame(rows)
    out = os.path.join(os.path.dirname(__file__), '..', 'data','sample_water.csv')
    df.to_csv(out, index=False)
    print('Saved', out, df.shape)
if __name__ == '__main__':
    generate_synthetic()
