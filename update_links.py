import requests
import re

def main():
    # 1. 还是老规矩，去拿那 15 个详情页链接
    source_url = "https://raw.githubusercontent.com/crashgfw/free-airport-nodes/main/README.md"
    
    try:
        resp = requests.get(source_url, timeout=20)
        # 提取链接
        links = re.findall(r'https?://fn08\.sp0303\.xyz/nodes/[a-zA-Z0-9]+', resp.text)
        
        if links:
            # 2. 我们不爬网页内容了，直接把这 15 个原始链接存进 targets.txt
            # 这样 targets.txt 就成了一个“链接清单”
            with open('targets.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(links))
            print(f"✅ 已成功整理 {len(links)} 个详情页链接！")
        else:
            print("❌ 未能获取到链接清单")
            
    except Exception as e:
        print(f"⚠️ 运行异常: {e}")

if __name__ == "__main__":
    main()
