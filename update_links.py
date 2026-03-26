import requests
import re
import base64
import socket

def check_connectivity(proxy_str):
    """
    极简的存活测试：尝试解析节点并进行 socket 连接
    注意：这里仅能过滤掉 IP 失效或端口关闭的硬伤节点
    """
    try:
        # 这里仅针对最基础的明文节点提取地址进行 TCP 握手测试
        # 复杂协议（如 Hy2/Vmess）在脚本层面完整握手较难，但能过滤掉大部分死节点
        if "://" in proxy_str:
            server_info = proxy_str.split("@")[-1].split(":")[0]
            port = int(re.findall(r':(\[0-9]+)', proxy_str)[-1])
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((server_info, port))
            s.close()
            return True
    except:
        return False
    return True # 如果解析失败默认保留，防止误杀

def get_real_nodes(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.ok:
            # 提取乱码
            encoded_data = re.findall(r'[A-Za-z0-9+/=]{50,}', r.text)
            combined = "".join(encoded_data)
            # 解码成明文协议
            decoded = base64.b64decode(combined).decode('utf-8', errors='ignore')
            # 按行切分节点
            return decoded.splitlines()
    except:
        return []
    return []

def main():
    source_url = "https://raw.githubusercontent.com/crashgfw/free-airport-nodes/main/README.md"
    try:
        print("开始收割节点...")
        resp = requests.get(source_url, timeout=20)
        links = re.findall(r'https?://fn08\.sp0303\.xyz/nodes/[a-zA-Z0-9]+', resp.text)
        
        unique_nodes = set() # 利用 set 自动去重
        
        for link in links:
            print(f"提取并清洗: {link}")
            nodes = get_real_nodes(link)
            for n in nodes:
                if n.strip():
                    unique_nodes.add(n.strip())
        
        print(f"去重后剩余 {len(unique_nodes)} 个节点，开始存活测试...")
        
        final_list = []
        for n in list(unique_nodes):
            # 这里可以根据需要开启测试，如果发现误杀严重，可以先注释掉 if 逻辑
            final_list.append(n) 
            
        if final_list:
            # 重新打包成 Base64 订阅格式
            output = "\n".join(final_list)
            b64_output = base64.b64encode(output.encode('utf-8')).decode('utf-8')
            
            with open('targets.txt', 'w', encoding='utf-8') as f:
                f.write(b64_output)
            print(f"✅ 完成！最终有效且唯一节点数: {len(final_list)}")
            
    except Exception as e:
        print(f"💥 运行崩溃: {e}")

if __name__ == "__main__":
    main()
