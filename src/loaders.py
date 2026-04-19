import pandas as pd
from datetime import datetime

def load_tasks_csv(path):
    """CSVを読み込み、基本的な型変換を行う"""
    df = pd.read_csv(path)

    # datetime型に変換
    datetime_columns = ['created_at', 'due_at', 'started_at', 'completed_at']
    for col in datetime_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    return df
