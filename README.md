# 業務データ分析システム

## 概要

単一の CSV ファイルから業務改善ポイントを自動抽出する Python パッケージです。

**特徴：**
- ✅ KPI 自動計算（完了率、平均処理時間、SLA超過率など）
- ✅ ボトルネック工程の自動検出
- ✅ 担当者別の能力・負荷分析
- ✅ AI 改善提案の自動生成
- ✅ グラフ・レポートの自動出力

---

## セットアップ

### 1. リポジトリをクローン

```bash
cd /home/dev-nodee/operational-analytics-system
```

### 2. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

### 3. ダミーデータを生成（初回のみ）

```bash
cd data/sample
python generate_dummy_data.py
# → tasks.csv が生成される
```

---

## 使用方法

### シンプルな実行

```bash
python run.py
```

デフォルトの入力: `data/sample/tasks.csv`
デフォルトの出力: `output/`

### カスタムパスで実行

```bash
python run.py --input /path/to/your/data.csv --output /path/to/output
```

---

## 出力内容

実行完了後、`output/` ディレクトリに以下が生成されます：

```
output/
├── analysis_report.md          # 分析レポート（Markdown形式）
└── charts/
    ├── 01_kpi_summary.png      # KPI一覧表
    ├── 02_assignee_comparison.png  # 担当者別比較グラフ
    └── 03_bottleneck_analysis.png  # ボトルネック分析グラフ
```

---

## テスト実行

```bash
pytest tests/ -v
```

---

## 実装モジュール

| モジュール | 役割 |
|-----------|------|
| `loaders.py` | CSV 読込み |
| `preprocess.py` | データ前処理（リードタイム、待機時間など計算） |
| `kpi.py` | KPI 計算（完了率、平均処理時間など） |
| `analysis.py` | ボトルネック検出、担当者負荷分析 |
| `suggestions.py` | 改善提案の自動生成 |
| `visualize.py` | グラフ・画像出力 |
| `pipeline.py` | 全体パイプライン統括 |

---

## ポートフォリオの意図

### 1. なぜ 500 件か？

統計的な説得力が必要です。
- 少なすぎる（10件程度）→ ノイズが大きい
- 多すぎる（10万件）→ リアルなデータソースが限定的

**500件** は業務データの1-3ヶ月分に相当し、パターン認識に必要な最小サンプル数。

### 2. テストコードの存在

単なる「動く」ではなく「正しく動く」ことを証明。
- `test_preprocess.py`: 計算ロジックの正確性
- `test_kpi.py`: KPI 算出の正確性
- `test_analysis.py`: 分析結果の検証可能性

### 3. 改善提案が「なぜか」を説明

提案の根拠をコードに実装：
- **ボトルネック提案**: `threshold_multiplier=1.5`（全体平均の 1.5 倍以上）
- **負荷偏り提案**: `load_disparity > 2.0`（最大/最小の比率）
- **品質提案**: `rework_rate < 5`（5%未満なら不要）

分析の思考過程が見える。

### 4. 実装順序の透明性

4日間の段階的実装を示す：
- **Day 1**: 基礎（データ読込・前処理）
- **Day 2**: 計算（KPI・分析）
- **Day 3**: 可視化・提案
- **Day 4**: 統合・ドキュメント

プロジェクト管理能力を証明。

---

## このシステムで証明すること

✅ **データ分析能力**
- Pandas による複雑な集計
- 統計量の計算（平均・中央値・標準偏差）

✅ **仮説検証能力**
- ボトルネック仮説の検定
- 負荷偏り指数の定量化

✅ **改善提案能力**
- データに基づく施策立案
- 実装可能な対策を複数提示

✅ **エンジニアリング実装力**
- テストコード
- 整理されたモジュール設計
- CLI インターフェース

---

## ライセンス

MIT

---

## Author

yuki-labs
