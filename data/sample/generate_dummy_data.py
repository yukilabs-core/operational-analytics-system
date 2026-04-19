import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_dummy_tasks(n_tasks=500, seed=42):
    """
    リアルな業務データを生成

    仕様:
    - 件数: 500件
    - 期間: 直近90日
    - ステータス: 4段階（作成→処理中→確認待ち→完了）
    - 担当者: 5人（能力差あり）
    - 差し戻し率: 10%
    """

    random.seed(seed)
    np.random.seed(seed)

    # 基本パラメータ
    statuses = ['作成', '処理中', '確認待ち', '完了']
    assignees = ['担当者A', '担当者B', '担当者C', '担当者D', '担当者E']
    departments = ['営業', '企画', '事務', '技術']
    priorities = ['低', '中', '高']
    categories = ['案件', '問い合わせ', '報告', '申請']

    # 担当者の処理時間（分布の中央値）
    assignee_speed = {
        '担当者A': 2.0,   # 速い（2日）
        '担当者B': 4.0,   # 普通（4日）
        '担当者C': 4.5,   # 普通（4.5日）
        '担当者D': 5.0,   # 遅い（5日）
        '担当者E': 3.5,   # やや速い（3.5日）
    }

    tasks = []
    base_date = datetime.now() - timedelta(days=90)

    for task_id in range(1, n_tasks + 1):
        # 作成日時（直近90日、時間帯はランダム）
        days_ago = random.randint(0, 89)
        hours_offset = random.randint(0, 23)
        created_at = base_date + timedelta(days=days_ago, hours=hours_offset)

        # 期限（作成から3-7日後）
        due_at = created_at + timedelta(days=random.randint(3, 7))

        # 担当者（ランダム割当）
        assignee = random.choice(assignees)

        # 処理時間（担当者の能力に応じて変動）
        base_time = assignee_speed[assignee]
        processing_days = np.random.normal(base_time, 0.8)  # 標準偏差0.8日
        processing_days = max(0.5, processing_days)  # 最小0.5日

        # ステータス判定
        started_at = created_at + timedelta(hours=random.randint(1, 4))

        # 完了しているか、待機中か、未処理か（8割完了、2割未処理）
        if random.random() < 0.85:
            # 完了
            completed_at = started_at + timedelta(days=processing_days)

            # SLA判定（期限内か？）
            sla_breach = completed_at > due_at

            # 差し戻し（10%の確率）
            rework_count = 1 if random.random() < 0.10 else 0
            current_status = '完了'

            # 差し戻しがあれば、完了日を遅延させる
            if rework_count > 0:
                completed_at = completed_at + timedelta(days=1.5)
                sla_breach = completed_at > due_at
        else:
            # 未完了（処理中 or 確認待ち）
            if random.random() < 0.6:
                current_status = '処理中'
                completed_at = None
            else:
                current_status = '確認待ち'
                completed_at = None
            sla_breach = False
            rework_count = 0

        # 待機時間の粗い推定（確認待ちの場合は長くする）
        if current_status == '確認待ち':
            wait_hours = random.randint(12, 48)
        elif current_status == '処理中':
            wait_hours = random.randint(0, 8)
        else:
            wait_hours = random.randint(0, 4)

        tasks.append({
            'task_id': f'T{task_id:06d}',
            'title': f'タスク{task_id}',
            'category': random.choice(categories),
            'priority': random.choice(priorities),
            'department': random.choice(departments),
            'assignee': assignee,
            'created_at': created_at.isoformat(),
            'due_at': due_at.isoformat(),
            'started_at': started_at.isoformat(),
            'completed_at': completed_at.isoformat() if completed_at else '',
            'current_status': current_status,
            'processing_time_hours': (completed_at - started_at).total_seconds() / 3600 if completed_at else None,
            'wait_time_hours': wait_hours,
            'rework_count': rework_count,
            'sla_breach_flag': sla_breach if completed_at else False,
        })

    df = pd.DataFrame(tasks)
    return df

if __name__ == '__main__':
    df = generate_dummy_tasks(n_tasks=500)
    df.to_csv('tasks.csv', index=False)
    print(f"Generated {len(df)} dummy tasks")
    print(df.head())
