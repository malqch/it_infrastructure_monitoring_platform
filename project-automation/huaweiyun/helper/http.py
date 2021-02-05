import requests
import urllib3
import logging
import traceback

logger = logging.getLogger('log')
urllib3.disable_warnings()

class HttpHelper(object):

    def __init__(self):
        pass

    @staticmethod
    def get(url, headers):
        """
        HTTP GET 方法
        :param url: 请求地址
        :param headers: 请求头
        :return:
        """
        if headers:
            # 发送请求
            try:
                result = requests.get(url=url, headers=headers, verify=False, timeout=60)
                return result.status_code, result.json()
            except Exception as e:
                logger.info(e.message)
                logger.info(traceback.format_exc())
                result = {'msg': f'查询失败:{str(e)}'}
                return 500, result
        else:
            result = {'msg': '华为云登录失败！'}
            return 500, result

    @staticmethod
    def post(url, headers, data=None):
        """
        HTTP POST方法
        :param url: 请求地址
        :param data: 请求参数
        :param headers: 请求头
        :return:
        """
        if headers:
            try:
                result = requests.post(url=url, headers=headers, data=data, verify=False, timeout=60)
                return result.status_code, result.json()
            except Exception as e:
                logger.info(e.message)
                logger.info(traceback.format_exc())
                result = {'msg': f'操作失败:{str(e)}'}
                return 500, result
        else:
            result = {'msg': '华为云登录失败！'}
            return 500, result

    @staticmethod
    def put(url, headers, params=None):
        """
        HTTP PUT方法
        :param url: 请求地址
        :param params: 请求参数
        :param headers: 请求头
        :return:
        """
        if headers:
            try:
                result = requests.post(url=url, headers=headers, data=params, verify=False, timeout=60)
                return result.status_code, result.json()
            except Exception as e:
                logger.info(e.message)
                logger.info(traceback.format_exc())
                result = {'msg': f'更新失败:{str(e)}'}
                return 500, result
        else:
            result = {'msg': '华为云登录失败！'}
            return 500, result

    @staticmethod
    def patch(url, headers, params=None):
        """
        HTTP PATCH方法
        :param url: 请求地址
        :param params: 请求参数
        :param headers: 请求头
        :return:
        """
        if headers:
            try:
                result = requests.post(url=url, headers=headers, data=params, verify=False, timeout=60)
                return result.status_code, result.json()
            except Exception as e:
                logger.info(e.message)
                logger.info(traceback.format_exc())
                result = {'msg': f'请求失败:{str(e)}'}
                return 500, result
        else:
            result = {'msg': '华为云登录失败！'}
            return 500, result

    @staticmethod
    def delete(url, headers):
        """
        HTTP DELETE方法
        :param url: 请求地址
        :param headers: 请求头
        :return:
        """
        if headers:
            try:
                result = requests.delete(url=url, headers=headers, verify=False, timeout=60)
                return result.status_code, result.json()
            except Exception as e:
                logger.info(e.message)
                logger.info(traceback.format_exc())
                result = {'msg': f'删除失败:{str(e)}'}
                return 500, result
        else:
            result = {'msg': '华为云登录失败！'}
            return 500, result

