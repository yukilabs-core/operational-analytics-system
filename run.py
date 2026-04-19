#!/usr/bin/env python3
"""
業務データ分析システム - メインスクリプト

使用方法:
    python run.py --input data/sample/tasks.csv --output output
"""

import argparse
from src.pipeline import AnalyticsPipeline

def main():
    parser = argparse.ArgumentParser(
        description='業務データ分析システム'
    )
    parser.add_argument(
        '--input', '-i',
        type=str,
        default='data/sample/tasks.csv',
        help='入力CSVファイルパス (デフォルト: data/sample/tasks.csv)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='output',
        help='出力ディレクトリ (デフォルト: output)'
    )

    args = parser.parse_args()

    print(f"📊 業務データ分析システム")
    print(f"入力: {args.input}")
    print(f"出力: {args.output}\n")

    pipeline = AnalyticsPipeline(args.input)
    pipeline.run(output_dir=args.output)

if __name__ == '__main__':
    main()
