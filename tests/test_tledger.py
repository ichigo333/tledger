import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import argparse
import unittest
from datetime import date
from unittest.mock import patch
from argparse import Namespace

from tledger import validate_args, parse_date
from options import TODAY, YESTERDAY, DAY, MONTH


def make_args(**kwargs) -> Namespace:
    defaults = dict(add=None, time=None, day=None, month=None, year=None, show=None)
    defaults.update(kwargs)
    return Namespace(**defaults)


def make_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser()


class BaseTestValidateArgs(unittest.TestCase):

    def setUp(self):
        self.patcher = patch("sys.stderr")
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()


class TestValidateArgsAdd(BaseTestValidateArgs):

    def test_add_without_time_errors(self):
        parser = make_parser()
        args = make_args(add="coding")
        with self.assertRaises(SystemExit):
            validate_args(parser, args)

    def test_add_with_time_valid(self):
        parser = make_parser()
        args = make_args(add="coding", time=60)
        validate_args(parser, args)

    def test_add_with_month_without_day_errors(self):
        parser = make_parser()
        args = make_args(add="coding", time=60, month=3)
        with self.assertRaises(SystemExit):
            validate_args(parser, args)

    def test_add_with_month_and_day_valid(self):
        parser = make_parser()
        args = make_args(add="coding", time=60, month=3, day=15)
        validate_args(parser, args)

    def test_add_with_year_without_month_errors(self):
        parser = make_parser()
        args = make_args(add="coding", time=60, year=2025)
        with self.assertRaises(SystemExit):
            validate_args(parser, args)

    def test_add_with_year_and_month_valid(self):
        parser = make_parser()
        args = make_args(add="coding", time=60, year=2025, month=3, day=15)
        validate_args(parser, args)


class TestValidateArgsShowDay(BaseTestValidateArgs):

    def test_show_day_without_day_errors(self):
        parser = make_parser()
        args = make_args(show=DAY)
        with self.assertRaises(SystemExit):
            validate_args(parser, args)

    def test_show_day_with_day_valid(self):
        parser = make_parser()
        args = make_args(show=DAY, day=15)
        validate_args(parser, args)

    def test_show_day_with_year_without_month_errors(self):
        parser = make_parser()
        args = make_args(show=DAY, day=15, year=2025)
        with self.assertRaises(SystemExit):
            validate_args(parser, args)

    def test_show_day_with_year_and_month_valid(self):
        parser = make_parser()
        args = make_args(show=DAY, day=15, year=2025, month=3)
        validate_args(parser, args)


class TestValidateArgsShowMonth(BaseTestValidateArgs):

    def test_show_month_without_month_defaults_to_current(self):
        parser = make_parser()
        args = make_args(show=MONTH)
        validate_args(parser, args)

    def test_show_month_with_month_valid(self):
        parser = make_parser()
        args = make_args(show=MONTH, month=3)
        validate_args(parser, args)

    def test_show_month_with_day_warns(self):
        parser = make_parser()
        args = make_args(show=MONTH, month=3, day=15)
        with patch("builtins.print") as mock_print:
            validate_args(parser, args)
            mock_print.assert_called_once_with("Warning: --show month option ignores --day [num] option")

    def test_show_month_without_day_no_warning(self):
        parser = make_parser()
        args = make_args(show=MONTH, month=3)
        with patch("builtins.print") as mock_print:
            validate_args(parser, args)
            mock_print.assert_not_called()


class TestValidateArgsNoOp(BaseTestValidateArgs):

    def test_no_args_valid(self):
        parser = make_parser()
        args = make_args()
        validate_args(parser, args)

    def test_show_today_valid(self):
        parser = make_parser()
        args = make_args(show=TODAY)
        validate_args(parser, args)

    def test_show_yesterday_valid(self):
        parser = make_parser()
        args = make_args(show=YESTERDAY)
        validate_args(parser, args)


class TestParseDate(BaseTestValidateArgs):

    def test_all_args_provided(self):
        parser = make_parser()
        args = make_args(year=2025, month=3, day=15)
        self.assertEqual(parse_date(parser, args), date(2025, 3, 15))

    def test_no_args_defaults_to_today(self):
        parser = make_parser()
        args = make_args()
        self.assertEqual(parse_date(parser, args), date.today())

    def test_only_day_provided(self):
        parser = make_parser()
        args = make_args(day=15)
        today = date.today()
        self.assertEqual(parse_date(parser, args), date(today.year, today.month, 15))

    def test_only_month_provided(self):
        parser = make_parser()
        args = make_args(month=6)
        today = date.today()
        self.assertEqual(parse_date(parser, args), date(today.year, 6, today.day))

    def test_only_year_provided(self):
        parser = make_parser()
        args = make_args(year=2024)
        today = date.today()
        self.assertEqual(parse_date(parser, args), date(2024, today.month, today.day))

    def test_invalid_date_errors(self):
        parser = make_parser()
        args = make_args(year=2025, month=2, day=30)
        with self.assertRaises(SystemExit):
            parse_date(parser, args)


if __name__ == "__main__":
    unittest.main()