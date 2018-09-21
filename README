# Cron expression parser

cron_expression_parser parses an input cron string and expands each field to show the times at which it will run.

The standard cron format with five time fields (minute, hour, day of month, month, and day of week) plus a command is
considered. Special time strings are excluded such as "@yearly".

Field	        Allowed values	    Allowed special characters	Remarks
Minutes     	0–59	            * , -
Hours	        0–23	            * , -
Day of month	1–31	            * , - ? L W	                ? L W only in some implementations
Month	        1–12 or JAN–DEC	    * , -
Day of week	    0–6 or SUN–SAT	    * , - ? L #	                ? L W only in some implementations

https://en.wikipedia.org/wiki/Cron#CRON_expression

## Usage

  - Requirements: Python 2.7
  - Run the following command from within the project root directory
    $ ./run_parser.sh */15 0 1,15 \* 1-5 /user/bin/find
  - Please note that * should be escaped E.g \*

## Expected output

    minute        0 15 30 45
    hour          0
    day_of_month  1 15
    month         1 2 3 4 5 6 7 8 9 10 11 12
    day_of_week   1 2 3 4 5
    command       /user/bin/find

## Testing

  - Tests are located in the test directory
  - Recommendation:
    Create a virtual environment and activate it. Run the following command from within the project root directory to
    install all required packages.

  $ pip install -r requirements.txt

  - To run all tests, run the following command in the project root directory after activating the virtual environment.

  $ python run_tests.py

## Improvements

  - Day of month to include ? L W input options
  - Day of week to include ? L # input options
