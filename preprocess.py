import numpy as np
import pandas as pd
from scipy.stats.mstats import winsorize

def preprocess_data(df):
        # 1. Convert object columns to datetime
        object_col = df.select_dtypes(include=['object']).columns
        for col in object_col:
            df[col] = pd.to_datetime(df[col])

        # 2. Drop columns with >70% null values
        null_counts = df.isnull().sum()
        null_percentage = (null_counts / len(df)) * 100
        null_columns = null_percentage[null_percentage > 0].sort_values()
        df.drop(columns=null_columns[null_percentage >70].index, inplace=True)

        # 3. Drop uniform columns
        numeric_columns = df.select_dtypes(include=['number']).columns
        categorical_columns = df.select_dtypes(include=['object', 'category', 'bool']).columns
        numeric_columns = [col for col in numeric_columns if col != 'mobile_number']
        numeric_uniform_columns = [col for col in numeric_columns if df[col].nunique(dropna=True) == 1]
        categoric_uniform_columns = [col for col in categorical_columns if df[col].nunique(dropna=True) == 1]
        df.drop(columns=numeric_uniform_columns + categoric_uniform_columns, inplace=True)
        numeric_columns = [col for col in numeric_columns if col not in numeric_uniform_columns]
        # 4. Fill numeric missing values with median
        df = df.fillna(df.median(numeric_only=True))

        # 5. Forward-fill remaining nulls
        null_columns_names = df.columns[df.isnull().any()].tolist()
        for col in null_columns_names:
            df[col] = df[col].ffill()

        data_1 = df.copy()
        for col in numeric_columns:
            data_1[col] = winsorize(df[col], (0.01, 0.01))
            lower_bound = np.percentile(data_1[col], 1)
            upper_bound = np.percentile(data_1[col], 99)
            data_1[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
        
        df = data_1
        del data_1
        # 6. Feature Engineering
        

        new_columns = pd.DataFrame({
        'arpu_change': ((df['arpu_9'] - df['arpu_8']) / df['arpu_8']) * 100,
        'total_rech_amt_change': df['total_rech_amt_9'] - df['total_rech_amt_8'],
        'total_rech_num_change': df['total_rech_num_9'] - df['total_rech_num_8'],
        'vol_2g_mb_change': df['vol_2g_mb_9'] - df['vol_2g_mb_8'],
        'vol_3g_mb_change': df['vol_3g_mb_9'] - df['vol_3g_mb_8'],
        'total_og_mou_change': df['total_og_mou_9'] - df['total_og_mou_8']
        })
        df = pd.concat([df, new_columns], axis=1)
        
        df['arpu_change'] = df['arpu_change'].replace([np.inf, -np.inf], np.nan)






        # Drop datetime columns (or optionally convert them)
        

        # Initial Thresholds (Adjust these based on your data analysis)
        arpu_change_threshold = -30  # Example: 30% decrease in ARPU
        total_rech_amt_change_threshold = -500  # Example: 500 unit decrease in recharge amount
        total_rech_num_change_threshold = -3  # Example: 3 recharge decrease
        vol_2g_mb_change_threshold = -100  # Example: 100 MB decrease
        vol_3g_mb_change_threshold = -500  # Example: 500 MB decrease
        total_og_mou_change_threshold = -200 # example: 200 minutes decrease

        
        # Create the pseudo_churn column
        df['churn'] = 0  # Initialize all to 0

        df.loc[
            (df['arpu_change'] < arpu_change_threshold) |
            (df['total_rech_amt_change'] < total_rech_amt_change_threshold) |
            (df['total_rech_num_change'] < total_rech_num_change_threshold) |
            (df['vol_2g_mb_change'] < vol_2g_mb_change_threshold) |
            (df['vol_3g_mb_change'] < vol_3g_mb_change_threshold) |
            (df['total_og_mou_change'] < total_og_mou_change_threshold),
            'churn'
        ] = 1
        df = df.fillna(df.median(numeric_only=True))


        num_cols = df.select_dtypes(include=['number']).columns
        cat_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns

        data_1 = df.copy()
        for col in num_cols:
            data_1[col] = winsorize(df[col], (0.01, 0.01))
            lower_bound = np.percentile(data_1[col], 1)
            upper_bound = np.percentile(data_1[col], 99)
            data_1[col] = df[col].clip(lower=lower_bound, upper=upper_bound)


        df = data_1
        del data_1
        # Drop rows with missing target
        df = df.dropna(subset=['churn'])

        # Split features and target
        X = df.drop(columns=['churn'])
        y = df['churn']

        # Encode categorical variables
        X_encoded = pd.get_dummies(X, drop_first=True)  # One-hot encoding

        return X_encoded,None
