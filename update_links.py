import requests
import re
import base64

def get_content(url):
    """专门负责爬取详情页里的 Base64 乱码"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.ok:
            # 这里的正则专门抓取网页中那一大段 Base64 字符
            # 它们通常包裹在特定的 HTML 标签里或者直接在 body 中
            content = r.text
            # 过滤掉 HTML 标签，只保留可能的 Base64 字符部分
            # 我们直接提取页面上最长的一段连续无空格字符，通常就是节点包
            matches = re.findall(r'[A-Za-z0-9+/=]{50,}', content)
            return "\n".join(matches)
    except:
        return ""
    return ""

def main():
    source_url = "https://raw.githubusercontent.com/crashgfw/free-airport-nodes/main/README.md"
    
    try:
        print("正在获取详情页列表...")
        resp = requests.get(source_url, timeout=20)
        page_links = re.findall(r'https?://fn08\.sp0303\.xyz/nodes/[a-zA-Z0-9]+', resp.text)
        
        all_nodes = []
        if page_links:
            print(f"发现 {len(page_links)} 个页面，开始深度提取节点...")
            for link in page_links:
                print(f"正在提取: {link}")
                raw_data = get_content(link)
                if raw_data:
                    # 尝试解码并提取里面的协议链接 (vmess://, trojan:// 等)
                    try:
                        decoded = base64.b64decode(raw_data).decode('utf-8')
                        all_nodes.append(decoded)
                    except:
                        # 如果解码失败，直接存入原始数据（CF-SUB 能处理原始 Base64）
                        all_nodes.append(raw_data)
            
            # 写入 targets.txt
            with open('targets.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(all_nodes))
            print(f"✅ 大功告成！已将所有节点内容写入 targets.txt")
        else:
            print("❌ 未发现任何页面链接")
            
    except Exception as e:
        print(f"💥 运行崩溃: {e}")

if __name__ == "__main__":
    main()
