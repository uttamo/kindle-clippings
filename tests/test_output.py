from unittest import TestCase
import datetime as dt
import os.path

from output import format_datetime, date_suffix


class TestOutput(TestCase):
    def test_format_datetime(self):
        # 'Thursday, 26 July 2018 01:29:40'
        assert format_datetime(dt.datetime(2018, 7, 26, 1, 29, 40)) == '1:29am, 26th July 2018'

        # 'Thursday, 16 August 2018 00:02:48'
        assert format_datetime(dt.datetime(2018, 8, 16, 2, 48, 1)) == '2:48am, 16th August 2018'

        # 'Thursday, 16 August 2018 00:14:48'
        assert format_datetime(dt.datetime(2018, 8, 16, 14, 48, 31)) == '2:48pm, 16th August 2018'

    def test_date_suffix(self):
        assert date_suffix(1) == 'st'
        assert date_suffix(2) == 'nd'
        assert date_suffix(3) == 'rd'
        assert date_suffix(4) == 'th'
        assert date_suffix(11) == 'th'
        assert date_suffix(13) == 'th'
        assert date_suffix(16) == 'th'
        assert date_suffix(20) == 'th'
        assert date_suffix(21) == 'st'
        assert date_suffix(22) == 'nd'
        assert date_suffix(29) == 'th'
        assert date_suffix(30) == 'th'
        assert date_suffix(31) == 'st'

        with self.assertRaises(ValueError):
            date_suffix(34)
