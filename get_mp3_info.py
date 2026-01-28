#!/usr/bin/env python3
"""
GitHubリポジトリからMP3ファイルのサイズと再生時間を取得するスクリプト
"""

import requests
import xml.etree.ElementTree as ET
from urllib.parse import unquote
import sys

try:
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3NoHeaderError
except ImportError:
    print("mutagenライブラリが必要です。インストールしてください: pip install mutagen")
    sys.exit(1)


def get_file_size(url):
    """URLからファイルサイズを取得"""
    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 200:
            content_length = response.headers.get('Content-Length')
            if content_length:
                return int(content_length)
    except Exception as e:
        print(f"ファイルサイズ取得エラー ({url}): {e}")
    return None


def get_mp3_duration(url):
    """MP3ファイルの再生時間を取得（秒）"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        if response.status_code == 200:
            # 一時ファイルに保存せず、メモリで処理
            import io
            audio = MP3(io.BytesIO(response.content))
            return int(audio.info.length)
    except ID3NoHeaderError:
        # ID3タグがない場合でも再生時間は取得できる
        try:
            import io
            response = requests.get(url, stream=True, timeout=30)
            audio = MP3(io.BytesIO(response.content))
            return int(audio.info.length)
        except Exception as e:
            print(f"再生時間取得エラー ({url}): {e}")
    except Exception as e:
        print(f"再生時間取得エラー ({url}): {e}")
    return None


def update_rss_file(xml_file):
    """RSSファイルを読み込んで、MP3ファイルの情報を更新"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # RSS名前空間
    ns = {'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}
    
    items = root.findall('.//item')
    print(f"見つかったエピソード数: {len(items)}")
    
    for i, item in enumerate(items):
        enclosure = item.find('enclosure')
        if enclosure is None:
            continue
            
        url = enclosure.get('url')
        if not url or 'mp3' not in url.lower():
            continue
        
        title_elem = item.find('title')
        title = title_elem.text if title_elem is not None else f"エピソード{i}"
        
        print(f"\n処理中: {title}")
        print(f"  URL: {url}")
        
        # ファイルサイズを取得
        file_size = get_file_size(url)
        if file_size:
            enclosure.set('length', str(file_size))
            print(f"  ファイルサイズ: {file_size} bytes")
        else:
            print(f"  警告: ファイルサイズを取得できませんでした")
        
        # 再生時間を取得
        duration = get_mp3_duration(url)
        if duration:
            duration_elem = item.find('itunes:duration', ns)
            if duration_elem is not None:
                duration_elem.text = str(duration)
                print(f"  再生時間: {duration} 秒 ({duration // 60}:{duration % 60:02d})")
            else:
                print(f"  警告: itunes:duration要素が見つかりませんでした")
        else:
            print(f"  警告: 再生時間を取得できませんでした")
    
    # ファイルを保存
    tree.write(xml_file, encoding='UTF-8', xml_declaration=True)
    print(f"\n更新完了: {xml_file}")


if __name__ == '__main__':
    xml_file = 'kazu-life-podcast rss-source.xml'
    print(f"RSSファイルを処理中: {xml_file}")
    update_rss_file(xml_file)









