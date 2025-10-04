import pandas as pd
import os

in_path = os.path.join(os.path.dirname(__file__), '..', 'data','sample_water.csv')
out_path = os.path.join(os.path.dirname(__file__), '..', 'data','processed_water.csv')

def preprocess(path_in=in_path, path_out=out_path):
    df = pd.read_csv(path_in, parse_dates=['date'])
    df = df.sort_values(['household_id', 'date']).reset_index(drop=True)
 # Time features
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.weekday
    df['is_weekend'] = df['day_of_week'].isin([5,6]).astype(int)

    df.to_csv(path_out, index=False)
    print('Saved', path_out, df.shape)
    return df
if __name__ == '__main__':
    preprocess()