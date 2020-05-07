'''
@Description: 
@Author: FlyingRedPig
@Date: 2020-05-06 19:19:06
@LastEditors: FlyingRedPig
@LastEditTime: 2020-05-06 23:59:38
@FilePath: \EDM\edm\Spider\Overview.py
'''

from CampaignSpider import CampaignSpider
import time


class Overview(CampaignSpider):

    def __init__(self, campaignId, driver=None):
        super().__init__(campaignId, driver)

    def overviewUrl(self):
        campaignId = str(self.getCampaignId())
        url = r'https://my300723.s4hana.ondemand.com/ui#Initiative-manageCampaignFlow?Tab=OVERVIEW&/CampaignObject/000000' + campaignId + '/1'
        return url

    def goOverviewPage(self):
        if self.driver == None:  #若没有手动传driver过来
            self.initDriver()
            self.driver.get(self.overviewUrl())
        elif self.driver.current_url == self.url():
            self.driver.find_element_by_id(
                "application-Initiative-manageCampaignFlow-component---object--ObjectPageLayout-anchBar-application-Initiative-manageCampaignFlow-component---object--Info_display_fragment_section-anchor"
            ).click()
        return

    def overviewData(self):
        time.sleep(10)
        return self.driver.find_element_by_id("__text12")


if __name__ == "__main__":

    o = Overview(6463)
    print(o.driver)
    o.goOverviewPage()
    print(o.overviewData())
