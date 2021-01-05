from src.Models.Report.BasicPerformance import BasicPerformance
from src.Models.Report.ClickPerformance import ClickPerformance

if __name__ == '__main__':
    a = BasicPerformance.select(6414)
    b = ClickPerformance.select(6414)
    print(a)
    print(b)