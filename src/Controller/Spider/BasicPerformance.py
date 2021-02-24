"""
@Description: 抓取Performance页面上的信息
@Author: FlyingRedPig
@Date: 2020-05-01 19:22:36
@LastEditors: FlyingRedPig
@LastEditTime: 2020-08-06 10:34:11
@FilePath: \EDM\src\Spider\BasicPerformance.py
"""
import sys

sys.path.append('../..')
from src.Controller.Spider.CampaignSpider import CampaignSpider
import re
import selenium


class BasicPerformance(CampaignSpider):

    def __init__(self, campaign_id, driver=None):

        super().__init__(campaign_id, driver)

        self.box_list = list(map(lambda x: 'ext_tile_fragment--measuresWithoutTargetsContainerFlexBox-' + str(x), range(12)))
        self.index_list = [
            'Sent', 'Hard Bounces', 'Soft Bounces', 'Delivered', 'Opened',
            'Unique Click', 'Click'
        ]
        self.rate_list = [
            'Bounce Rate', 'Opened Messages in %', 'CTR', 'Unique CTR',
            'Click-To-Open Rate'
        ]

    @staticmethod
    def __catch_number(sentence: str) -> int:
        """
        @description: 因为我们是通过title（鼠标悬停出现的字）来抓数的 
        @param {type} sentence: 每个box的title（鼠标悬停出现的字） 
        @return: 
        """
        sentence = sentence.replace(',', '')  # 将逗号去除
        return int(re.search(r'\d+', sentence).group())

    def __judge_index(self, sentence: str) -> bool:
        """
        判断一个句子是不是表示index(Sent, Opened, etc)，若index，则True；若Rate，则False
        :param sentence: 每个box的title（鼠标悬停出现的字） 
        :return:
        """
        judge = list(map(lambda x: x in sentence, self.rate_list))
        return not (True in judge)

    def data(self) -> dict:

        self.init_driver()
        self.driver.get(self.url)
        self.if_load_page(self.box_list[0])  # 通过这个方法来判断是否真正加载出来了这些box

        # data_dic 这里得到基本数据
        data_dic = {}  # 初始化数据字典
        for item in self.index_list:  # 如果最后没有找到任何记录，我还能保持一个0，让这一项存在
            data_dic[item] = 0
        for i in self.box_list:
            try:
                sentence = self.driver.find_element_by_id(i).get_attribute(
                    'title')
            except selenium.common.exceptions.NoSuchElementException:
                continue
            if self.__judge_index(sentence):  # 去除rate的干扰
                for index_item in self.index_list:
                    if index_item in sentence:  # eg:如果unique clicks在句子中，它就归为unique clicks这类,注意：unique clicks永远比clicks优先判断，之后立刻break
                        number = self.__catch_number(sentence)
                        data_dic[index_item] = number
                        break

        data_dic['smc_campaign_id'] = self.campaign_id
        return data_dic


if __name__ == "__main__":
    b = BasicPerformance('6364')
    print(b.data())
