'''
@Description: Request template
@Author: FlyingRedPig
@Date: 2020-11-24 11:07:37
@LastEditors: FlyingRedPig
@LastEditTime: 2020-11-24 11:07:38
@FilePath: \MA_tool\src\Request\Request.py
'''
import datetime as dt
class Request():
    def __init__(self, campaign_name: str, type: str, owner_first_name: str, owner_last_name:str, department: str, location: str, wave: int, smc_campaign_id: int, request_time: dt.date, event_time: dt.date, launch_time: dt.date, editor: str):
        """
        request template
        """
        self.campaign_name = campaign_name
        self.type = type
        self.owner_first_name = owner_first_name
        self.owner_last_name = owner_last_name
        self.department = department
        self.location = location
        self.wave = wave
        self.smc_campaign_id = smc_campaign_id
        self.request_time = request_time
        self.event_time = event_time
        self.editor = editor