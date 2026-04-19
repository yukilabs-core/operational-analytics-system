import pandas as pd
from .loaders import load_tasks_csv
from .preprocess import preprocess_pipeline
from .kpi import KPICalculator, calculate_by_assignee
from .analysis import BottleneckAnalyzer, analyze_by_day_of_week
from .suggestions import SuggestionGenerator
from .visualize import plot_kpi_summary, plot_assignee_comparison, plot_bottleneck_analysis

class AnalyticsPipeline:
    """分析パイプラインの統括クラス"""

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
        self.results = {}

    def run(self, output_dir='output'):
        """全体パイプラインを実行"""
        import os
        os.makedirs(output_dir, exist_ok=True)

        print("🔄 Step 1: データ読込...")
        self.df = load_tasks_csv(self.csv_path)
        print(f"   ✓ {len(self.df)} 件読み込み")

        print("🔄 Step 2: データ前処理...")
        self.df = preprocess_pipeline(self.df)
        print("   ✓ 完了")

        print("🔄 Step 3: KPI計算...")
        kpi_calc = KPICalculator(self.df)
        kpi_summary = kpi_calc.get_summary_kpis()
        self.results['kpi'] = kpi_summary
        print(f"   ✓ 完了率: {kpi_summary['完了率(%)']:.1f}%")

        print("🔄 Step 4: 担当者別分析...")
        assignee_kpis = calculate_by_assignee(self.df)
        self.results['assignee_kpis'] = assignee_kpis
        print(f"   ✓ {len(assignee_kpis)} 人分析")

        print("🔄 Step 5: ボトルネック検出...")
        bn_analyzer = BottleneckAnalyzer(self.df)
        bottleneck_info = bn_analyzer.detect_bottlenecks()
        assignee_load_info = bn_analyzer.analyze_assignee_load()
        self.results['bottleneck'] = bottleneck_info
        self.results['assignee_load'] = assignee_load_info
        print(f"   ✓ 検出完了")

        print("🔄 Step 6: 改善提案生成...")
        suggestion_gen = SuggestionGenerator(
            self.df, kpi_summary, bottleneck_info, assignee_load_info
        )
        suggestions = suggestion_gen.generate_all_suggestions()
        self.results['suggestions'] = suggestions
        print(f"   ✓ {len(suggestions)} 件の提案を生成")

        print("🔄 Step 7: 可視化...")
        plot_kpi_summary(kpi_summary, f'{output_dir}/charts')
        plot_assignee_comparison(assignee_kpis, f'{output_dir}/charts')
        plot_bottleneck_analysis(bottleneck_info, f'{output_dir}/charts')
        print("   ✓ 3枚のグラフを生成")

        print("🔄 Step 8: レポート出力...")
        self._save_markdown_report(output_dir)
        print("   ✓ Markdownレポート出力")

        print("\n✅ 分析完了！")
        print(f"   出力先: {output_dir}/")

    def _save_markdown_report(self, output_dir):
        """Markdownレポートを生成"""
        md_lines = [
            "# 業務データ分析レポート",
            "",
            "## 1. KPI サマリー",
            "",
            "| 指標 | 値 |",
            "|------|-----|",
        ]

        for k, v in self.results['kpi'].items():
            md_lines.append(f"| {k} | {v} |")

        md_lines.extend([
            "",
            "## 2. 担当者別分析",
            "",
            self.results['assignee_kpis'].to_markdown(),
            "",
            "## 3. ボトルネック分析",
            "",
            self.results['bottleneck'].to_markdown(),
            "",
            f"負荷偏在指数: {self.results['assignee_load']['負荷偏在指数']}",
            "",
            "## 4. 改善提案",
            "",
        ])

        for suggestion in self.results['suggestions']:
            md_lines.append(suggestion)
            md_lines.append("")

        report_path = f'{output_dir}/analysis_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_lines))
