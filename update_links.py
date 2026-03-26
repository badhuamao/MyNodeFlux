import requests
import re

def main():
    # 1. 目标：源仓库的 README (这里有那 15 个详情页链接)
    source_url = "https://raw.githubusercontent.com/crashgfw/free-airport-nodes/main/README.md"
    
    try:
        print("正在同步源仓库数据...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(source_url, headers=headers, timeout=20)
        resp.raise_for_status()
        
        # 2. 正则提取所有详情页 URL
        # 匹配格式: https://fn08.sp0303.xyz/nodes/XXXXXX
        links = re.findall(r'https?://fn08\.sp0303\.xyz/nodes/[a-zA-Z0-9]+', resp.text)
        
        if links:
            # 3. 去重并保存
            unique_links = sorted(list(set(links)))
            with open('targets.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(unique_links))
            print(f"✅ 成功提取 {len(unique_links)} 个最新详情页链接！")
        else:
            print("❌ 警告：未在源文件中找到任何链接，请检查源仓库是否改版。")
            
    except Exception as e:
        print(f"💥 运行崩溃: {e}")

if __name__ == "__main__":
    main()
