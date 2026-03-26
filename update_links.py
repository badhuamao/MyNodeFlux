import requests
import re
import base64

def get_nodes_from_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if not r.ok: return []
        
        # 核心逻辑：直接把网页里所有 50 字符以上的“连续非空字符”全抓出来
        # 这样不管他把 Base64 藏在哪个标签里，都能被正则扫到
        potential_blocks = re.findall(r'[A-Za-z0-9+/=]{50,}', r.text)
        
        results = []
        for block in potential_blocks:
            try:
                # 尝试解密这块乱码
                decoded = base64.b64decode(block).decode('utf-8', errors='ignore')
                # 只要解开的内容里有任何一个协议头，就说明抓对宝了
                if any(proto in decoded for proto in ['vmess://', 'vless://', 'trojan://', 'ss://', 'hy2://', 'hysteria2://']):
                    # 按照行分割，防止多个节点粘在一起
                    results.extend([line.strip() for line in decoded.splitlines() if '://' in line])
            except:
                continue
        return results
    except:
        return []

def main():
    source_url = "https://raw.githubusercontent.com/crashgfw/free-airport-nodes/main/README.md"
    try:
        print("🕵️ 正在进行全网页扫描提取...")
        resp = requests.get(source_url, timeout=20)
        # 提取那 15 个详情页链接
        links = re.findall(r'https?://fn08\.sp0303\.xyz/nodes/[a-zA-Z0-9]+', resp.text)
        
        all_nodes = set() # 自动去重
        for link in links:
            print(f"📡 扫描中: {link}")
            found = get_nodes_from_page(link)
            if found:
                print(f"   ✅ 成功扣出 {len(found)} 个节点")
                all_nodes.update(found)
        
        if all_nodes:
            # 合并后再次 Base64 编码，生成 NekoRay 喜欢的标准格式
            final_str = "\n".join(list(all_nodes))
            b64_data = base64.b64encode(final_str.encode('utf-8')).decode('utf-8')
            
            with open('targets.txt', 'w', encoding='utf-8') as f:
                f.write(b64_data)
            print(f"🎉 大功告成！共收割 {len(all_nodes)} 个唯一节点，已写入 targets.txt")
        else:
            print("❌ 扫描结束，未能发现任何节点。可能需要人工检查网页源码了。")
            
    except Exception as e:
        print(f"⚠️ 运行异常: {e}")

if __name__ == "__main__":
    main()
