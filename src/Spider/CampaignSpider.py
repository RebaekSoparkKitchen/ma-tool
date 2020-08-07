'''
@Description: 
@Author: FlyingRedPig
@Date: 2020-05-01 17:58:32
@LastEditors: FlyingRedPig
@LastEditTime: 2020-08-06 10:34:27
@FilePath: \EDM\src\Spider\CampaignSpider.py
'''

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import selenium
import time
import json
from src.Control.MA import MA


class CampaignSpider(MA):

    def __init__(self, campaignId, driver=None):
        '''
        @description: 
        @param {type} campaignId:是最重要的参数，其他类请求服务的时候要用它作为键值请求；driverPath:指定chrome_driver的地址
        @return: 
        '''
        super().__init__()
        self.campaignId = campaignId
        self.driverPath = self.readConfig()['chrome_driver']
        self.driver = driver

    def getCampaignId(self):
        return self.campaignId

    def getDriverPath(self):
        return self.driverPath

    def setCampaignId(self, campaignId):
        self.campaignId = campaignId
        return

    def initDriver(self):
        '''
        @description: 
        @param {type} 
        @return: 
        '''
        driverPath = self.getDriverPath()

        desired_capabilities = DesiredCapabilities().CHROME
        desired_capabilities['pageLoadStrategy'] = 'eager'

        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches',
                                               ['enable-automation'])

        driver = webdriver.Chrome(
            options=chrome_options,
            executable_path=driverPath,
            desired_capabilities=desired_capabilities)  # chrome_driver的执行文件

        driver.delete_all_cookies()
        driver.maximize_window()
        self.driver = driver
        return

    def closeDriver(self):
        self.driver.close()
        return

    def url(self):
        '''
        通过campaignId获得url
        :return: url地址
        '''
        campaignId = str(self.getCampaignId())
        url = r'https://my300723.s4hana.ondemand.com/ui#Initiative-manageCampaignFlow?Tab=PERFORMANCE&/CampaignObject/000000' + campaignId + '/1'
        return url

    def ifLoadPage(self, id, attemptNum=30, intervalTime=5) -> None:
        '''
        :param id: 新页面特有的id，通过判断它来判断页面是否跳转了
        :param attemptNum: 尝试次数，到达上限后放弃，并报错
        :param intervalTime: 尝试的间隔时间
        :return: 若通过则无返回，若不通过则raise error
        '''
        count = 0
        while True:
            try:
                self.driver.find_element_by_id(id)
                break
            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(intervalTime)
            count += 1
            if count == attemptNum:
                raise RuntimeError('未跳转异常，请检查跳转操作！')

    def click(self, id, attemptNum=60, intervalTime=1):
        '''
        :param id: 要点击的按钮
        :param attemptNum:
        :param intervalTime:
        :return: 原理与ifLoadPage一样，不再赘述
        '''
        count = 0
        while True:
            try:
                self.driver.find_element_by_id(id).click()
                break
            except:
                time.sleep(intervalTime)
            count += 1
            if count == attemptNum:
                raise RuntimeError('点击操作异常，点不到按钮，请检查点击操作！')


if __name__ == "__main__":
    a = CampaignSpider(6414)
    a.initDriver()
    a.ifLoadPage('__box7-0')
    print(a.url())