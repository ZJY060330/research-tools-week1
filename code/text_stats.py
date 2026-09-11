"""实验二：统计文本文件中的单词出现频率。

用法：
    python code/text_stats.py <文本文件> [--top N]

规则：
    - 忽略大小写（统一转成小写后再统计）
    - 去掉标点：标点一律作为分隔符，单词 = 连续的字母
      （因此 don't 会被拆成 don 和 t 两个词）
    - 按出现次数降序输出前 N 个单词，默认 N = 10
    - 次数相同时按字母升序排列，保证结果稳定可复现
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

# 一个“单词”= 一串连续的字母；标点和数字都不属于单词，起分隔作用
# [^\W\d_] = 字母（Unicode 语义：排除非单词字符、数字、下划线）
WORD_PATTERN = re.compile(r"[^\W\d_]+", re.UNICODE)


def count_words(text):
    """返回 Counter：单词（小写）-> 出现次数。"""
    return Counter(WORD_PATTERN.findall(text.lower()))


def top_words(counter, n=10):
    """按次数降序、单词升序返回前 n 项，元素为 (单词, 次数)。"""
    return sorted(counter.items(), key=lambda item: (-item[1], item[0]))[:n]


def build_parser():
    parser = argparse.ArgumentParser(
        description="统计文本文件中的单词频率，输出出现次数最多的前 N 个单词。"
    )
    parser.add_argument("file", help="待统计的文本文件路径")
    parser.add_argument(
        "-n", "--top", type=int, default=10, help="输出前多少个单词，默认 10"
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)

    if args.top <= 0:
        print("错误：--top 必须是正整数", file=sys.stderr)
        return 2

    path = Path(args.file)
    if path.is_dir():
        print(f"错误：{path} 是目录，不是文件", file=sys.stderr)
        return 1

    try:
        # 文本文件按 UTF-8 读取；errors="replace" 避免个别坏字节直接崩溃
        text = path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        print(f"错误：找不到文件 {path}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"错误：无法读取 {path}：{exc}", file=sys.stderr)
        return 1

    counter = count_words(text)
    if not counter:
        print("警告：文件中没有找到任何单词", file=sys.stderr)
        return 1

    print(f"文件：{path}    不同单词：{len(counter)}    总词数：{sum(counter.values())}")
    print(f"出现次数最多的前 {min(args.top, len(counter))} 个单词：")
    for rank, (word, count) in enumerate(top_words(counter, args.top), start=1):
        print(f"{rank:>2}. {word:<15} {count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
