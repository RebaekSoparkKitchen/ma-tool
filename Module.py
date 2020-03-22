import time
from Clean_df import EDM
from Calender import Calender, Simple_tracker
from Display import Display
from DataSpider import DataSpider
from Operation import Report, Tracker
from Read_json import Read_json
import warnings
import json
import importlib,sys
import os

#ignore warnings
warnings.filterwarnings('ignore')

class Module(object):

    def __init__(self, location='local_path'):

        #read config file
        with open("config.json", "r", encoding='utf-8') as f:
            config = json.loads(f.read())    # load的传入参数为字符串类型

        #read path from config file
        self.tracker_path = config['local_path']['tracker_path']
        self.simple_tracker_path = config['local_path']['simple_tracker_path']
        self.report_template = config['local_path']['report_template']
        self.report_save = config['local_path']['report_save']

        # get dataframe
        edm = EDM(self.tracker_path)
        self.vanilla_df = edm.get_dataframe1() #清洗后的dataframe
        self.clean_df = edm.clean_date()   #原dataframe
        self.today_report = []
        return

    def get_tracker_path(self):
        return self.tracker_path

    def get_simple_tracker_path(self):
        return self.simple_tracker_path
    
    def get_report_template(self):
        return self.report_template
    
    def get_report_save(self):
        return self.report_save

    def get_vanilla_df(self):
        return self.vanilla_df

    def get_clean_df(self):
        return self.clean_df

    def get_today_report(self):
        return self.today_report
    

    def show(self):
        '''
        展示界面，展示所有维度
        '''
        vanilla_df = self.get_vanilla_df()
        df = self.get_clean_df()
        orginal_d = Display(vanilla_df)
        d = Display(df)

        print('Future work')
        try:
            display(d.future_work())
        except NameError:
            print(d.future_work())
        print('Wait work')
        try:
            display(orginal_d.wait_work())
        except NameError:
            print(orginal_d.wait_work())
        print('Report')
        try:
            display(d.report())
        except NameError:
            print(d.report())
        print('Communication Limit Hint')
        try:
            display(d.communication_limit_hint())
        except NameError:
            print(d.communication_limit_hint())
        print('Check list')
        try:
            display(d.check())
        except NameError:
            print(d.check())

        return


    def create_simple_tracker(self):
        '''
        创建simple tracker
        '''
        df = self.get_clean_df()
        simple_tracker_path = self.get_simple_tracker_path()
        c = Calender(df,simple_tracker_path)
        c.to_xlsx()
        s = Simple_tracker()
        s.create_excel()
        print('Create simple tracker successfully!')
        return 


    def today_report_list(self) -> list:
        '''
        得到今天report的list，为后面的抓取数据提供接口
        '''
        df = self.get_clean_df()
        d = Display(df)
        report_list = list(d.report()['Campaign ID'])
        report_list = [int(x) for x in report_list]
        return report_list

    def scratch(self, campaign_id, overwrite=False):
        '''
        catch_data_from_web的辅助函数
        '''
        if overwrite:
            spider = DataSpider(campaign_id)
            spider.scratch_data()
        else:
            try:
                Read_json(campaign_id)
            except KeyError:
                spider = DataSpider(campaign_id)
                spider.scratch_data()
        return


    def catch_data_from_web(self, campaign_id_input, overwrite=True):
        '''
        campaign_id_input: 这是直接从input函数或其他list接过来的
        overwrite:指是否重新抓取数据，覆盖原数据
        '''

        if not type(campaign_id_input) is list:
            campaign_id_input = [int(campaign_id_input)]

        for campaign_id in campaign_id_input:
            self.scratch(campaign_id, overwrite)
            print('Get',str(campaign_id), 'from the system successfully!')
                
        return 

    def write_data_in_tracker(self, campaign_id_input):
        '''
        把campaign data从json读出来，存到tracker中
        '''
        df = self.get_clean_df()
        tracker_path = self.get_tracker_path()

        if not type(campaign_id_input) is list:
            campaign_id_input = [int(campaign_id_input)]

        for campaign_id in campaign_id_input:

            campaign_id = int(campaign_id)

            j = Read_json(campaign_id)
            data_dic = j.get_data_dic()
            main_click_list = j.get_main_click_list()
            other_click_list = j.get_other_click_list()


            t = Tracker(tracker_df=df, tracker_path=tracker_path)

            try:
                t.write_data(data_dic=data_dic, campaign_id=campaign_id)
            except IndexError:
                raise IndexError('您那tracker里没填campaign id啊喂')

            t.save_data()
        print('Write campaign data in tracker successfully!')
        return
    
    def create_single_report_excel(self, campaign_id):
        '''
        生成report的excel文件
        '''
        campaign_id = int(campaign_id)

        j = Read_json(campaign_id)
        data_dic = j.get_data_dic()
        main_click_list = j.get_main_click_list()
        other_click_list = j.get_other_click_list()
        df = self.get_clean_df()
        report_template = self.get_report_template()
        report_save = self.get_report_save()

        r = Report(df=df, campaign_id=campaign_id, template_path=report_template)
        while True:
            try:
                r.excute_report(data_dic=data_dic,
                                main_click_list=main_click_list,
                                other_click_list=other_click_list,
                                save_path=report_save)
                print('Campaign', str(campaign_id), 'report created successfully!')
                break
            except IndexError:
                raise IndexError('您那tracker里没填campaign id啊喂')
            except PermissionError:
                print('Please close the target report file, we will try after 5 seconds.')
                time.sleep(5)
        return 

    def create_report_excel(self, campaign_id_input):

        if not type(campaign_id_input) is list:
            campaign_id_input = [int(campaign_id_input)]
        
        for campaign_id in campaign_id_input:
            self.create_single_report_excel(campaign_id)
        
        return 

class Conversation(Module):

    def say_hi(self):

        self.show()
        self.create_simple_tracker()
        print("Hi Zinan, Nice day ha, let's go!!!")
        return

    def order_report(self):

        while True:

            order = input("What we gonna do? Get today's report automatically?")

            if ('yes' or '是') in order:
                campaign_id = self.today_report_list()

            elif ('man' or '人工') in order:
                campaign_id = input('Pls tell me the campaign id, you are the best!')

            elif 'no' or '否' in order:
                print("Ciao Ciao ~~")
                break
            
            else:
                print('也听不懂你丫在说啥啊，整点儿明白话！')
                continue

            if campaign_id == []:
                print('您这campaign id是空白啊，咋填？！')
                continue
            
            self.catch_data_from_web(campaign_id, overwrite=True)
            print('Catch data from Internet successfully!')
            self.write_data_in_tracker(campaign_id)
            print('Write data in main tracker successfully!')
            self.create_report_excel(campaign_id_input=campaign_id)
            print('Create report excel successfully!')


        return 



if __name__ == '__main__':

    campaign_id = [4804,4793]
    i = Module()
    i.show()
    i.catch_data_from_web(campaign_id, overwrite=False)
    i.create_simple_tracker()
    i.write_data_in_tracker(campaign_id)
    i.create_report_excel(campaign_id_input=campaign_id)




