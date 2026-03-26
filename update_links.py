import requests
import re

def main():
    # 源仓库（我们要监控的对象）
    source_url = "https://raw.githubusercontent.com/crashgfw/free-airport-nodes/main/README.md"
    
    try:
        print("正在获取最新详情页网址...")
        resp = requests.get(source_url, timeout=20)
        # 提取那 15 个详情页链接
        links = re.findall(r'https?://fn08\.sp0303\.xyz/nodes/[a-zA-Z0-9]+', resp.text)
        
        if links:
            # 存入 targets.txt，一行一个网址
            with open('targets.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(links))
            print(f"✅ 成功！已记录 {len(links)} 个网址。")
        else:
            print("❌ 未发现链接，请检查源仓库。")
    except Exception as e:
        print(f"💥 出错: {e}")

if __name__ == "__main__":
    main()
