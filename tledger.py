import argparse
import os
from datetime import date
from storage import save_entry, read_file
from options import *
from display import display
from config_handler import load_config

def validate_args(parser: argparse.ArgumentParser, args):
    if args.add:
        if not args.time:
            parser.error("--add option requires --time (-t) option")
        if args.month and not args.day:
            parser.error("--month option requires --day option when using --add")
        if args.year and not args.month:
            parser.error("--year option requires --month option when using --add")

    if args.show == DAY:
        if not args.day:
            parser.error("--show day option requires --day [num] option")
        if args.year and not args.month:
            parser.error("--show day with --year option requires --month [num] option")

    if args.show == MONTH: 
        # if not args.month:
        #     parser.error("--show month option requires --month [num] option")
        if args.day:
            print("Warning: --show month option ignores --day [num] option")


def parse_date(parser: argparse.ArgumentParser, args) -> date:
    today = date.today()
    year  = args.year  or today.year
    month = args.month or today.month
    day   = args.day   or today.day

    try:
        return date(year=year, month=month, day=day)
    except ValueError as e:
        parser.error(f"Invalid date: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="tledger")
    parser.add_argument("-a", "--add", type=str, help="Add entry, requires category.  Defaults to today's date.")
    parser.add_argument("-t", "--time", type=int, help="Time in minutes.")
    parser.add_argument("-d", "--day", type=int, choices=range(1, 32), metavar="DAY[1-31]", 
                        help="Specify day of the month. Used for date of current entry or with --show day option")
    parser.add_argument("-m", "--month", type=int, choices=range(1, 13), metavar="MONTH[1-12]",
                        help="Specify month of the year. Used for date of current entry or with --show day option")
    parser.add_argument("-y", "--year", type=int, help="Specify year. Used for date of current entry or with --show day option")
    parser.add_argument("-s", "--show", type=str, choices={TODAY, YESTERDAY, MONTH, DAY}, help="Show summary")

    args = parser.parse_args()
    validate_args(parser, args)

    selected_date = parse_date(parser, args)

    data_dir = os.path.expanduser(load_config()["data_dir"])
    file_name = f"{data_dir}/{selected_date.year}-{selected_date.month:02d}.txt"

    if args.add and args.time:
        save_entry(file_name, args.add, args.time, selected_date)  
    elif args.show:
        table = read_file(file_name)
        display(args.show, table, selected_date)
        