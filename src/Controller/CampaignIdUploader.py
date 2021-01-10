import sys

sys.path.append("../..")

from src.Models.Workflow import campaign_id_work
from src.Views.Diagram.Panel import Panel
from src.Views.WorkDialogue.CampaignID import CampaignID
from src.Models.Uploader import Uploader
from rich import print, box



def upload():
    data = campaign_id_work()
    id_index = 0
    panel = Panel(data).display()
    for i in range(len(data.content)):
        panel.__next__()
        pk_id = data.content[i][id_index]
        smc_campaign_id = CampaignID().ask()
        uploader = Uploader(pk_id=pk_id, table="Request", col="smc_campaign_id", data=smc_campaign_id)
        uploader.upload()



def transfer_data(pk_id: int, data: str):
    uploader = Uploader(pk_id=pk_id, table="Request", col="smc_campaign_id", data=data)
    uploader.upload()


def dialogue():
    return CampaignID().ask()


if __name__ == '__main__':
    upload()
    # import datetime as dt
    # now = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d %H:%M:%S')
    # print(now)
