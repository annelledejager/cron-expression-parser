import unittest

from tests.test_cron_expression_parser import CronExpressionParserTestCase, HelpInstructionsTestCase
from tests.test_pep8 import Pep8TestCase


def create_suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(CronExpressionParserTestCase))
    test_suite.addTest(unittest.makeSuite(HelpInstructionsTestCase))
    test_suite.addTest(unittest.makeSuite(Pep8TestCase))

    return test_suite


if __name__ == '__main__':
    suite = create_suite()

    runner = unittest.TextTestRunner()
    runner.run(suite)
