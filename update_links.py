import requests
import re

def main():
    # 方案 A: 尝试访问 Raw 链接
    # 方案 B: 尝试访问 项目主页链接 (如果 Raw 报错)
    urls = [
        "https://raw.githubusercontent.com/crashgfw/free-airport-nodes/main/README.md",
        "https://github.com/crashgfw/free-airport-nodes/blob/main/README.md"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    links = []
    for target in urls:
        try:
            print(f"尝试从 {target} 获取数据...")
            resp = requests.get(target, headers=headers, timeout=15)
            if resp.ok:
                # 提取匹配 fn08.sp0303.xyz/nodes/ 的所有链接
                # 增加对转义字符和 HTML 实体字符的兼容
                found = re.findall(r'https?://fn08\.sp0303\.xyz/nodes/[a-zA-Z0-9]+', resp.text)
                if found:
                    links = list(set(found)) # 去重
                    break
        except Exception as e:
            print(f"访问 {target} 出错: {e}")

    if links:
        # 排序确保顺序一致
        links.sort()
        with open('targets.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(links))
        print(f"✅ 成功！已提取 {len(links)} 个详情页链接。")
    else:
        print("❌ 依然未能发现链接。请手动检查该仓库的 README.md 是否还包含 sp0303.xyz 的链接。")

if __name__ == "__main__":
    main()
