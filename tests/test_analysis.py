import pytest
import pandas as pd
from src.analysis import BottleneckAnalyzer

@pytest.fixture
def sample_df_with_bottleneck():
    """ボトルネック検出用サンプルデータ"""
    return pd.DataFrame({
        'task_id': ['T001', 'T002', 'T003', 'T004', 'T005', 'T006'],
        'current_status': ['完了', '完了', '完了', '完了', '完了', '完了'],
        'wait_time_days': [
            1.0,
            1.0,
            1.0,
            12.0,
            12.0,
            12.0,
        ],
    })

def test_bottleneck_detection(sample_df_with_bottleneck):
    """ボトルネック検出のテスト"""
    analyzer = BottleneckAnalyzer(sample_df_with_bottleneck)
    assert analyzer.df_completed is not None
