import json


class Read_json(object):

    def __init__(self, campaign_id, data_path=r'C:\Users\C5293427\Desktop\MA\campaign_data\data.json'):
         
        self.other_link = []
        self.campaign_id = campaign_id
        self.path = data_path
        self.data_dic = {}
        self.total_click_list = []    #所有link的数据及名称
        self.main_click_list = []     #主要link的数据及名称
        self.other_click_list = []    #其他link的数据及名称
        self.vallina_dic = {}
        self.main()
        
    def get_path(self):
        return self.path

    def get_campaign_id(self):
        return self.campaign_id

    def get_data_dic(self):
        return self.data_dic

    def get_total_click_list(self):
        return self.total_click_list
    
    def get_main_click_list(self):
        return self.main_click_list

    def get_other_click_list(self):
        return self.other_click_list

    def get_other_link(self):
        return self.other_link

    def load_dic(self):
        '''
        把json文件读出来，并解析成字典
        '''
        filename = self.get_path()
        with open(filename) as f_obj:
            dic = json.load(f_obj)

        self.vallina_dic = dic[str(self.get_campaign_id())]
        
        return dic

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
    
    def main(self):

        total_dic = self.load_dic()
        campaign_id = str(self.get_campaign_id())
        specific_dic = total_dic[campaign_id]
        self.total_click_list = specific_dic['total_click_list']
        self.main_click_list = specific_dic['main_click_list']
        self.other_click_list = specific_dic['other_click_list']
        self.data_dic = specific_dic['data_dic']
        return 
    


if __name__ == '__main__':
    
    try:
        r = Read_json(4686)
    except KeyError:
        raise KeyError('你那个json文件里根本没有这个campaign id啊喂！')
    print(r.get_other_link())
    print(r.total_click_list)
    print(r.main_click_list)
    print(r.other_click_list)
    print(r.data_dic)



