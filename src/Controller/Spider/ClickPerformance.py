"""
@Description: 具体每一个链接名称作为主键的一个表单
@Author: FlyingRedPig
@Date: 2020-05-02 11:11:05
@LastEditors: FlyingRedPig
@LastEditTime: 2020-08-06 10:34:39
@FilePath: \EDM\src\Spider\ClickPerformance.py
"""
import sys

sys.path.append('../..')
from src.Controller.Spider.CampaignSpider import CampaignSpider
from src.Controller.Spider.BasicPerformance import BasicPerformance
import time
import selenium
from selenium.webdriver.common.keys import Keys


class ClickPerformance(CampaignSpider):

    def __init__(self, campaign_id, driver=None):
        """
        @description: 从父类CampaignSpider我们就预留了driver接口，可以随时覆盖self.driver，
        这样我们就可以把driver如接力一般传来传去地操作。
        @param {type} 
        @return: 
        """
        super().__init__(campaign_id, driver)
        self.attribute = None  # 表格的第一行，代表特征的名称，亦称attribute（字段）

    def get_attribute(self) -> tuple:
        """
        @description:由于我们在收表格的时候使用set()使list乱序了，我们特别地，
        在开始的时候将表头(attribute)收集起来。值得注意的是：我们必须在执行data()方法之后在调用这个方法。
        @param {type} 
        @return: 
        """
        if self.attribute is None:
            raise TypeError(
                "This method should be called after data()")
        return self.attribute

    def __go_click_page(self) -> None:
        """
        @description: 从basicperformance页面跳到click页面的一次鼠标点击操作，注意：要求url必须是performance那个页面
        @param {type} 
        @return: 
        """
        runtime = 0
        while True:
            try:
                self.driver.find_element_by_id(
                    'successTableFragment--smartSuccessTable-header-inner')
                break
            except selenium.common.exceptions.NoSuchElementException:
                self.click('success_frag--tableButton-button')
                time.sleep(3)
                runtime += 1
                if runtime == 30:
                    raise RuntimeError('页面跳转异常，点到按钮了，但无法跳转！')
        return

    def __find_table_element(self) -> list:
        """
        利用selenium直接抓取所有页面内的td元素
        :return:一个列表，形如：[(46,'SAP 天天事'),(3, 'GDPR注册')]
        """

        row = self.driver.find_elements_by_tag_name('tr')
        click_list = []
        for i in row:
            j = i.find_elements_by_tag_name('td')
            row_list = []  # 准备row_list，此处效仿numpy表示矩阵的方法，用列表嵌套表示表格
            for item in j:
                text = item.text
                row_list.append(text)
            click_list.append(tuple(row_list))
        return list(filter(lambda x: x != () and set(x) != {''}, click_list))

    def __final_td(self) -> selenium.webdriver.remote.webelement.WebElement:
        """
        要找到最后一个td对象，方便点击
        :return: selenium那个什么对象，后面用来点的
        """
        return self.driver.find_elements_by_tag_name(
            'tr')[-1].find_elements_by_tag_name('td')[-1]

    def __scroll_down(self, num: int = 3) -> None:
        """
        抓click data的辅助函数：为表格翻页
        :return: 
        """
        item = self.__final_td()
        item.click()
        for i in range(num):
            item.send_keys(Keys.DOWN)
        return

    def data(self, scroll_num: int = 3, attempt_num: int = 60) -> list:
        """
        @description: 此类向外输出的唯一方法
        @param {int, int} scroll_num,下拉表格的次数，应该在[1,6]之间; attempt_num, 尝试刷新表格的次数，should be > 0
        @return: 
        """
        self.__go_click_page()

        for i in range(attempt_num):
            table = self.__find_table_element()
            if len(table) == 1:
                time.sleep(1)  # 休息1s等待数据刷新
            else:
                break
        self.attribute = table[0]
        # 我们此时将表格下拉，直到所拉取的信息为已知信息的子集为止。
        while True:
            self.__scroll_down(scroll_num)
            screen_table = self.__find_table_element()
            if set(screen_table).issubset(set(table)):
                break
            else:
                table = list(set(table) | set(screen_table))

        # 做成一个json能够接受的样子
        table.remove(self.get_attribute())

        def row_process(row):
            row = dict(zip(self.get_attribute(), row))
            row['smc_campaign_id'] = self.campaign_id
            return row

        table = list(map(row_process, table))

        return table


if __name__ == "__main__":
    b = BasicPerformance(6414)
    print(b.data())
    c = ClickPerformance(6414, b.driver)

    print(c.data())
    print(c.get_attribute())

