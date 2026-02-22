import argparse
from datetime import date
from storage import save_entry, read_file
from options import *
from display import display


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="tledger")
    parser.add_argument("-a", "--add", type=str, help="Add entry, requires category.  Defaults to today's date.")
    parser.add_argument("-t", "--time", type=int, help="Time in minutes.")
    parser.add_argument("-d", "--day", type=int, help="Specify day of the month. Used for date of current entry or with --show day option")
    parser.add_argument("-m", "--month", type=int, help="Specify month of the year. Used for date of current entry or with --show day option")
    parser.add_argument("-s", "--show", type=str, choices={TODAY, YESTERDAY, MONTH, DAY}, help="Show summary")

    args = parser.parse_args()

    if args.add and not args.time:
        print("Error: --add option requires --time (-t) option")
        exit()
    if args.show and args.show == DAY and not args.day:
        print("Error: --show day option requires --day [num] option")
        exit()
    if args.day and (args.day < 1 or args.day > 31):
        print("Error: for --day [num] option, [num] must be between 1 and 31")
        exit()

    today = date.today()
    if args.add and args.time:
        print(f"{date.today()} {args.add} {args.time}")

        if args.day:
            selected_day = date(year=today.year, month=today.month, day=args.day)
            save_entry(args.add, args.time, selected_day)
        else:
            save_entry(args.add, args.time)
    elif args.show:
        selected_day = None
        if args.day:
            selected_day = date(year=today.year, month=today.month, day=args.day)

        file_name = f"{date.today().year}-{date.today().month}.txt"
        print(f"Reading file: {file_name}")
        table = read_file(file_name)
        display(args.show, table, selected_day)
        