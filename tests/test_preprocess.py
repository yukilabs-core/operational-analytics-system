import pytest
import pandas as pd
from datetime import datetime, timedelta
from src.preprocess import (
    calculate_lead_time,
    calculate_active_time,
    calculate_wait_time,
)

@pytest.fixture
def sample_df():
    """テスト用サンプルデータ"""
    return pd.DataFrame({
        'task_id': ['T001', 'T002'],
        'created_at': [
            datetime(2024, 1, 1, 0, 0),
            datetime(2024, 1, 1, 0, 0),
        ],
        'started_at': [
            datetime(2024, 1, 1, 0, 0),
            datetime(2024, 1, 1, 0, 0),
        ],
        'completed_at': [
            datetime(2024, 1, 3, 0, 0),
            datetime(2024, 1, 5, 0, 0),
        ],
    })

def test_lead_time_calculation(sample_df):
    """リードタイム計算のテスト"""
    df = calculate_lead_time(sample_df)
    assert df.loc[0, 'lead_time_days'] == 2.0
    assert df.loc[1, 'lead_time_days'] == 4.0

def test_active_time_calculation(sample_df):
    """実作業時間計算のテスト"""
    df = calculate_active_time(sample_df)
    assert df.loc[0, 'active_time_days'] == 2.0
    assert df.loc[1, 'active_time_days'] == 4.0

def test_wait_time_calculation(sample_df):
    """待機時間計算のテスト"""
    df = calculate_lead_time(sample_df)
    df = calculate_active_time(df)
    df = calculate_wait_time(df)
    assert df.loc[0, 'wait_time_days'] == 0.0
    assert df.loc[1, 'wait_time_days'] == 0.0
