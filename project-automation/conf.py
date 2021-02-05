import os
base_path = os.path.abspath(__file__)
SCRIPT_PATH = os.path.join(os.path.dirname(base_path), "script/script_file")
AUTH = 'http://10.10.10.130:8000/sys/api/auth/'
ASSET_URL = 'http://10.10.10.130:8001/asset/api/'
# 定义redis连接信息
REDIS_CONF = {
    # "password": "",
    "host": "10.10.10.130",
    "port": 6379,
    "db": 1,
    "max_connections":10
}

# 华为云配置
HUAWEIYUN_GLOBAL_URL = 'https://172.16.1.95:7443'
HUAWEIYUN_USERNAME = 'admin'
HUAWEIYUN_PASSWORD = 'Guanli@m0r'

# 华为云PATH
BASIC_URI = '/service'
VERSION_URI = BASIC_URI + '/versions'
LOGIN_URI = BASIC_URI + '/session'
SITE_URI = BASIC_URI + '/sites'

