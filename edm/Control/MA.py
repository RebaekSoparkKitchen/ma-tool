'''
@Description: 作为最高层级的类，让大家能方便读取配置文件
@Author: FlyingRedPig
@Date: 2020-08-03 11:47:04
@LastEditors: FlyingRedPig
@LastEditTime: 2020-08-03 13:41:36
@FilePath: \EDM\edm\Control\MA.py
'''
import json

class MA(object):
    def __init__(self):
        self.config =self.readConfig()
    
    def readConfig(self) -> dict:
        configPath = r'../config/config.json'
        with open(configPath,'r',encoding='utf8') as fp:
            json_data = json.load(fp)
        return json_data

    def setConfig(self, attribute, data) -> None:
        configPath = r'../config/config.json'
        config = self.readConfig()
        config['username'] = data
        if config == {}:
            print("此更改将清空config文件， 请查看命令是否合理")
            return 
        with open(configPath,"w") as f:
            json.dump(config,f)
        return 
    
