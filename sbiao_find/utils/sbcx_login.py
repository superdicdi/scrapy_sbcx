import requests
import cookielib

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        "Host": "sbcx.com",
        "Referer": "http://sbcx.com/"
        }

def sb_login(username, pwd):
    post_url = "http://sbcx.com/?m=Mod&mod=Sys_Login&act=in&reurl=&mid=log_1"

    post_data = {
        "username": username,
        "pwd": pwd,
        "reurl": "%2F",
        "func": 0
    }
    response = session.post(post_url, data=post_data, headers=headers)
    session.cookies.save()
    print(response)

sb_login("18610379194", "tuyue7208562")