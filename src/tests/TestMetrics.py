import unittest
import sys

sys.path.append("../..")
from src.Models.Metrics import Metrics


class TestMetrics(unittest.TestCase):

    def setUp(self) -> None:
        self.metrics = Metrics('China', ('2020-01-01', '2020-12-31'))

    def test_total_number(self):
        t = self.metrics.total_number()
        self.assertEqual(331, t['Email Number'])
        self.assertEqual(247, t['Unique Email Number'])
        self.assertEqual(4232940, t['Touch Points'])
        self.assertEqual(12788, t['Average Touch Points'])
        self.assertEqual(30, t['EDM'])
        self.assertEqual(14, t['Newsletter'])
        self.assertEqual(3, t['Nurture'])
        self.assertEqual(2, t['Offline Event Invitation'])
        self.assertEqual(198, t['Webinar Invitation'])
        self.assertAlmostEqual(0.063, t['Open Rate'], places=2)
        self.assertAlmostEqual(0.060, t['Click to Open Rate'], places=2)
        self.assertAlmostEqual(0.0078, t['CTR'], places=2)
        self.assertAlmostEqual(0.0049, t['Valid CTR'], places=2)
        self.assertAlmostEqual(0.0037, t['Unique CTR'], places=2)

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
