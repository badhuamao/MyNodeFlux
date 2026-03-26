import requests
import re
import base64
import time

def get_real_node_data(url):
    # 模拟最新版 Chrome 浏览器的完整请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://github.com/crashgfw/free-airport-nodes',
        'Connection': 'keep-alive'
    }
    try:
        # 增加延迟，模拟真人点击
        time.sleep(1) 
        r = requests.get(url, headers=headers, timeout=15)
        if r.ok:
            # 这里的正则修改：不再只找 50 位以上的，只要是符合 Base64 协议特征的都抓
            # 有时候节点会被拆分成多段
            content = r.text
            
            # 暴力匹配：提取页面中所有看起来像 Base64 的段落
            blocks = re.findall(r'[A-Za-z0-9+/=]{40,}', content)
            
            valid_nodes = []
            for b in blocks:
                try:
                    decoded = base64.b64decode(b).decode('utf-8', errors='ignore')
                    # 只要解出来包含常见的协议头，就认为是有效节点
                    if any(p in decoded for p in ['vmess://', 'vless://', 'ss://', 'trojan://', 'hy2://', 'hysteria2://']):
                        valid_nodes.extend(decoded.splitlines())
                except:
                    continue
            return valid_nodes
    except:
        return []
    return []

def main():
    source_url = "https://raw.githubusercontent.com/crashgfw/free-airport-nodes/main/README.md"
    try:
        # 获取那 15 个链接
        resp = requests.get(source_url, timeout=20)
        links = re.findall(r'https?://fn08\.sp0303\.xyz/nodes/[a-zA-Z0-9]+', resp.text)
        
        all_nodes = set()
        if links:
            for link in links:
                print(f"🕵️ 正在尝试突破: {link}")
                nodes = get_real_node_data(link)
                if nodes:
                    print(f"   ✅ 成功获取 {len(nodes)} 个节点")
                    for n in nodes:
                        if "://" in n: all_nodes.add(n.strip())
                else:
                    print(f"   ❌ 突破失败，页面未返回有效负载")
        
        if all_nodes:
            # 标准 Base64 订阅封装
            final_data = "\n".join(list(all_nodes))
            b64_output = base64.b64encode(final_data.encode('utf-8')).decode('utf-8')
            with open('targets.txt', 'w', encoding='utf-8') as f:
                f.write(b64_output)
            print(f"🎉 任务完成！共计提取 {len(all_nodes)} 个节点")
        else:
            print("⚠️ 警告：全军覆没，对方可能升级了动态加密（JS-Challenge）")
            
    except Exception as e:
        print(f"💥 运行崩溃: {e}")

if __name__ == "__main__":
    main()
