import pandas as pd
import numpy as np

class KPICalculator:
    """KPI計算クラス"""

    def __init__(self, df):
        """df: 前処理済みのタスクデータフレーム"""
        self.df = df
        self.df_completed = df[df['current_status'] == '完了'].copy()

    def total_tasks(self):
        """総件数"""
        return len(self.df)

    def completed_tasks(self):
        """完了件数"""
        return len(self.df_completed)

    def completion_rate(self):
        """完了率 (%)"""
        if self.total_tasks() == 0:
            return 0
        return (self.completed_tasks() / self.total_tasks()) * 100

    def avg_active_time(self):
        """平均実作業時間 (日)"""
        if len(self.df_completed) == 0:
            return 0
        return self.df_completed['active_time_days'].mean()

    def avg_wait_time(self):
        """平均待機時間 (日)"""
        if len(self.df_completed) == 0:
            return 0
        return self.df_completed['wait_time_days'].mean()

    def median_active_time(self):
        """中央値実作業時間 (日)"""
        if len(self.df_completed) == 0:
            return 0
        return self.df_completed['active_time_days'].median()

    def sla_breach_rate(self):
        """SLA超過率 (%)"""
        if len(self.df_completed) == 0:
            return 0
        breach_count = (self.df_completed['sla_breach_flag'] == True).sum()
        return (breach_count / len(self.df_completed)) * 100

    def rework_rate(self):
        """再作業率 (%)"""
        if len(self.df_completed) == 0:
            return 0
        rework_count = (self.df_completed['rework_count'] > 0).sum()
        return (rework_count / len(self.df_completed)) * 100

    def get_summary_kpis(self):
        """全KPIを辞書で返す"""
        return {
            '総件数': self.total_tasks(),
            '完了件数': self.completed_tasks(),
            '完了率(%)': round(self.completion_rate(), 2),
            '平均処理時間(日)': round(self.avg_active_time(), 2),
            '中央値処理時間(日)': round(self.median_active_time(), 2),
            '平均待機時間(日)': round(self.avg_wait_time(), 2),
            'SLA超過率(%)': round(self.sla_breach_rate(), 2),
            '再作業率(%)': round(self.rework_rate(), 2),
        }

def calculate_by_assignee(df):
    """担当者別KPI計算"""
    df_completed = df[df['current_status'] == '完了']

    assignee_kpis = df_completed.groupby('assignee').agg({
        'task_id': 'count',
        'active_time_days': ['mean', 'std'],
        'sla_breach_flag': lambda x: (x == True).sum(),
        'rework_count': lambda x: (x > 0).sum(),
    }).round(2)

    assignee_kpis.columns = ['件数', '平均処理時間', '処理時間SD', 'SLA超過', '再作業件数']
    assignee_kpis['再作業率(%)'] = (assignee_kpis['再作業件数'] / assignee_kpis['件数'] * 100).round(2)

    return assignee_kpis

def calculate_by_status(df):
    """ステータス別KPI計算"""
    status_kpis = df.groupby('current_status').agg({
        'task_id': 'count',
    })
    status_kpis.columns = ['件数']
    return status_kpis
