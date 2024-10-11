import requests
import json

# API的URL
url = 'https://curator.jsc.nasa.gov/rest/lunarapi/samples/samplesbyclassification/Basalt'

# 发送GET请求
response = requests.get(url)

# 检查响应状态码
if response.status_code == 200:
    # 解析JSON数据
    data = response.json()

    # 打印数据，或进行其他处理
    print(json.dumps(data, indent=4))  # 美化打印JSON数据
else:
    print("Failed to retrieve data:", response.status_code)
