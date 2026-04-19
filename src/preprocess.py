import pandas as pd
import numpy as np

def normalize_columns(df):
    """列名の標準化"""
    df.columns = df.columns.str.lower().str.strip()
    return df

def calculate_lead_time(df):
    """リードタイム(作成～完了の日数)を計算"""
    df['lead_time_days'] = (df['completed_at'] - df['created_at']).dt.total_seconds() / (24 * 3600)
    return df

def calculate_active_time(df):
    """実作業時間(開始～完了の日数)を計算"""
    df['active_time_days'] = (df['completed_at'] - df['started_at']).dt.total_seconds() / (24 * 3600)
    return df

def calculate_wait_time(df):
    """待機時間(完了済みのもののみ)を計算"""
    df['wait_time_days'] = df['lead_time_days'] - df['active_time_days']
    df['wait_time_days'] = df['wait_time_days'].clip(lower=0)  # 負数はクリップ
    return df

def flag_outliers(df, column='active_time_days', threshold=3):
    """外れ値にフラグを立てる（3σを超える）"""
    mean = df[column].mean()
    std = df[column].std()
    df[f'{column}_outlier'] = np.abs(df[column] - mean) > threshold * std
    return df

def preprocess_pipeline(df):
    """前処理の全体パイプライン"""
    df = normalize_columns(df)
    df = calculate_lead_time(df)
    df = calculate_active_time(df)
    df = calculate_wait_time(df)
    df = flag_outliers(df, column='active_time_days')

    # 欠損値の処理
    df = df.copy()
    df['active_time_days'] = df['active_time_days'].fillna(df['active_time_days'].mean())
    df['wait_time_days'] = df['wait_time_days'].fillna(0)

    return df
