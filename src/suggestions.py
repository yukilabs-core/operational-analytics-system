class SuggestionGenerator:
    """改善提案自動生成クラス"""

    def __init__(self, df, kpi_summary, bottleneck_info, assignee_load_info):
        self.df = df
        self.kpi = kpi_summary
        self.bottleneck = bottleneck_info
        self.assignee_load = assignee_load_info
        self.suggestions = []

    def generate_bottleneck_suggestion(self):
        """ボトルネック工程への提案"""
        # ボトルネックが存在するか確認
        bn_statuses = self.bottleneck[self.bottleneck['ボトルネック']].index.tolist()

        if not bn_statuses:
            return None

        bn_status = bn_statuses[0]  # 最初のボトルネック
        wait_time = self.bottleneck.loc[bn_status, '平均待機時間']

        suggestion = f"""
【提案1】ボトルネック工程『{bn_status}』の改善

現状: '{bn_status}' での平均待機時間が {wait_time:.1f}日

対策案:
  1) 承認者/確認者の並列処理体制を検討
  2) 事前チェックリストで不備を削減
  3) 優先度ルールで重要案件を先行
        """
        return suggestion.strip()

    def generate_load_imbalance_suggestion(self):
        """担当者負荷偏りへの提案"""
        if not self.assignee_load['偏在が高い']:
            return None

        assignee_counts = self.assignee_load['担当者別件数']
        max_person = max(assignee_counts, key=assignee_counts.get)
        min_person = min(assignee_counts, key=assignee_counts.get)
        max_count = assignee_counts[max_person]
        min_count = assignee_counts[min_person]

        suggestion = f"""
【提案2】担当者の負荷バランス改善

現状: 最高負荷『{max_person}』({max_count}件) / 最低負荷『{min_person}』({min_count}件)
      負荷偏在指数: {self.assignee_load['負荷偏在指数']:.1f}x

対策案:
  1) '{max_person}' から '{min_person}' へ案件を {(max_count - min_count)//2}件程度転送
  2) 定期的な負荷フラット化レビューを導入
  3) 専門スキル別の配分ルール見直し
        """
        return suggestion.strip()

    def generate_quality_suggestion(self):
        """品質改善への提案"""
        rework_rate = self.kpi.get('再作業率(%)', 0)

        if rework_rate < 5:
            return None

        suggestion = f"""
【提案3】再作業率の削減

現状: 再作業率 {rework_rate:.1f}%

対策案:
  1) 入力チェック項目を強化（事前バリデーション）
  2) よくある不備パターンを整理してチェックリスト化
  3) 再作業になった理由を分類分析
        """
        return suggestion.strip()

    def generate_all_suggestions(self):
        """全ての提案を生成"""
        self.suggestions = [
            self.generate_bottleneck_suggestion(),
            self.generate_load_imbalance_suggestion(),
            self.generate_quality_suggestion(),
        ]

        # Noneを除外
        self.suggestions = [s for s in self.suggestions if s is not None]

        return self.suggestions

    def to_text(self):
        """テキスト形式で返す"""
        if not self.suggestions:
            return "推奨される改善提案がありません。"

        return "\n\n".join(self.suggestions)
