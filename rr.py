#原作者：happy knva
#精简：@yyfyy123
#增加推送：@vesugier
#多账号推送相关正则参考 @ookamisk

from telethon import TelegramClient, events
import requests, re, time, os

api_id = 2747876
api_hash = '941436b0f5621e6376bb673bf554ce19'
tg_user_id = '380135603'
tg_bot_token = '1382415388:AAHFvi_TXxCbv8B_31_KLZpkZe684beCWCA'
output_msg = True # 是否打印消息
channel_white_list = [1001427039780] # 过滤频道消息
cookies = [
        "pt_key=AAJgMa4MADDFfJDuXb1Qvq9oY9597lrhgQwYLB7VclBxyBTtxy7i9yCCJ9R5zSq5FUghco05QlA;pt_pin=toyfun;",
        "pt_key=AAJgS0hrADAc4aoyjMejHZKR8uNbxLUEo6MDdDhLhPpWOwI6Zhq2zy8JJcWRBw0Q_R1skWjxjnY;pt_pin=shuoshuo0405;",
        "pt_key=AAJgPXfIADBKUQwFyas0BRxi0Y2if2uqCrBXApAC7g_ysF1fUoj3KrrwtArwG4457FSXvIHTtgk;pt_pin=jd_5f100403d4fa7;",
        "pt_key=AAJgSZsCADAsNj-e29JFW7YabpLGLOyoYXNG4koE4kFsUl0xioRvJ6XzJRSltKrLW-HVIGyZkzI;pt_pin=520161323_m;",
        "pt_key=AAJgM6-KADD0bvwMx9egiRPlsKEk6JXVf-CD3XiEY6pgXdD7hNCjAwHM-FD7orn63vb7-2XxKgw;pt_pin=jd_52177145561f1;",
        "pt_key=AAJgSeKAADCNoXlcRcO3PJWr9MrXfkpsHeOSvk7BXZGYcO3sazQjFIfChLDcWeq-_wfD80NWn04;pt_pin=%E5%BE%90%E6%97%A9%E6%97%A90925;",
        "pt_key=AAJgSeG0ADDqnmYljIoAhiI6TGwd-bmbstJVLve3WCywRyKM8Jq_WmRlPuXb-057Foz1LVr7occ;pt_pin=jd_593a4fd8dfd70;",
        ""
        ]

proxies={ #tg推送用代理，不需要的请删除72行proxies参数或者取消73行注释 注释72行
        'http':'http://127.0.0.1:7890',
        'https':'http://127.0.0.1:7890'
        }

regex = re.compile(r"(https://api.m.jd.com.*)\)", re.M)

client = TelegramClient(
        'your session id',
        api_id,
        api_hash
        )

headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1",
        "Cookie": "",
        }

cookiesRegex = re.compile(r'pt_pin\=(.*?)',re.S)

f = open("push.txt","w")
f.write(" ")
f.close()

def get_bean(url):
    for cookie in cookies:
        headers["Cookie"] = cookie
        pt_pin = re.findall(cookiesRegex, cookie)
        res = requests.get(url, headers=headers).json()
        if int(res['code']) != 0:
            print("cookie无效")
        else:
            print(res['data']['awardTitle'], res['data']['couponQuota'])
        desp = ''
        desp += '账号:【'+pt_pin[0]+'】{} {}\n'.format(res['data']['awardTitle'], res['data']['couponQuota'])
        if "None" in desp:
            continue
        else:
            f=open("push.txt","a")
            f.write(desp)
            f.close

def push():
    print("tg")
    f = open("push.txt","r")
    text = f.read()
    f.close()
    msg ={
        'chat_id': {tg_user_id},
        'text': f'直播间京豆\n\n{text}',
        'disable_web_page_preview': 'true'
        }
    #requests.post(url=f'https://api.telegram.org/bot{tg_bot_token}/sendMessage', data=msg, timeout=15,proxies=proxies).json()
    requests.post(url=f'https://api.telegram.org/bot{tg_bot_token}/sendMessage', data=msg, timeout=15).json()
    f = open("push.txt","w")
    f.write(" ")
    f.close()

@client.on(events.NewMessage(chats=[-1001427039780], from_users=[1663824060]))
@client.on(events.NewMessage(chats=[-1001212172599]))
async def my_event_handler(event):
    # if event.peer_id.channel_id not in channel_white_list :
    #     return
    jdUrl = re.findall(regex, event.message.text)
    count = len(open("push.txt", 'r').readlines())
    if output_msg:
        print(event.message.text)
    if len(jdUrl) == 1:
        get_bean(jdUrl[0])
    if count > 10 :
        push()



with client:
    client.loop.run_forever()
