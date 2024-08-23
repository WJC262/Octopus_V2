#from openai import OpenAI
import argparse
from langchain_community.llms import Ollama
import re
import requests
import webbrowser    
import cv2

def search_youtube_videos(query):
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)

def take_a_photo(camera):
    # 打开默认摄像头（通常是摄像头 0）
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("无法打开摄像头")
        exit()

    while True:
        # 读取摄像头的一帧
        ret, frame = cap.read()
        
        if not ret:
            print("无法接收帧，程序即将退出")
            break
        
        # 显示帧
        cv2.imshow('摄像头', frame)
        
        # 如果按下 'q' 键，则退出循环
        if cv2.waitKey(1) == ord('q'):
            break

    # 释放摄像头并关闭窗口
    cap.release()
    cv2.destroyAllWindows()

def get_trending_news(query, language = "NULL"):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import base64

def encode_header(s):
    return f"=?utf-8?B?{base64.b64encode(s.encode('utf-8')).decode('utf-8')}?="

def send_email(receiver_email, subject, body):
    sender_email = 'XXX' #填写自己的邮箱
    # 创建一个带附件的实例
    message = MIMEMultipart()
    # 对昵称进行 Base64 编码
    sender_name = encode_header("Jiachen")
    message['From'] = f"{sender_name} <{sender_email}>"
    message['To'] = receiver_email
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    # 发送邮件
    try:
        smtp_server = 'smtp.qq.com'
        server = smtplib.SMTP_SSL(smtp_server, 465)  # 使用SSL连接
        server.login(sender_email, 'wecygzatpvdfcdji')
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)

        
        


# send_email(receiver_email, subject, body)

def identify_nexa(result):
    match = re.search(r'<(nexa_\d+)>', result)
    if match:
        return match.group(1)
    return 'other'

def router(input_text):
    query = f"Below is the query from the users, please call the correct function and generate the parameters to call the function.\n\nQuery: {input_text} \n\nResponse:"
    llm = Ollama(base_url = 'http://localhost:11434', model="octopus-v2-Q4_K_S")
    #llm.bind(stop = "<nexa_end>")
    result = llm.invoke(query, stop = ["Function"])
    print(result)

    nexa_type = identify_nexa(result)
    print(nexa_type)
    # 提取函数名的正则表达式
    function_pattern = re.compile(r"def\s+(\w+)\s*\(")
    #function_match = function_pattern.search(result)

    # 提取函数调用的正则表达式
    call_pattern = re.compile(r"<[^>]*>\('([^']*)'(?:, '([^']*)')?(?:, '([^']*)')?\)<nexa_end>")
    call_match = call_pattern.search(result)

    # 提取函数名
    #function_name = function_match.group(1) if function_match else None

    # 提取变量
    variables = call_match.groups() if call_match else []

    # 打印结果
    #print(f"Function name: {function_name}")
    for i, var in enumerate(variables):
        print(f"Var{i+1}: {var}")
    #for i in variables.size():
    #    print(variables[i])
    #print(len(variables))
    # if variables[0] == "None" and variables[1] == "None" and variables[2] == "None":
    #     size = 0
    # if variables[0] != "None" and variables[1] == "None" and variables[2] == "None":
    #     size = 1
    # if variables[0] != "None" and variables[1] != "None" and variables[2] == "None":
    #     size = 2
    # if variables[0] != "None" and variables[1] != "None" and variables[2] != "None":
    #     size = 3
    size = sum(1 for var in variables if var is not None)
    print(size)

    if nexa_type == 'nexa_4':
        search_youtube_videos(variables[0])
        # if size == 1:
        #     search_youtube_videos(variables[0], variables[1])
        # if size == 2:
        #     search_youtube_videos(variables[0], variables[1], variables[2])
    if nexa_type == 'nexa_0':
        take_a_photo(variables[0])

    if nexa_type == 'nexa_1':
        if size == 0 or size == 1:
            get_trending_news(variables[0])
        if size == 2:
            get_trending_news(variables[0], variables[1])
        # if size == 2:
        #     search_youtube_videos(variables[0], variables[1], variables[2])

    if nexa_type == 'nexa_3':
        if size == 0 or size == 1:
            send_email(variables[0])
        if size == 2:
            send_email(variables[0], variables[1])
        if size == 3:
            send_email(variables[0], variables[1], variables[2])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'question')
    parser.add_argument('input_text', type = str)

    args = parser.parse_args()
    # url = f"https://www.google.com/search?q={'中国'}"
    #webbrowser.open(url)

    # cap = cv2.VideoCapture(0)
    # if not cap.isOpened():
    #     print("无法打开摄像头")
    #     exit()
    # while True:
    #     # 读取摄像头的一帧
    #     ret, frame = cap.read()
        
    #     if not ret:
    #         print("无法接收帧，程序即将退出")
    #         break

    #     cv2.imshow('摄像头', frame)

    #     if cv2.waitKey(1) == ord('q'):
    #         break

    # cap.release()
    # cv2.destroyAllWindows()
    
    router(args.input_text)