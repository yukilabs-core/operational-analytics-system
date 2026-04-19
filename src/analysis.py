import pandas as pd
import numpy as np

class BottleneckAnalyzer:
    """ボトルネック分析クラス"""

    def __init__(self, df):
        self.df = df
        self.df_completed = df[df['current_status'] == '完了'].copy()

    def detect_bottlenecks(self, threshold_multiplier=1.5, min_count=5):
        """
        ボトルネック工程を検出

        ロジック:
        - ステータス別の平均待機時間を計算
        - 全体平均の 1.5倍以上 かつ 件数5件以上 をボトルネック判定
        """
        overall_avg_wait = self.df_completed['wait_time_days'].mean()

        # ステータス別の平均待機時間
        status_wait = self.df_completed.groupby('current_status').agg({
            'wait_time_days': ['mean', 'count'],
        }).round(2)

        status_wait.columns = ['平均待機時間', '件数']

        # ボトルネック判定
        status_wait['ボトルネック'] = (
            (status_wait['平均待機時間'] > overall_avg_wait * threshold_multiplier) &
            (status_wait['件数'] >= min_count)
        )

        return status_wait

    def analyze_assignee_load(self):
        """
        担当者の負荷偏りを分析

        指標: 最大負荷 / 最小負荷（偏在指数）
        """
        df_completed = self.df_completed

        assignee_counts = df_completed['assignee'].value_counts()

        if len(assignee_counts) < 2:
            load_disparity = 1.0
        else:
            load_disparity = assignee_counts.max() / assignee_counts.min()

        return {
            '担当者別件数': assignee_counts.to_dict(),
            '負荷偏在指数': round(load_disparity, 2),
            '偏在が高い': load_disparity > 2.0,
        }

    def analyze_by_department(self):
        """部門別の滞留分析"""
        df_completed = self.df_completed

        dept_analysis = df_completed.groupby('department').agg({
            'task_id': 'count',
            'active_time_days': 'mean',
            'wait_time_days': 'mean',
            'sla_breach_flag': lambda x: (x == True).sum(),
        }).round(2)

        dept_analysis.columns = ['件数', '平均処理時間', '平均待機時間', 'SLA超過件数']

        return dept_analysis

def analyze_by_day_of_week(df):
    """曜日別の処理件数・時間分析"""
    df_completed = df[df['current_status'] == '完了'].copy()
    df_completed['dow'] = df_completed['completed_at'].dt.day_name()

    dow_analysis = df_completed.groupby('dow').agg({
        'task_id': 'count',
        'active_time_days': 'mean',
    }).round(2)

    dow_analysis.columns = ['完了件数', '平均処理時間']

    return dow_analysis
