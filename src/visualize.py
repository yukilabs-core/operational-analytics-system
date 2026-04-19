import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os

def plot_kpi_summary(kpi_dict, output_dir='output/charts'):
    """KPI サマリーを表形式で画像化"""
    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis('tight')
    ax.axis('off')

    # テーブルデータを準備
    table_data = [[k, str(v)] for k, v in kpi_dict.items()]

    table = ax.table(cellText=table_data, colLabels=['指標', '値'],
                     cellLoc='center', loc='center',
                     colWidths=[0.6, 0.4])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)

    plt.title('KPI サマリー', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/01_kpi_summary.png', dpi=100, bbox_inches='tight')
    plt.close()

    print(f"✓ KPI summary saved: {output_dir}/01_kpi_summary.png")

def plot_assignee_comparison(assignee_kpis, output_dir='output/charts'):
    """担当者別の処理時間・件数比較"""
    os.makedirs(output_dir, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # 件数比較
    assignee_kpis['件数'].plot(kind='bar', ax=axes[0], color='steelblue')
    axes[0].set_title('担当者別 完了件数', fontweight='bold')
    axes[0].set_xlabel('担当者')
    axes[0].set_ylabel('件数')
    axes[0].grid(axis='y', alpha=0.3)

    # 処理時間比較
    assignee_kpis['平均処理時間'].plot(kind='bar', ax=axes[1], color='coral')
    axes[1].set_title('担当者別 平均処理時間', fontweight='bold')
    axes[1].set_xlabel('担当者')
    axes[1].set_ylabel('日数')
    axes[1].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/02_assignee_comparison.png', dpi=100, bbox_inches='tight')
    plt.close()

    print(f"✓ Assignee comparison saved: {output_dir}/02_assignee_comparison.png")

def plot_bottleneck_analysis(bottleneck_df, output_dir='output/charts'):
    """ボトルネック分析を棒グラフで表示"""
    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 4))

    bottleneck_df['平均待機時間'].plot(kind='barh', ax=ax, color='tomato')
    ax.set_title('ステータス別 平均待機時間', fontweight='bold')
    ax.set_xlabel('日数')
    ax.grid(axis='x', alpha=0.3)

    # ボトルネック判定箇所にマーク
    for i, (idx, row) in enumerate(bottleneck_df.iterrows()):
        if row['ボトルネック']:
            ax.text(row['平均待機時間'] + 0.3, i, '⚠ ボトルネック',
                   va='center', fontweight='bold', color='red')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/03_bottleneck_analysis.png', dpi=100, bbox_inches='tight')
    plt.close()

    print(f"✓ Bottleneck analysis saved: {output_dir}/03_bottleneck_analysis.png")
