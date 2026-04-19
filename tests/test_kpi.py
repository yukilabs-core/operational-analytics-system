import pytest
import pandas as pd
from datetime import datetime
from src.kpi import KPICalculator

@pytest.fixture
def sample_df_with_status():
    """ステータス付きサンプルデータ"""
    return pd.DataFrame({
        'task_id': ['T001', 'T002', 'T003', 'T004'],
        'current_status': ['完了', '完了', '完了', '処理中'],
        'sla_breach_flag': [False, False, True, False],
        'rework_count': [0, 0, 1, 0],
        'active_time_days': [2.0, 3.0, 4.0, 1.5],
        'wait_time_days': [0.5, 1.0, 2.0, 0.0],
    })

def test_completion_rate(sample_df_with_status):
    """完了率の計算テスト"""
    calc = KPICalculator(sample_df_with_status)
    assert calc.completion_rate() == 75.0

def test_sla_breach_rate(sample_df_with_status):
    """SLA超過率の計算テスト"""
    calc = KPICalculator(sample_df_with_status)
    assert calc.sla_breach_rate() == pytest.approx(33.33, abs=0.1)

def test_rework_rate(sample_df_with_status):
    """再作業率の計算テスト"""
    calc = KPICalculator(sample_df_with_status)
    assert calc.rework_rate() == pytest.approx(33.33, abs=0.1)

def test_avg_active_time(sample_df_with_status):
    """平均処理時間のテスト"""
    calc = KPICalculator(sample_df_with_status)
    assert calc.avg_active_time() == 3.0
