'''
@Description: 抓取Performance页面上的信息
@Author: FlyingRedPig
@Date: 2020-05-01 19:22:36
@LastEditors: FlyingRedPig
@LastEditTime: 2020-05-07 16:50:04
@FilePath: \EDM\edm\Spider\BasicPerformance.py
'''
from CampaignSpider import CampaignSpider
import re
import time
import selenium


class BasicPerformance(CampaignSpider):

    def __init__(self, campaignId, driver=None):

        super().__init__(campaignId, driver)

        self.boxList = list(map(lambda x: '__box7-' + str(x), range(12)))
        self.indexList = [
            'Sent', 'Hard Bounces', 'Soft Bounces', 'Delivered', 'Opened',
            'Unique Click', 'Click'
        ]
        self.rateList = [
            'Bounce Rate', 'Opened Messages in %', 'CTR', 'Unique CTR',
            'Click-To-Open Rate'
        ]

    def getRateList(self) -> list:
        return self.rateList

    def getBoxList(self) -> list:
        return self.boxList

    def getIndexList(self) -> list:
        return self.indexList

    def __catchNumber(self, sentence: str) -> int:
        '''
        @description: 因为我们是通过title（鼠标悬停出现的字）来抓数的 
        @param {type} sentence: 每个box的title（鼠标悬停出现的字） 
        @return: 
        '''
        sentence = sentence.replace(',', '')  #将逗号去除
        return int(re.search('\d+', sentence).group())

    def __judgeIndex(self, sentence: str) -> bool:
        '''
        判断一个句子是不是表示index(Sent, Opened, etc)，若index，则True；若Rate，则False
        :param sentence: 每个box的title（鼠标悬停出现的字） 
        :return:
        '''
        judge = list(map(lambda x: x in sentence, self.getRateList()))
        return not (True in judge)

    def basicPerformanceData(self) -> dict:

        self.initDriver()
        self.driver.get(self.url())

        self.ifLoadPage('__box7-0')  #通过这个方法来判断是否真正加载出来了这些box

        # dataDic 这里得到基本数据
        dataDic = {}  #初始化数据字典
        for i in self.getBoxList():
            try:
                sentence = self.driver.find_element_by_id(i).get_attribute(
                    'title')
            except selenium.common.exceptions.NoSuchElementException:
                continue
            if self.__judgeIndex(sentence):  #去除rate的干扰
                for index_item in self.getIndexList():
                    if index_item in sentence:  #eg:如果unique clicks在句子中，它就归为unique clicks这类,注意：unique clicks永远比clicks优先判断，之后立刻break
                        number = self.__catchNumber(sentence)
                        dataDic[index_item] = number
                        break
        return dataDic


if __name__ == "__main__":
    b = BasicPerformance('6364')
    print(b.basicPerformanceData())
