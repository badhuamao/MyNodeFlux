import requests
import re
import base64
import time

def get_real_node_data(url):
    # 使用更加逼真的浏览器头，加入随机的 Cookie 模拟
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
    }
    try:
        # 增加随机停顿，防止被防火墙瞬间识别
        time.sleep(2) 
        r = requests.get(url, headers=headers, timeout=20)
        if r.ok:
            content = r.text
            # 改进正则：专门寻找被引号包裹或者在特定的 HTML 结构里的 Base64 字符串
            # 同时也寻找可能直接暴露的 vmess/vless 等协议前缀
            
            # 1. 尝试直接找协议
            protocols = re.findall(r'(vmess|vless|trojan|ss|hysteria2|hy2)://[a-zA-Z0-9\-\.\_\~\!\*\'\(\)\;\:\@\&\=\+\$\,\/\?\%\#\[\]]+', content)
            if protocols:
                return protocols

            # 2. 如果没找到协议，找超长的 Base64 块（通常以 == 结尾）
            blocks = re.findall(r'[A-Za-z0-9+/]{80,sha}==?', content)
            
            valid_nodes = []
            for b in blocks:
                try:
                    decoded = base64.b64decode(b).decode('utf-8', errors='ignore')
                    if '://' in decoded:
                        valid_nodes.extend([line.strip() for line in decoded.splitlines() if '://' in line])
                except:
                    continue
            return valid_nodes
    except:
        return []
    return []

def main():
    source_url = "https://raw.githubusercontent.com/crashgfw/free-airport-nodes/main/README.md"
    try:
        print("🔭 正在进行最后一次收割尝试...")
        resp = requests.get(source_url, timeout=20)
        links = re.findall(r'https?://fn08\.sp0303\.xyz/nodes/[a-zA-Z0-9]+', resp.text)
        
        all_nodes = set()
        for link in links:
            print(f"尝试读取: {link}")
            nodes = get_real_node_data(link)
            if nodes:
                print(f"   ✨ 发现 {len(nodes)} 个节点")
                all_nodes.update(nodes)
            else:
                print(f"   ⚠️ 未能识别有效内容")
        
        if all_nodes:
            # 重新打包
            final_list = list(all_nodes)
            out_str = "\n".join(final_list)
            b64_out = base64.b64encode(out_str.encode('utf-8')).decode('utf-8')
            with open('targets.txt', 'w', encoding='utf-8') as f:
                f.write(b64_out)
            print(f"🎉 最终成功收割 {len(final_list)} 个节点！")
        else:
            print("🛑 确认：对方已开启动态加密，常规手段失效。")
            
    except Exception as e:
        print(f"💥 出错: {e}")

if __name__ == "__main__":
    main()
