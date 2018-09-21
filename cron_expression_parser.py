import sys
import re

from consts import MINUTE, HOUR, DAY_OF_MONTH, MONTH, DAY_OF_WEEK, COMMAND, INVALID_INPUT, MAX_VALUES, WEEK_DAYS, MONTHS


class CronExpressionParser(object):
    """
    Responsible for parsing cron expression.
    """

    def __init__(self, args):
        self.minute = args[0].upper()
        self.hour = args[1].upper()
        self.day_of_month = args[2].upper()
        self.month = args[3].upper()
        self.day_of_week = args[4].upper()
        self.command = args[5]

    def _parser_map(self):
        """
        Maps inputs to parser methods.
        """
        return [
            (MINUTE, self._parse_minute),
            (HOUR, self._parse_hour),
            (DAY_OF_MONTH, self._parse_day_of_month),
            (MONTH, self._parse_month),
            (DAY_OF_WEEK, self._parse_day_of_week),
            (COMMAND, self._parse_command),
        ]

    @staticmethod
    def _get_range(value):
        """
        Gets range E.g 1-5 results in 1, 2, 3, 4, 5
        """
        value = map(int, value.split('-'))
        if value[0] > value[1]:
            return INVALID_INPUT

        return ' '.join(map(str, range(value[0], value[1] + 1)))

    @staticmethod
    def _get_values(value):
        """
        Gets values E.g 1,5 results in 1 5
        """
        value = map(int, value.split(','))
        return ' '.join(map(str, sorted(value)))

    @staticmethod
    def _get_increments(type, value):
        """
        Gets values E.g */5 results in 0 5 10 15 20 25 30
        """
        value = map(int, value.replace('*', '0').split('/'))
        if value[1] > MAX_VALUES[type]:
            return INVALID_INPUT

        return ' '.join(map(str, range(value[0], MAX_VALUES[type], value[1])))

    def _parse_helper(self, value, type):
        """
        Parses according to value, returns INVALID_INPUT if no strings match.
        """
        if re.search('[a-zA-Z]', value):
            return INVALID_INPUT

        if value.isdigit():
            if int(value) >= 0 and int(value) < MAX_VALUES[type]:
                return value
        elif value == '*':
            return ' '.join(map(str, range(1, MAX_VALUES[type] + 1)))
        elif '-' in value:
            if re.search('^[0-9]\-[0-9]+$', value):
                return self._get_range(value)
        elif ',' in value:
            if re.search('^[0-9]+([0-9]?\,[0-9]+)+$', value):
                return self._get_values(value)
        elif '/' in value:
            if re.search('^([0-9]+|\*)\/[0-9]+$', value):
                return self._get_increments(type, value)

        return INVALID_INPUT

    def _parse_minute(self):
        """
        Parses minutes.
        """
        return self._parse_helper(self.minute, MINUTE)

    def _parse_hour(self):
        """
        Parses hour.
        """
        return self._parse_helper(self.hour, HOUR)

    def _parse_day_of_month(self):
        """
        Parses day of month.
        """
        return self._parse_helper(self.day_of_month, DAY_OF_MONTH)

    def _parse_month(self):
        """
        Parses day of month.
        """
        for key, val in MONTHS.iteritems():
            self.month = self.month.replace(key, val)

        return self._parse_helper(self.month, MONTH)

    def _parse_day_of_week(self):
        """
        Parses day of week.
        """
        for key, val in WEEK_DAYS.iteritems():
            self.day_of_week = self.day_of_week.replace(key, val)

        return self._parse_helper(self.day_of_week, DAY_OF_WEEK)

    def _parse_command(self):
        """
        Parses command.
        """
        return self.command

    @staticmethod
    def _print_argument(type, parser):
        print type.ljust(14) + parser()

    def parse(self):
        """
        Parse method.
        """
        for type, parser in self._parser_map():
            self._print_argument(type, parser)


def instructions():
    print """
        Input format - minute hour day-of-month month day-of-week command
        E.g */15 0 1,15 \* 1-5 /user/bin/find

        Note that * needs to be escaped E.g \*
    """


if __name__ == '__main__':
    if '--help' in sys.argv:
        instructions()
    else:
        if len(sys.argv) != 7:
            instructions()
        else:
            parser = CronExpressionParser(sys.argv[1:])
            parser.parse()
