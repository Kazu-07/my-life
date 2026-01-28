#!/usr/bin/env python3
"""
RSS XMLファイルのitemタグ内の要素間に空行を追加し、ns0:をitunes:に統一するスクリプト
"""

import re
import sys

def format_item(item_content):
    """itemタグの内容を整形"""
    # ns0:をitunes:に置換
    item_content = item_content.replace('ns0:', 'itunes:')
    
    # 各要素の間に空行を追加
    # title
    item_content = re.sub(r'(<item>\s*)(<title>)', r'\1\n      \2', item_content)
    # itunes:author
    item_content = re.sub(r'(</title>\s*)(<itunes:author>)', r'\1\n\n      \2', item_content)
    # itunes:summary
    item_content = re.sub(r'(</itunes:author>\s*)(<itunes:summary>)', r'\1\n\n      \2', item_content)
    # description
    item_content = re.sub(r'(</itunes:summary>\s*)(<description>)', r'\1\n\n      \2', item_content)
    # enclosure
    item_content = re.sub(r'(</description>\s*)(<enclosure)', r'\1\n\n      \2', item_content)
    # guid
    item_content = re.sub(r'(/>\s*)(<guid>)', r'\1\n\n      \2', item_content)
    # pubDate
    item_content = re.sub(r'(</guid>\s*)(<pubDate>)', r'\1\n\n      \2', item_content)
    # itunes:duration
    item_content = re.sub(r'(</pubDate>\s*)(<itunes:duration>)', r'\1\n\n      \2', item_content)
    # itunes:explicit
    item_content = re.sub(r'(</itunes:duration>\s*)(<itunes:explicit>)', r'\1\n\n      \2', item_content)
    # itunes:image
    item_content = re.sub(r'(</itunes:explicit>\s*)(<itunes:image)', r'\1\n\n      \2', item_content)
    # </item>
    item_content = re.sub(r'(/>\s*)(</item>)', r'\1\n\n    \2', item_content)
    
    return item_content

def format_rss_file(filename):
    """RSSファイルを整形"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 名前空間をitunes:に統一
    content = content.replace('xmlns:ns0=', 'xmlns:itunes=')
    content = content.replace('ns0:', 'itunes:')
    
    # itemタグを抽出して整形
    pattern = r'(  <item>.*?</item>)'
    
    def replace_item(match):
        item_content = match.group(1)
        # 既存の空行を削除
        item_content = re.sub(r'\n\s*\n', '\n', item_content)
        # 各要素の間に空行を追加
        item_content = re.sub(r'(<item>\s*)(<title>)', r'\1\n      \2', item_content)
        item_content = re.sub(r'(</title>\s*)(<itunes:author>)', r'\1\n\n      \2', item_content)
        item_content = re.sub(r'(</itunes:author>\s*)(<itunes:summary>)', r'\1\n\n      \2', item_content)
        item_content = re.sub(r'(</itunes:summary>\s*)(<description>)', r'\1\n\n      \2', item_content)
        item_content = re.sub(r'(</description>\s*)(<enclosure)', r'\1\n\n      \2', item_content)
        item_content = re.sub(r'(/>\s*)(<guid>)', r'\1\n\n      \2', item_content)
        item_content = re.sub(r'(</guid>\s*)(<pubDate>)', r'\1\n\n      \2', item_content)
        item_content = re.sub(r'(</pubDate>\s*)(<itunes:duration>)', r'\1\n\n      \2', item_content)
        item_content = re.sub(r'(</itunes:duration>\s*)(<itunes:explicit>)', r'\1\n\n      \2', item_content)
        item_content = re.sub(r'(</itunes:explicit>\s*)(<itunes:image)', r'\1\n\n      \2', item_content)
        item_content = re.sub(r'(/>\s*)(</item>)', r'\1\n\n    \2', item_content)
        return item_content
    
    content = re.sub(pattern, replace_item, content, flags=re.DOTALL)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"整形完了: {filename}")

if __name__ == '__main__':
    filename = 'kazu-life-podcast rss-source.xml'
    format_rss_file(filename)



















