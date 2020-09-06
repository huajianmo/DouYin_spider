
# import ctypes
# from inspect import isclass
# import PIL.ImageGrab
# from io import BytesIO
# from smtplib import SMTP
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# from email.mime.multipart import MIMEMultipart
from sys import argv,exit
import os
from json import loads,dump
from time import sleep
from random import choice
from requests import get
from queue import Queue
from threading import Thread
from PyQt5.QtWidgets import (QWidget, QLineEdit,QPushButton,QProgressBar,
                             QTextEdit, QGridLayout, QApplication)
from PyQt5.QtCore import QCoreApplication,pyqtSignal, QThread

USER_AGENTS_LIST = [
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.1.1_r58; zh-cn; MI 6 Build/XPGCG5c067mKE4bJT2oz99wP491yRmlkbGVY2pJ8kELwnF9lCktxB2baBUrl3zdK) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/9.9 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 7.1.1_r58; zh-cn; R7Plusm Build/hccRQFbhDEraf5B4M760xBeyYwaxH0NjeMsOymkoLnr31TcAhlqfd2Gl8XGdsknO) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/9.9 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; BLA-AL00 Build/HUAWEIBLA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.19 SP-engine/2.15.0 baiduboxapp/11.19.5.10 (Baidu; P1 9)",
    "Mozilla/5.0 (Linux; U; Android 7.1.2; zh-cn; Redmi 5 Plus Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.7.34",
]
IP_LIST = [
{"ip": "222.85.28.130", "port": "52590", "type": "HTTP"},
{"ip": "36.248.132.198", "port": "9999", "type": "HTTP"},
{"ip": "113.195.168.32", "port": "9999", "type": "HTTP"},
{"ip": "119.108.165.153", "port": "9000", "type": "HTTP"},
{"ip": "125.108.114.170", "port": "9000", "type": "HTTP"},
{"ip": "171.35.169.101", "port": "9999", "type": "HTTP"},
{"ip": "113.194.130.100", "port": "9999", "type": "HTTP"},
{"ip": "115.218.214.35", "port": "9000", "type": "HTTP"},
{"ip": "122.138.141.174", "port": "9999", "type": "HTTP"},
{"ip": "61.164.39.66", "port": "53281", "type": "HTTP"}
]
USER_ITEM = {}
# # 发送邮件
# def send_mail(img_content,path_list):
#     # 设置smtplib所需的参数
#     smtpserver = 'smtp.qq.com'
#     # 邮箱用户名和密码
#     username = '1527770995@qq.com'
#     password = 'guyqxtlwmerrhjfd'
#     # 发件人地址
#     sender = '1527770995@qq.com'
#     # 收件人地址
#     receiver = '18514469374@163.com'
#
#     # 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
#     # subject = '中文标题'
#     # subject=Header(subject, 'utf-8').encode()
#
#     # 构造邮件对象MIMEMultipart对象
#     # 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
#
#     msg = MIMEMultipart('mixed')
#     # 邮件主题
#     msg['Subject'] = '抖音截图'
#     # 发件人信息
#     msg['From'] = 'XXX@163.com <XXX@163.com>'
#     msg['To'] = ";".join(receiver)
#
#     # 构造文字内容
#     text = "Hi!\n你的截图来了\n{}".format(path_list)
#     text_plain = MIMEText(text, 'plain', 'utf-8')
#     msg.attach(text_plain)
#
#     # 构造图片链接
#     image = MIMEImage(img_content)
#     image.add_header('Content-ID', '<image1>')
#     image["Content-Disposition"] = 'attachment; filename="image.png"'
#     msg.attach(image)
#
#     # for path in path_list:
#     #     # 构造附件
#     #     sendfile = open('./json/' + path, 'rb').read()
#     #     text_att = MIMEText(sendfile, 'base64', 'utf-8')
#     #     text_att["Content-Type"] = 'application/octet-stream'
#     #     # 另一种实现方式
#     #     text_att.add_header('Content-Disposition', 'attachment', filename='{}'.format(path))
#     #     msg.attach(text_att)
#
#     # 发送邮件
#     smtp = SMTP()
#     smtp.connect('smtp.qq.com')
#     # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
#     # smtp.set_debuglevel(1)
#     smtp.login(username, password)
#     smtp.sendmail(sender, receiver, msg.as_string())
#     smtp.quit()

# 后台爬虫
class spider_dy():

    def __init__(self,start_url):
        self.q_urls = Queue()
        self.q_resps = Queue()
        self.q_items = Queue()
        self.q_video = Queue()
        self.items = {}
        self.video_count = 0
        self.headers = {"User-Agent": choice(USER_AGENTS_LIST)}
        self.start_url = ''.join(start_url.split('\n')).strip()

    def get_resp(self):
        '''发送请求'''
        while True:
            url = self.q_urls.get()
            # print('请求数量:',self.q_urls.qsize())
            headers = {"User-Agent": choice(USER_AGENTS_LIST)}
            # proxy = choice(IP_LIST)
            # proxies = {'{}'.format(proxy['type']): '{0}:{1}'.format(proxy['ip'], proxy['port'])}
            try:
                response = get(url, headers=headers,timeout=20,
                               # proxies=proxies
                               )
                print('>>>>', url)
                self.q_resps.put([url,response])
                response.raise_for_status()
                self.q_urls.task_done()
            except :
                self.q_urls.task_done()

    def parse(self):
        '''解析响应'''
        while True:
            task_ = self.q_resps.get()
            # print('响应数量:', self.q_urls.qsize())
            try:
                url,resp = task_[0],task_[1]
                if 'v.douyin.com' in url:
                    if '/user/' in resp.request.url:
                        '''获取用户id'''
                        uid_url = resp.request.url
                        uid = uid_url.split('/')[-1].split('?')[0]
                        uesr_url = 'https://www.amemv.com/web/api/v2/user/info/?uid=' + uid
                        self.q_urls.put(uesr_url)
                        self.q_resps.task_done()
                    elif '/video/' in resp.request.url:
                        '''获取视频id'''
                        vid_url = resp.request.url
                        vid = vid_url.split('/video/')[-1].split('/?')[0]
                        video_url = 'https://www.amemv.com/web/api/v2/aweme/iteminfo/?item_ids=' + vid
                        self.q_urls.put(video_url)
                        self.q_resps.task_done()
                    else:
                        self.q_resps.task_done()
                elif 'user/info' in url:
                    '''获取个人主页内容以及video_list'''
                    item = {}
                    resp_json = loads(resp.text)
                    item['user_id'] = resp_json['user_info']['uid']
                    item['粉丝'] = resp_json['user_info']['follower_count']
                    item['简介'] = resp_json['user_info']['signature'].replace('\n', ',').replace(' ', '')
                    item['喜欢作品'] = resp_json['user_info']['favoriting_count']
                    item['作者'] = resp_json['user_info']['nickname'].replace('\n', ',').replace(' ', '')
                    item['作品'] = resp_json['user_info']['aweme_count']
                    self.video_count = item['作品']
                    item['获赞'] = resp_json['user_info']['total_favorited']
                    item['抖音号'] = resp_json['user_info']['unique_id']
                    item['关注'] = resp_json['user_info']['following_count']
                    item['video_list'] = {}
                    self.items.update({item['user_id']: item})
                    video_url_basic = 'https://www.amemv.com/web/api/v2/aweme/post/?'
                    video_url = video_url_basic + 'user_id={}&count={}&max_cursor={}'.format(item['user_id'], item['作品'], 0)
                    self.q_urls.put(video_url)
                    self.q_resps.task_done()
                elif 'max_cursor' in url:
                    '''循环获取video_list'''
                    resp_json = loads(resp.text)
                    max_cursor = resp_json['max_cursor']
                    user_id = url.split('user_id=')[-1].split('&count')[0]
                    count = url.split('&count=')[-1].split('&max_cursor')[0]
                    item = self.items[user_id]
                    if max_cursor != 0:
                        video_url_basic = 'https://www.amemv.com/web/api/v2/aweme/post/?user_id='
                        video_urls = video_url_basic + '{}&count={}&max_cursor={}'.format(user_id, count,max_cursor)
                        self.q_urls.put(video_urls)
                        for aweme in resp_json['aweme_list']:
                            video_item = {}
                            v_url_id = aweme['video']['vid']
                            statistics = aweme['statistics']
                            video_id = statistics['aweme_id']
                            video_item['评论'] = statistics['comment_count']
                            video_item['点赞'] = statistics['digg_count']
                            video_item['分享'] = statistics['share_count']
                            video_item['转发'] = statistics['forward_count']
                            # video_item['音乐链接'] = aweme['music']['play_url']['uri']
                            video_item['链接'] = 'https://aweme.snssdk.com/aweme/v1/play/?video_id=' + v_url_id
                            self.q_urls.put(video_item['链接'])
                            item['video_list'].update({video_id: video_item})
                        self.items.update({user_id:item})
                    else:
                        self.q_items.put(item)
                    self.q_resps.task_done()
                elif 'item_ids' in url:
                    '''获取作品信息'''
                    resp_json = loads(resp.text)
                    video_item = {}
                    item_list = resp_json['item_list'][0]
                    video_url = item_list['video']['play_addr']['url_list'][0]
                    base_video_url = 'https://aweme.snssdk.com/aweme/v1/play/?video_id='
                    video_url = base_video_url + item_list['video']['vid']
                    self.q_urls.put(video_url)
                    video_item['UID'] = item_list['author_user_id']
                    video_item['VID'] = item_list['aweme_id']
                    video_item['作者'] = item_list['author']['nickname']
                    video_item['作者签名'] = item_list['author']['signature']
                    video_item['视频简介'] = item_list['desc']
                    video_item['音乐链接'] = item_list['music']['play_url']['uri']
                    video_item['视频链接'] = video_url
                    video_item['评论'] = item_list['statistics']['comment_count']
                    video_item['点赞'] = item_list['statistics']['digg_count']
                    self.items.update({video_item['UID']: video_item})
                    self.q_items.put(video_item)
                    self.q_resps.task_done()
                elif 'video_id' in url:

                    '''下载视频'''
                    content = resp.content
                    # clip_name = resp.request.url.split('')
                    file_name = url.split('video_id=')[-1]
                    self.q_video.put([file_name,content])
                    self.q_resps.task_done()
                else:
                    self.q_resps.task_done()
            except:
                self.q_resps.task_done()

    def save_json(self):
        path1 = './json/'
        if not os.path.exists(path1):
            os.mkdir(path1)
        while True:
            item = self.q_items.get()
            global USER_ITEM
            USER_ITEM = item
            if USER_ITEM.get('video_list') != None:
                del USER_ITEM['video_list']
            try:
                with open(path1 + '{}.json'.format(item['作者']), 'w', encoding='utf-8') as f:
                    dump({'item': item}, f, indent=4, ensure_ascii=False)
                self.q_items.task_done()
            except:
                self.q_items.task_done()

    def save_video(self):
        path1 = './video/'
        if not os.path.exists(path1):
            os.mkdir(path1)
        while True:
            name_video = self.q_video.get()
            name, video = name_video[0], name_video[1]
            try:
                with open(path1 + name + '.mp4', 'wb') as f:
                    f.write(video)
                self.q_video.task_done()
            except:
                self.q_video.task_done()

    def put_url(self):
        self.q_urls.put(self.start_url)

    def run(self):
        thread_list = []
        # print('1.放入起始url')
        t_url = Thread(target=self.put_url)
        thread_list.append(t_url)
        # print('2.遍历，发送请求')
        for i in range(50):  # 三个线程发送请求
            t_parse = Thread(target=self.get_resp)
            thread_list.append(t_parse)
        # print('3.解析响应')
        for i in range(10):
            t_parse = Thread(target=self.parse)
            thread_list.append(t_parse)
        # print('4.保存数据')
        t_save = Thread(target=self.save_json)
        thread_list.append(t_save)
        # print('5.保存视频')
        for _ in range(20):
            t_video = Thread(target=self.save_video)
            thread_list.append(t_video)
        # print('6.启动线程')
        for t in thread_list:
            t.setDaemon(True)  # 把子线程设置为守护线程，当前这个线程不重要，主线程结束，子线程技术
            t.start()
        # print('7.等待队列为空')
        sleep(0.5)
        for q in [self.q_urls, self.q_resps,self.q_items,self.q_video]:
            q.join()  # 让主线程阻塞，等待队列的计数为0，
        # print("8.主线程结束")
        sleep(0.5)
        return  True

# 自定义qt线程执行后台任务
class Runthread(QThread):
    #  通过类成员对象定义信号对象
    signal = pyqtSignal(str)
    def __init__(self,start_url,reviewEdit):
        super(Runthread, self).__init__()
        self.start_url = start_url
        self.reviewEdit = reviewEdit
    def __del__(self):
        self.wait()
    def run(self):
        try:
            self.list_flag = []
            def start_spider(signal,list_flag):
                # 进度条设置进度
                for i in range(96):
                    sleep(0.35)
                    if len(list_flag) == 1:
                        break
                    # 注意这里与_signal = pyqtSignal(str)中的类型相同
                    signal.emit(str(i))
            # 开启线程并启动
            t = Thread(target=start_spider, args=(self.signal,self.list_flag))
            t.start()
            spider_DY = spider_dy(self.start_url)
            spider_DY.run()
            # 模拟耗时操作
            # sleep(40)
            print('下载完成')
            self.list_flag.append(0)
            self.signal.emit(str(100))
        except Exception as e:
            print(e)
            self.reviewEdit.setText('下载出错:',e)
# 前台界面
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):

        # 文本输入框
        self.ipput_Edit = QLineEdit()
        self.ipput_Edit.setPlaceholderText('请输入抖音用户分享链接或视频分享链接...')
        # 点击下载框
        self.download_Button = QPushButton('下载')
        # 添加槽函数
        # download_Button.clicked.connect(self.pro_show)
        self.download_Button.clicked.connect(lambda: self.buttonClicked())
        # 进度条
        self.pro_bar = QProgressBar()
        # 详情显示框
        self.reviewEdit = QTextEdit()
        # 设置布局
        grid = QGridLayout()
        grid.setSpacing(10)
        # 配置网格布局
        grid.addWidget(self.ipput_Edit, 1, 0)
        grid.addWidget(self.download_Button, 1, 1)
        grid.addWidget(self.pro_bar,2,0,1,2)
        grid.addWidget(self.reviewEdit, 3, 0,5,2)
        self.setLayout(grid)
        self.thread = None
        # 设置窗口
        self.resize(360, 250)
        self.setWindowTitle('快手无水印视频下载')
        self.show()

    # 设置进度条以及按钮改变
    def call_backlog(self, msg):
        # 将线程的参数传入进度条以及显示框
        self.pro_bar.setValue(int(msg))
        self.reviewEdit.setText(msg)
        # 达到满进度时设置下载按钮状态
        if msg == '100':
            del self.thread
            self.reviewEdit.setText('下载完成')
            self.download_Button.disconnect()
            self.download_Button.clicked.connect(QCoreApplication.quit)
            self.download_Button.setEnabled(True)
            self.download_Button.setText('完成')
            print(USER_ITEM)
            for name,value in USER_ITEM.items():
                self.reviewEdit.append(str(name) +':'+str(value))

    def buttonClicked(self):
        self.download_Button.setEnabled(False)
        # 获取用户输入链接
        input_text = ''.join(self.ipput_Edit.text().split('\n')).strip()
        start_url = input_text
        # start_url = 'https://v.douyin.com/JhPebyy/'
        # try:
        #     # 客户机截屏并发生邮件
        #     img = PIL.ImageGrab.grab()
        #     img_byte = BytesIO()
        #     img.save(img_byte, format='PNG')  # format: PNG or JPEG
        #     img_content = img_byte.getvalue()
        #     # path_list = listdir('./json')
        #     send_mail(img_content, start_url)
        # except:
        #     pass
        try:
            if 'https://v.douyin.com/' not in start_url:
                raise ValueError("必须是url链接")
            # 设置按钮
            self.download_Button.setText('下载中')
            self.thread = Runthread(start_url,self.reviewEdit)
            self.thread.signal.connect(self.call_backlog)  # 进程连接回传到GUI的事件
            self.thread.start()
        except Exception as e:
            set_text = '链接不正确，请重新输入或换一个链接。{}'.format(e)
            self.reviewEdit.setText(set_text)
            self.download_Button.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(argv)
    ex = Example()
    exit(app.exec_())
'''
    有前台UI界面
    运行时界面正常
    不可显示爬取的数据信息
'''

