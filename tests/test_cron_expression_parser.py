import unittest
from StringIO import StringIO

from mock import patch

from cron_expression_parser import CronExpressionParser, instructions


class CronExpressionParserTestCase(unittest.TestCase):
    def setUp(self):
        super(CronExpressionParserTestCase, self).setUp()

    def test_success(self):
        # Given
        self.parser = CronExpressionParser(['*/15', '0', '1,15', '*', '1-5', '/user/bin/find'])

        # When
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.parser.parse()

        # Then
        self.assertEqual(fake_output.getvalue(), 'minute        0 15 30 45\n'
                                                 'hour          0\n'
                                                 'day of month  1 15\n'
                                                 'month         1 2 3 4 5 6 7 8 9 10 11 12\n'
                                                 'day of week   1 2 3 4 5\n'
                                                 'command       /user/bin/find\n')

    def test_success_max_values(self):
        # Given
        self.parser = CronExpressionParser(['*', '*', '*', '*', '*', '/user/bin/find'])

        # When
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.parser.parse()

        # Then
        self.assertEqual(fake_output.getvalue(),
                         'minute        1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60\n'
                         'hour          1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24\n'
                         'day of month  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31\n'
                         'month         1 2 3 4 5 6 7 8 9 10 11 12\n'
                         'day of week   1 2 3 4 5 6 7\n'
                         'command       /user/bin/find\n')

    def test_invalid_range_input(self):
        # Given
        self.parser = CronExpressionParser(['1-5-', '*', '*', '*', '*', '/user/bin/find'])

        # When
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.parser.parse()

        # Then
        self.assertEqual(fake_output.getvalue(),
                         'minute        invalid input\n'
                         'hour          1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24\n'
                         'day of month  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31\n'
                         'month         1 2 3 4 5 6 7 8 9 10 11 12\n'
                         'day of week   1 2 3 4 5 6 7\n'
                         'command       /user/bin/find\n')

    def test_invalid_range_order_input(self):
        # Given
        self.parser = CronExpressionParser(['5-1', '*', '*', '*', '*', '/user/bin/find'])

        # When
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.parser.parse()

        # Then
        self.assertEqual(fake_output.getvalue(),
                         'minute        invalid input\n'
                         'hour          1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24\n'
                         'day of month  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31\n'
                         'month         1 2 3 4 5 6 7 8 9 10 11 12\n'
                         'day of week   1 2 3 4 5 6 7\n'
                         'command       /user/bin/find\n')

    def test_invalid_list_input(self):
        # Given
        self.parser = CronExpressionParser(['*', '1, 5', '*', '*', '*', '/user/bin/find'])

        # When
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.parser.parse()

        # Then
        self.assertEqual(fake_output.getvalue(),
                         'minute        1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60\n'
                         'hour          invalid input\n'
                         'day of month  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31\n'
                         'month         1 2 3 4 5 6 7 8 9 10 11 12\n'
                         'day of week   1 2 3 4 5 6 7\n'
                         'command       /user/bin/find\n')

    def test_invalid_list_order_input(self):
        # Given
        self.parser = CronExpressionParser(['*', '5,1,2', '*', '*', '*', '/user/bin/find'])

        # When
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.parser.parse()

        # Then
        self.assertEqual(fake_output.getvalue(),
                         'minute        1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60\n'
                         'hour          1 2 5\n'
                         'day of month  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31\n'
                         'month         1 2 3 4 5 6 7 8 9 10 11 12\n'
                         'day of week   1 2 3 4 5 6 7\n'
                         'command       /user/bin/find\n')

    def test_invalid_increment_input(self):
        # Given
        self.parser = CronExpressionParser(['*', '1/100', '5/*', '3/5/6', '*', '/user/bin/find'])

        # When
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.parser.parse()

        # Then
        self.assertEqual(fake_output.getvalue(),
                         'minute        1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60\n'
                         'hour          invalid input\n'
                         'day of month  invalid input\n'
                         'month         invalid input\n'
                         'day of week   1 2 3 4 5 6 7\n'
                         'command       /user/bin/find\n')

    def test_invalid_alpha_input(self):
        # Given
        self.parser = CronExpressionParser(['*', '*', '*', '*', '1-MONDAY', '/user/bin/find'])

        # When
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.parser.parse()

        # Then
        self.assertEqual(fake_output.getvalue(),
                         'minute        1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60\n'
                         'hour          1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24\n'
                         'day of month  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31\n'
                         'month         1 2 3 4 5 6 7 8 9 10 11 12\n'
                         'day of week   invalid input\n'
                         'command       /user/bin/find\n')

    def test_invalid_max_input(self):
        # Given
        self.parser = CronExpressionParser(['120', '*', '*', '*', '*', '/user/bin/find'])

        # When
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.parser.parse()

        # Then
        self.assertEqual(fake_output.getvalue(),
                         'minute        invalid input\n'
                         'hour          1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24\n'
                         'day of month  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31\n'
                         'month         1 2 3 4 5 6 7 8 9 10 11 12\n'
                         'day of week   1 2 3 4 5 6 7\n'
                         'command       /user/bin/find\n')


class HelpInstructionsTestCase(unittest.TestCase):
    def setUp(self):
        super(HelpInstructionsTestCase, self).setUp()

    def test_success(self):
        # When
        with patch('sys.stdout', new=StringIO()) as fake_output:
            instructions()

        # Then
        self.assertEqual(fake_output.getvalue(), '\n'
                                                 '        Input format - minute hour day-of-month month day-of-week command\n'
                                                 '        E.g */15 0 1,15 \\* 1-5 /user/bin/find\n\n'
                                                 '        Note that * needs to be escaped E.g \\*\n'
                                                 '    \n')
