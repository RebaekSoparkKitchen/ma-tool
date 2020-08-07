'''
@Description: EDM.Analytics的测试文件
@Author: FlyingRedPig
@Date: 2020-04-23 21:54:48
@LastEditors: FlyingRedPig
@LastEditTime: 2020-08-06 10:35:38
@FilePath: \EDM\src\tests\test_Analytics.py
'''
import unittest
import os
import sys
import datetime as dt
sys.path.append(os.getcwd())
from src.Tracker.Analytics import Analytics


class TestAnalytics(unittest.TestCase):

    def test_init(self):
        a = Analytics(1235, 1223, 2311)
        self.assertEquals(a.getCampaignId(), (1235, 1223, 2311))
        self.assertEquals(a.getStartDate(), dt.date(2020, 1, 1))
        b = Analytics()
        self.assertEqual(b.getCampaignId(), ())

    def test_setStartDate(self):
        a = Analytics(1235, 1223, 2311)
        a.setStartDate(dt.date(2020, 4, 3))
        self.assertEqual(a.getStartDate(), dt.date(2020, 4, 3))
        with self.assertRaises(TypeError):
            a.setStartDate(2020, 4, 3)

    def test_getStardDate(self):
        a = Analytics(1235)
        self.assertEquals(a.getStartDate(), dt.date(2020, 1, 1))


if __name__ == '__main__':
    unittest.main()