# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import os
import time
import requests
import urllib
from tqdm import tqdm
from get_text import parse_result


os.chdir("./")
lfasr_host = 'https://raasr.xfyun.cn/v2/api'
# 请求的接口名
api_upload = '/upload'
api_get_result = '/getResult'


class RequestApi(object):
    def __init__(self, appid, secret_key, upload_file_path):
        self.appid = appid
        self.secret_key = secret_key
        self.upload_file_path = upload_file_path
        self.ts = str(int(time.time()))
        self.signa = self.get_signa()

    def get_signa(self):
        appid = self.appid
        secret_key = self.secret_key
        m2 = hashlib.md5()
        m2.update((appid + self.ts).encode('utf-8'))
        md5 = m2.hexdigest()
        md5 = bytes(md5, encoding='utf-8')
        # 以secret_key为key, 上面的md5为msg， 使用hashlib.sha1加密结果为signa
        signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        return signa

    def upload(self):
        # print("上传部分：")
        upload_file_path = self.upload_file_path
        file_len = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)


        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict["fileSize"] = file_len
        param_dict["fileName"] = file_name
        param_dict["duration"] = "200" # 当前未验证，可随机传一个数字
        param_dict["pd"] = "medical" # 领域个性化参数
        param_dict["roleType"] = 1 # 开启角色分离功能
        param_dict["roleNum"] = 2 # 说话人数
        # print("upload参数：", param_dict)
        with open(upload_file_path, 'rb') as f:
            data = f.read(file_len)

        response = requests.post(url=lfasr_host + api_upload + "?" + urllib.parse.urlencode(param_dict),
                                 headers={"Content-type": "application/json"}, data=data)
        # print("upload_url:", response.request.url)
        result = json.loads(response.text)
        # print("upload resp:", result)
        return result

    def get_result(self):
        upload_file_path = self.upload_file_path
        uploadresp = self.upload()
        orderId = uploadresp['content']['orderId']
        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict['orderId'] = orderId
        param_dict['resultType'] = "transfer,predict"
        # print("")
        # print("查询部分：")
        # print("get result参数：", param_dict)
        status = 3


        # 建议使用回调的方式查询结果，查询接口有请求频率限制
        while status == 3:
            response = requests.post(url=lfasr_host + api_get_result + "?" + urllib.parse.urlencode(param_dict),
                                        headers={"Content-type": "application/json"})
            result = json.loads(response.text)
            status = result['content']['orderInfo']['status']
            if status == 4:
                break
            time.sleep(5)

        # print("get_result resp:", result)

        # 将 json 结果写入文件
        # with open(self.output_file_path, 'w', encoding='utf-8') as f:
        #     f.write(json.dumps(result, ensure_ascii=False, indent=4))

        # print(f"转录成功,音频文件{upload_file_path}已转录至{output_file_path}")

        print('已成功获取json格式,正在格式化...')

        return result

def start(appid, secret_key, pload_file_path, output_file_path):
    api = RequestApi(appid,
                    secret_key,
                    upload_file_path=pload_file_path)
    
    try:
        Authentication = parse_result(api.get_result(), output_file_path)
    except KeyError:
        print("转录失败,请输入正确的密钥")

# 输入讯飞开放平台的appid，secret_key和待转写的文件路径
if __name__ == '__main__':
    api = RequestApi(appid="",
                     secret_key="",
                     upload_file_path=r"/mntcephfs/lab_data/youjiajun/Tdata_降噪/test/output1.wav",
                     output_file_path=r"/home/youjiajun/result.json")

    parse_result(api.get_result(), "/home/youjiajun/result.txt")

    # api.get_result()
    
