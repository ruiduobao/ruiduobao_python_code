from urllib.parse import urljoin

# 当前页面的URL
current_url = "http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/44.html"

# 从a标签中获取相对链接
href = "44/4401.html"

# 使用urljoin构建下一级链接
next_url = urljoin(current_url, href)

print(next_url)
#打印结果：http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/44/4401.html