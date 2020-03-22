from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import selenium
import time
import re
import json




class DataSpider(object):

    def __init__(self, campaign_id):
        '''
        DataSpider对象最重要的attribute就是campaign_id
        :param campaign_id: 以campaign_id为key来连接系统和本地
        '''
        #读取配置文件
        #read config file
        with open("config.json", "r", encoding='utf-8') as f:
            config = json.loads(f.read())    # load的传入参数为字符串类型

        self.campaign_id = campaign_id
        box_list = []
        for i in range(12):
            box_list.append('__box7-'+str(i))
        self.box_list = box_list
        self.index = ['Sent', 'Hard Bounces', 'Soft Bounces', 'Delivered', 'Opened', 'Unique Click', 'Click']
        self.rate_list = ['Bounce Rate', 'Opened Messages in %', 'CTR', 'Unique CTR', 'Click-To-Open Rate']
        self.data_dic = {}
        self.total_click_list = []    #所有link的数据及名称
        self.main_click_list = []     #主要link的数据及名称
        self.other_click_list = []    #其他link的数据及名称
        self.overall_data = {}
        #初始化driver
        desired_capabilities = DesiredCapabilities().CHROME
        desired_capabilities['pageLoadStrategy'] = 'eager'

        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

        driver = webdriver.Chrome(options=chrome_options,
                                  executable_path=r'C:\Users\C5293427\Desktop\MA\chromedriver_win32\chromedriver.exe',
                                  desired_capabilities=desired_capabilities)  # chrome_driver的执行文件

        driver.delete_all_cookies()
        self.driver = driver
        self.other_link = config['other_link'] #从配置文件中读取其他link的名字

    def get_campaign_id(self):
        '''
        :return: get方法
        '''
        return self.campaign_id

    def get_box_list(self):
        '''
        :return: get方法
        '''
        return self.box_list

    def get_index(self):
        '''
        :return: get方法
        '''
        return self.index

    def get_rate_list(self):
        '''
        get方法
        :return:
        '''
        return self.rate_list

    def get_data_dic(self):
        '''
        get方法
        :return:
        '''
        return self.data_dic

    def get_total_click_list(self):
        '''
        get方法
        :return:
        '''
        return self.total_click_list

    def get_driver(self):
        '''
        get方法，一般不用这个方法，一般以self.driver直接操作
        :return:
        '''
        return self.driver

    def get_other_link(self):
        return self.other_link

    def get_main_click_list(self):
        return self.main_click_list

    def get_other_click_list(self):
        return self.other_click_list

    def get_overall_data(self):
        return self.overall_data

    def url(self):
        '''
        通过campaign_id获得url
        :return: url地址
        '''
        campaign_id = str(self.get_campaign_id())
        url = r'https://my300723.s4hana.ondemand.com/ui#Initiative-manageCampaignFlow?Tab=PERFORMANCE&/CampaignObject/000000'+campaign_id+'/1'
        return url

    def catch_number(self, sentence):
        '''
        辅助方法
        :param sentence: 给定一个句子，也就是相应的title
        :return: 得到index对应的数字
        '''
        sentence = sentence.replace(',', '') #将逗号去除
        number = re.search('\d+', sentence).group()
        number = int(number)
        return number

    def judge_index(self, sentence):
        '''
        判断一个句子是不是表示index，若index，则True；若Rate，则False
        :param sentence: 是相应的title
        :return:
        '''
        index = self.get_index()
        rate_list = self.get_rate_list()
        for i in rate_list:
            if i in sentence:
                return False
        return True

    def judge_load_page(self, id, attempt_num=30, interval_time=5):
        '''
        :param id: 新页面特有的id，通过判断它来判断页面是否跳转了
        :param attempt_num: 尝试次数，到达上限后放弃，并报错
        :param interval_time: 尝试的间隔时间
        :return: 若通过则无返回，若不通过则raise error
        '''

        url = self.url()
        count = 0

        for i in range(attempt_num):
            try:
                self.driver.find_element_by_id(id)
                break
            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(interval_time)
                self.driver.get(url)
            count += 1
        if count == attempt_num:
            raise RuntimeError('未跳转异常，请检查跳转操作！')

    def try_click(self, id, attempt_num=30, interval_time=5):
        '''

        :param id: 要点击的按钮
        :param attempt_num:
        :param interval_time:
        :return: 原理与judge_load_page一样，不再赘述
        '''
        url = self.url()
        count = 0
        for i in range(attempt_num):
            try:
                self.driver.find_element_by_id(id).click()
                break
            except:
                time.sleep(interval_time)
                self.driver.get(url)
            count += 1

        if count == attempt_num:
            raise RuntimeError('点击操作异常，点不到按钮，请检查点击操作！')


    def find_table_element(self):
        '''
        利用selenium直接抓取所有页面内的td元素
        :return:一个列表，形如：[(46,'SAP 天天事'),(3, 'GDPR注册')]
        '''

        row = self.driver.find_elements_by_tag_name('tr')
        list = []
        for i in row:
            j = i.find_elements_by_tag_name('td')
            for item in j:
                text = item.text
                list.append(text)

        list = self.single2tuple(list)
        return list

    def find_last_td(self):
        '''
        要找到最后一个td对象，方便点击
        :return: selenium那个什么对象，后面用来点的
        '''
        row = self.driver.find_elements_by_tag_name('tr')
        for i in row:
            j = i.find_elements_by_tag_name('td')
            for item in j:
                pass
        return item


    def single2tuple(self, old_list):
        '''
        抓click data的辅助函数
        :param element_list: ['GDPR注册',1,'立即报名',29,'SAP 天天事', 7]
        :return: [('GDPR注册',1),('立即报名',29),('SAP 天天事', 7)]
        '''
        new_list = []
        num = len(old_list)
        if num % 2 != 0:
            raise RecursionError('抓表格元素的时候出现单数了！')
        elif num == 0:
            return []

        for i in range(len(old_list)):
            if i % 2 == 0:
                try:
                    new_list.append((int(old_list[i]), old_list[i+1]))
                except ValueError:
                    new_list.append((old_list[i], old_list[i + 1]))
            else:
                continue

        return new_list

    def absorb_element(self, total_list, new_list):
        '''
        抓click data的辅助函数：多屏元素的收纳
        :param total_list: 存储着过往的所有元素
        :param added_list: 新抓来的元素列表
        :return: 一个列表，包含两个列表中的所有非重复元素
        '''
        for i in new_list:
            if i not in total_list:
                total_list.append(i)

        return total_list

    def scroll_down(self, num=6):
        '''
        抓click data的辅助函数：为表格翻页
        :return: 不需要return
        '''
        item = self.find_last_td()
        item.click()
        for i in range(num):
            item.send_keys(Keys.DOWN)
        return

    def pure_list(self, list):
        '''
        去除列表中的重复元素
        :param list: 输入列表
        :return: 一个没有重复元素的列表
        '''
        new_list=[]
        for i in list:
            if i not in new_list:
                new_list.append(i)
        return new_list

    def click_data_sort(self, list):
        '''
        click data的辅助函数
        利用insertion sort, 它适用于小input
        :param list: 形如[('GDPR注册',1),('立即报名',29),('SAP 天天事', 7)]
        :return: [('立即报名',29),('SAP 天天事', 7),('GDPR注册',1)]
        '''
        for j in range(1, len(list)):
            key = list[j]
            i = j-1
            try:
                while i >= 0 and list[i][0] < key[0]:
                    list[i+1] = list[i]
                    i = i-1
                list[i+1] = key
            except TypeError:
                raise TypeError('有链接的点击数不为int，请查看！')

        return list



    def click_data_process(self, list):
        '''
        click data被保存在列表中，所以输入是一个列表
        此方法的作用：(1)去重；（2）去除我们讨厌的元素
        :param list: 以元组的形式储存每一对数据
        :return:
        '''
        hate_list = [('Clicks', 'Content Link Name'), (0, ''), ('', '')]
        new_list = []
        for i in list:
            if (i not in new_list) and (i not in hate_list):
                new_list.append(i)

        new_list = self.click_data_sort(new_list)

        return new_list

    def click_data_split(self):
        '''
        此方法的作用是讲total_click_list分成main_click_list和other_click_link,储存在self中
        :return: None
        '''
        total_click_list = self.get_total_click_list()
        other_link = self.get_other_link()

        for item in total_click_list:
            if item[1] in other_link:
                self.other_click_list.append(item)
            else:
                self.main_click_list.append(item)
        return

    def collect_overall_data(self):
        '''
        用于存储json文件
        '''
        dic = {}
        dic['total_click_list'] = self.get_total_click_list()
        dic['main_click_list'] = self.get_main_click_list()
        dic['other_click_list'] = self.get_other_click_list()
        dic['data_dic'] = self.get_data_dic()
        self.overall_data = dic
        return
    

    def save_json(self):
        '''
        存储json文件
        '''
        overall_data = self.get_overall_data()
        campaign_id = int(self.get_campaign_id())
        
        filename = r'C:\Users\C5293427\Desktop\MA\campaign_data\data.json'

        with open(filename) as f_obj:
            dic = json.load(f_obj)
        
        dic[campaign_id] = overall_data

        with open(filename, 'w') as f_obj:
            json.dump(dic, f_obj)
        return

    

    def scratch_data(self):
        '''
        这是最终的组合版本，好比乐高的零件已经齐备，现在开始组装
        :param attempt_number: 尝试次数默认30次，每次尝试间隔5 seconds。
        :return: 得到最终的数据字典。
        '''

        box_list = self.get_box_list() #这个是每个格子（box）的id列表
        index = self.get_index()   #index的关键字

        url = self.url() #初始化url
        self.driver.get(url)

        self.judge_load_page('__box7-0')

        # data_dic 这里得到基本数据
        data_dic = {}   #初始化数据字典
        for i in box_list:
            try:
                sentence = self.driver.find_element_by_id(i).get_attribute('title')
            except selenium.common.exceptions.NoSuchElementException:
                continue
            if self.judge_index(sentence):    #去除rate的干扰
                for index_item in index:
                    if index_item in sentence:  #eg:如果unique clicks在句子中，它就归为unique clicks这类,注意：unique clicks永远比clicks优先判断，之后立刻break
                        number = self.catch_number(sentence)
                        data_dic[index_item] = number
                        break

        #这里开始跳转页面
        time.sleep(3)   #抓好上述数据后，留出5 seconds时间加载
        self.try_click('success_frag--tableButton-button')   #不断点击按钮

        #while语句在检查点击后是否成功跳转
        runtime = 0
        for i in range(30):
            try:
                test_jump = self.driver.find_element_by_id('successTableFragment--smartSuccessTable-header-inner')
            except selenium.common.exceptions.NoSuchElementException:
                self.try_click('success_frag--tableButton-button')
                time.sleep(3)
                runtime += 1
                if runtime == 30:
                    raise RuntimeError('页面跳转异常，点到按钮了，但无法跳转！')
        #检查完毕
        #获取data view页面的源代码
        time.sleep(3)

        #找到表格，第一屏的数据存储在表格中
        total_list = self.find_table_element()
        #开始循环，每次按6次向下按钮，开始读数据，直到最后到底（total_list的长度不再发生变化）
        while True:
            self.scroll_down(6)
            new_list = self.find_table_element()
            total_list = self.absorb_element(total_list=total_list, new_list=new_list)
            #检验total_list的长度是否有变化，count代表上一次循环结束时total_list的长度。即判断循环何时停止。
            try:
                if count == len(total_list):
                    break
            except UnboundLocalError:
                count = len(total_list)
            count = len(total_list)

        total_list = self.click_data_process(total_list)  #去除重复元素和讨厌的元素，例如空值

        self.data_dic = data_dic
        self.total_click_list = total_list
        self.click_data_split()  #拆出两个列表，分别为主要链接和其他链接
        self.collect_overall_data()
        self.save_json()
        self.driver.close()

        return data_dic, total_list


if __name__ == '__main__':

    spider = DataSpider(4708)
    spider.scratch_data()
    print(spider.get_total_click_list())
    print(spider.get_data_dic())
    print(spider.get_main_click_list())
    print(spider.get_other_click_list())














