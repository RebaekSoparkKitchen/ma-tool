import unittest
from src.Models.Metrics import Metrics
import sqlite3
from src.Connector.MA import MA


class TestMetrics(unittest.TestCase):

    def setUp(self) -> None:
        conn = sqlite3.connect(MA().read_config()['data_location']['Test_Database'])
        self.cur = conn.cursor()

    def test_total_number(self):


    def tearDown(self) -> None:
        self.cur.close()
