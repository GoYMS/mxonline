import  requests
import json
#测试发送短信


#通过云片网接口知道这三个参数是必填，第一个参数为云片网上的apikey值，第二个为发送验证码，第三个是手机号
def send_single_sms(apikey,code,mobile):
    #测试发送单条短信
    url = 'https://sms.yunpian.com/v2/sms/single_send.json'
    text = "【李皓琳】您的验证码是{0}。如非本人操作，请忽略本短信".format(code)
    res = requests.post(url,data={
        "apikey":apikey,
        "mobile":mobile,
        "text":text
    })
    re_json = json.loads(res.text)
    return re_json

if __name__ == '__main__':
    #第一个参数是
    res = send_single_sms("5c978b33eaccc2137a76b08dbd730dc7",462378,15515819567)
    import json
    res_json = json.loads(res.text)
    code = res_json["code"]
    msg = res_json["msg"]
    if code == 0:
        print("发送成功")
    else:
        print("发送失败: {}".format(msg))
    print(res.text)
