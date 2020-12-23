from src.Views.Panel import Panel
from src.Models.Workflow import campaign_id_work
from src.Connector.MA import MA

def upload():
    data = campaign_id_work()
    Panel(data).display()

