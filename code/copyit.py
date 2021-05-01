import requests
import re
class Baidu_Translate(object):
  def __init__(self, query_string):
    self.query_string = query_string
    self.url_1 = 'https://fanyi.baidu.com/sug'
    # self.url = 'https://fanyi.baidu.com/v2transapi' # 这里不能用这个地址，因为对方采用了反爬虫措施，访问这个地址是人家是不会给你任何数据的
    self.url_0 = 'https://fanyi.baidu.com/transapi'
    self.zh_pattern = re.compile('[\u4e00-\u9fa5]+')
    self.headers = {
      'Accept': '* / *',
      'Accept - Encoding': 'gzip, deflate',
      'Accept - Language': 'zh-CN, zh; q=0.9',
      'Connection': 'keep - alive',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
      'X-Requested-With': 'XMLHttpRequest',
    }
  def get_post_data(self):
    """
    拿到 post 请求上传的参数，并判断输入类型并予以返回
    :return: 查询词
    """
    if re.search(pattern=self.zh_pattern, string=self.query_string): # 输入的内容含有中文，则判别其为中文输入
      return {
      "from": "zh",
      "to": "en",
      "kw": self.query_string, # 模糊查询 url_1关键词
      "query": self.query_string, # 精准查询 url_0关键词
    }
    else:
      return {
      "from": "en",
      "to": "zh",
      "kw": self.query_string, # 模糊查询 url_1关键词
      "query": self.query_string, # 精准查询 url_0关键词
      }
  def request_translate(self):
    """
    向百度请求 json 数据
    :return: 向百度请求的 json 数据
    """
    data = self.get_post_data()
    try:
      response_0 = requests.request(method="post", url=self.url_0, headers=self.headers, data=data).json()
    except Exception: # 进行数据请求的任何异常处理
      response_0 = ''
    try:
      response_1 = requests.request(method="post", url=self.url_1, headers=self.headers, data=data).json()
    except Exception: # 进行数据请求的任何异常处理
      response_1 = ''
    return response_0, response_1
  def parse_translate_data(self):
    """
    数据解析，将请求到的翻译内容解析并输出
    :return: None
    """
    response_0 = self.request_translate()[0]
    response_1 = self.request_translate()[1]
    # item = response_0
    if response_0:
      item = response_0.get('data')[0].get('dst')
      print('key word:', self.query_string, '\t', 'translate:', item)
    if response_1:
      data = response_1.get('data')
      for item in data[:1]: # 长度一般为5，这里只保留其释义
        k = 'key word: \t[ {key} ]'.format(key=item.get('k'))
        v = 'value: \t\t[ {value} ]'.format(value=item.get('v'))
        return k,v
    # print(response_1.get('data'))
 
def getword(kw):
    query_keywords = kw
    if query_keywords == '':
        return '没有选取单词','翻译不行'
    else:
        baidu = Baidu_Translate(query_string=query_keywords)
        return baidu.parse_translate_data()
 
 
 
import pyWinhook
import pythoncom
import pyautogui
import pyperclip
import tkinter as tk
# 监听到鼠标事件调用
p = []
key = '2'
v = ''
mwin = tk.Tk()
mwin.wm_attributes('-topmost',1)
mwin.geometry("600x50")
mwin.title('code Helper')
n1 = tk.Entry(mwin,width = 150)
n2 = tk.Entry(mwin,width = 150)
 
n1.pack()
n2.pack()
def onMouseEvent(event):
    if (event.MessageName != "mouse move"):  # 因为鼠标一动就会有很多mouse move，所以把这个过滤下
        if event.MessageName == 'mouse left up':
            p.append(pyautogui.position())
            pyautogui.hotkey('ctrl','c')
            s = pyperclip.paste()
            global key
            global v
            try:
                key,v =getword(s)
            except:
                key = 'null'
                v = 'null'
            n1.delete(0,'end')
            n2.delete(0,'end')
            n1.insert(0, key)
            n2.insert(0,v)
    return True # 为True才会正常调用，如果为False的话，此次事件被拦截
# 监听到键盘事件调用
def onKeyboardEvent(event):
    #print(event.Key)  # 返回按下的键
    if event.Key == 'Q':
        event = quit()
    return True
def end(event):
    event = quit()
def main():
    # 创建管理器
    hm = pyWinhook.HookManager()
     # 监听键盘
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    # 监听鼠标
    hm.MouseAll = onMouseEvent
    hm.HookMouse()
    mwin.mainloop()
    end(hm)
    # 循环监听
    pythoncom.PumpMessages()
 
if __name__ == "__main__":
    main()