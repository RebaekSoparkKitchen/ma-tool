'''
@Description: 一个作为newsletter以及qbr的脚本
@Author: FlyingRedPig
@Date: 2020-07-15 11:51:16
@LastEditors: FlyingRedPig
@LastEditTime: 2020-07-29 12:03:11
@FilePath: \EDM_project\EDM\edm\Tracker\DA.py
'''
from edm.Tracker.RequestTracker import Request_Tracker
import pandas as pd
from dateutil.parser import parse
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter


class SMCDA(object):

    def __init__(self):
        rq = Request_Tracker()
        self.df = rq.getCleanDf()
        # 在clean df中 所有日期的格式都是datetime.date
        self.df['week_num'] = self.df['Launch Date'].apply(
            lambda x: x.isocalendar()[1])

        self.df['weekday_num'] = self.df['Launch Date'].apply(
            lambda x: x.isocalendar()[2])

        self.df['year'] = self.df['Launch Date'].apply(lambda x: x.year)
        self.df['month'] = self.df['Launch Date'].apply(lambda x: x.month)
        self.monthDic = {
            1: 'Jan',
            2: 'Feb',
            3: 'Mar',
            4: 'Apr',
            5: 'May',
            6: 'Jun',
            7: 'July',
            8: 'Aug',
            9: 'Sep',
            10: 'Oct',
            11: 'Nov',
            12: 'Dec'
        }

        self.weekDic = {
            1: 'Mon',
            2: 'Tue',
            3: 'Wed',
            4: 'Thu',
            5: 'Fri',
            6: 'Sat',
            7: 'Sun'
        }

    def get_df(self):
        return self.df

    def isHK(self, x):
        '''
        判断一个字符串是不是香港的，在MU中
        '''
        return 'hong' in x.lower()

    def isTW(self, x):
        return 'tai' in x.lower()

    def isCN(self, x):
        return 'china' in x.lower()

    @staticmethod
    def str2date(string: str):
        return parse(str(string)).date()

    def filterData(self, region: str, timeRange: tuple):
        '''
        timeRange 是一个 str tuple，我们会预处理把它变成dt.date
        region: ['gc','cn','tw','hk']
        '''
        time1 = SMCDA.str2date(timeRange[0])
        time2 = SMCDA.str2date(timeRange[1])

        df = self.get_df()

        df = df[(df['Launch Date'] > time1) & (df['Launch Date'] < time2)]

        if region.lower() == 'gc':
            return df
        elif region.lower() == 'cn':
            return df[df['MU'].apply(lambda x: self.isCN(x))]
        elif region.lower() == 'hk':
            return df[df['MU'].apply(lambda x: self.isHK(x))]
        elif region.lower() == 'tw':
            return df[df['MU'].apply(lambda x: self.isTW(x))]

    # 'Request Type' , 'MU', 'Team'
    @staticmethod
    def countBy(df, attribute: str):
        '''
        核心函数，我们需要大量的countBy
        '''
        return pd.pivot_table(
            df, index=[attribute], aggfunc='count')['Campaign Name']

    @staticmethod
    def openRateBy(df, attribute: str):
        '''
        核心函数，按attribute的开信率对比
        '''
        df = pd.pivot_table(df, index=[attribute], aggfunc=np.sum)
        return df['Opened'] / df['Delivered']

    # for newsletter

    def countByMonthPic(self, bgColor="#f4f8fb"):

        df = s.filterData('gc', (20200101, 20200630))
        df1 = s.filterData('gc', (20190101, 20190630))
        a = SMCDA.countBy(df, 'month')
        b = SMCDA.countBy(df1, 'month')
        month = list(map(lambda x: self.monthDic[x], a.index))
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['figure.facecolor'] = bgColor
        plt.rcParams['axes.facecolor'] = bgColor
        plt.grid(
            b=True,
            axis='y',
            color='#999999',
            linestyle='dashdot',
            linewidth=0.2,
            alpha=0.7)
        plt.bar(
            month,
            a.values,
            label="2020 1st half",
            width=0.7,
            alpha=0.7,
            color='#ffa600',
            edgecolor='#000000')

        plt.bar(
            month,
            b.values,
            label="2019 1st half",
            width=0.7,
            alpha=0.7,
            color='#bc5090',
            edgecolor='#000000')
        for x, y in zip(month, a.values):
            plt.text(x, y + 0.1, '%i' % y, ha='center', va='bottom')
        plt.legend()
        plt.show()
        plt.close()
        return

    @staticmethod
    def to_percent(temp, position):
        '''
        helper method, 为了显示百分比
        '''
        return '%1.0f' % (100 * temp) + '%'

    def byOpenRateMonth(self, df, bgColor="#f4f8fb"):

        a = SMCDA.openRateBy(df, 'month')
        month = list(map(lambda x: self.monthDic[x], a.index))
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['figure.facecolor'] = bgColor
        plt.rcParams['axes.facecolor'] = bgColor
        plt.grid(
            b=True,
            axis='y',
            color='#999999',
            linestyle='dashdot',
            linewidth=0.2,
            alpha=0.7)
        plt.bar(
            month,
            a.values,
            label="2020 1st half",
            width=0.7,
            alpha=0.7,
            color='#ffa600',
            edgecolor='#000000')

        plt.yticks(np.arange(0, 0.13, 0.02))

        for x, y in zip(month, a.values):
            plt.text(
                x,
                y + 0.002,
                '%1.2f' % (y * 100) + '%',
                ha='center',
                va='bottom')

        plt.gca().yaxis.set_major_formatter(FuncFormatter(SMCDA.to_percent))

        # plt.legend()
        plt.show()
        plt.close()

    def piePic(self, attribute, bgColor="#f4f8fb"):
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['figure.facecolor'] = bgColor
        plt.rcParams['axes.facecolor'] = bgColor

        df = s.filterData('gc', (20200101, 20200630))
        data = SMCDA.countBy(df, attribute)

        patches, l_text, p_text = plt.pie(
            data.values,  # 数值信息
            labels=data.index,  # 标签信息
            explode=None,  # 距离圆中心的距离
            colors=['#e4b98c', '#de825f', '#76a77d', '#b9c69f',
                    '#f0e8cf'],  # 颜色
            startangle=90,  # 逆时针起始角度设置
            labeldistance=1.1,
            autopct='%1.0f%%',  # 在饼图中，显示百分数)
            wedgeprops={
                'linewidth': 0.5,
                'edgecolor': '#000000'
            })

        for t in l_text:
            t.set_size(8)
        for t in p_text:
            t.set_size(7)
        # 设置x，y轴刻度一致，这样饼图才能是圆的
        plt.axis('equal')
        plt.show()
        plt.close()
        return


if __name__ == "__main__":
    s = SMCDA()
    df = s.filterData('gc', (20190101, 20190630))
    print(len(df))
    df1 = s.filterData('gc', (20200101, 20200630))
    print(len(df1))

    # bgColor = "#f4f8fb"
    # df = s.filterData('gc', (20200101, 20200630))
    # a = SMCDA.openRateBy(df, 'month')

    # month = list(map(lambda x: s.monthDic[x], a.index))
    # plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # plt.rcParams['figure.facecolor'] = bgColor
    # plt.rcParams['axes.facecolor'] = bgColor
    # plt.grid(
    #     b=True,
    #     axis='y',
    #     color='#999999',
    #     linestyle='dashdot',
    #     linewidth=0.2,
    #     alpha=0.7)
    # plt.bar(
    #     month,
    #     a.values,
    #     label="2020 1st half",
    #     width=0.7,
    #     alpha=0.7,
    #     color='#ffa600',
    #     edgecolor='#000000')

    # plt.yticks(np.arange(0, 0.13, 0.02))

    # for x, y in zip(month, a.values):
    #     plt.text(
    #         x, y + 0.002, '%1.2f' % (y * 100) + '%', ha='center', va='bottom')

    # def to_percent(temp, position):
    #     return '%1.0f' % (100 * temp) + '%'

    # plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

    # # plt.legend()
    # plt.show()
    # plt.close()
