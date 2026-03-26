import requests
import re
import base64

def get_real_node_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    try:
        # 使用 GitHub 环境去硬刚这个网页
        r = requests.get(url, headers=headers, timeout=15)
        if r.ok:
            # 找到网页里最长的那段 Base64（通常就是节点）
            b64_blocks = re.findall(r'[A-Za-z0-9+/=]{50,}', r.text)
            return "".join(b64_blocks)
    except:
        return ""
    return ""

def main():
    source_url = "https://raw.githubusercontent.com/crashgfw/free-airport-nodes/main/README.md"
    try:
        resp = requests.get(source_url, timeout=20)
        links = re.findall(r'https?://fn08\.sp0303\.xyz/nodes/[a-zA-Z0-9]+', resp.text)
        
        all_raw_nodes = ""
        for link in links:
            print(f"正在提取节点数据: {link}")
            raw_data = get_real_node_data(link)
            if raw_data:
                try:
                    # 解码成 vmess:// 等明文格式
                    decoded = base64.b64decode(raw_data).decode('utf-8', errors='ignore')
                    all_raw_nodes += decoded + "\n"
                except:
                    continue
        
        if all_raw_nodes:
            # 最终整体 Base64 编码，生成标准的订阅格式
            final_b64 = base64.b64encode(all_raw_nodes.encode('utf-8')).decode('utf-8')
            with open('targets.txt', 'w', encoding='utf-8') as f:
                f.write(final_b64)
            print(f"✅ 成功！已提取并打包节点。")
        else:
            print("❌ 未能提取到任何有效数据")
            
    except Exception as e:
        print(f"💥 错误: {e}")

if __name__ == "__main__":
    main()
