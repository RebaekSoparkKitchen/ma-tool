"""
@Description: 
@Author: FlyingRedPig
@Date: 2020-05-01 17:58:32
@LastEditors: FlyingRedPig
@LastEditTime: 2020-08-06 10:34:27
@FilePath: \EDM\src\Spider\CampaignSpider.py
"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import selenium
import time
from src.Connector.MA import MA


class CampaignSpider(MA):

    def __init__(self, campaign_id, driver=None):
        """
        @description: 
        @param {type} campaign_id:是最重要的参数，其他类请求服务的时候要用它作为键值请求；driverPath:指定chrome_driver的地址
        @return: 
        """
        super().__init__()
        self.campaign_id = campaign_id
        self.driver_path = self.read_config()['chrome_driver']
        self.driver = driver
        self.url = f'https://my300723.s4hana.ondemand.com/ui#Initiative-manageCampaignFlow?Tab=PERFORMANCE' \
                   f'&/CampaignObject/000000{self.campaign_id}/1'

    def init_driver(self):
        """
        @description: 
        @param {type} 
        @return: 
        """
        driver_path = self.driver_path
        desired_capabilities = DesiredCapabilities().CHROME
        desired_capabilities['pageLoadStrategy'] = 'eager'
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches',
                                               ['enable-automation'])

        driver = webdriver.Chrome(
            options=chrome_options,
            executable_path=driver_path,
            desired_capabilities=desired_capabilities)  # chrome_driver的执行文件

        driver.delete_all_cookies()
        driver.maximize_window()
        self.driver = driver
        return

    def close_driver(self):
        self.driver.close()
        return

    def url(self):
        """
        通过campaignId获得url
        :return: url地址
        """
        campaign_id = str(self.campaign_id)
        url = r'https://my300723.s4hana.ondemand.com/ui#Initiative-manageCampaignFlow?Tab=PERFORMANCE&/CampaignObject' \
              r'/000000' + self.campaign_id + '/1'
        return url

    def if_load_page(self, id, attempt_num=30, interval_time=5) -> None:
        """
        :param id: 新页面特有的id，通过判断它来判断页面是否跳转了
        :param attempt_num: 尝试次数，到达上限后放弃，并报错
        :param interval_time: 尝试的间隔时间
        :return: 若通过则无返回，若不通过则raise error
        """
        count = 0
        while True:
            try:
                self.driver.find_element_by_id(id)
                break
            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(interval_time)
            count += 1
            if count == attempt_num:
                raise RuntimeError('未跳转异常，请检查跳转操作！')

    def click(self, id, attempt_num=60, interval_time=1):
        """
        :param id: 要点击的按钮
        :param attempt_num:
        :param interval_time:
        :return: 原理与if_load_page一样，不再赘述
        """
        count = 0
        while True:
            try:
                self.driver.find_element_by_id(id).click()
                break
            except:
                time.sleep(interval_time)
            count += 1
            if count == attempt_num:
                raise RuntimeError('点击操作异常，点不到按钮，请检查点击操作！')


if __name__ == "__main__":
    a = CampaignSpider(6414)
    a.init_driver()
    a.if_load_page('__box7-0')
    print(a.url())