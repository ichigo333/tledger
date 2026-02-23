import argparse
import os
from datetime import date
from storage import save_entry, read_file
from options import *
from display import display
from config_handler import load_config

def are_args_validated(args) -> bool:
    if args.add and not args.time:
        print("Error: --add option requires --time (-t) option")
        return False
    if (args.add and args.month) and not args.day:
        print("Error: --month option requires --day option when using --add")
        return False
    if args.show and args.show == DAY and not args.day:
        print("Error: --show day option requires --day [num] option")
        return False
    if args.day and (args.day < 1 or args.day > 31):
        print("Error: for --day [num] option, [num] must be between 1 and 31")
        return False
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="tledger")
    parser.add_argument("-a", "--add", type=str, help="Add entry, requires category.  Defaults to today's date.")
    parser.add_argument("-t", "--time", type=int, help="Time in minutes.")
    parser.add_argument("-d", "--day", type=int, help="Specify day of the month. Used for date of current entry or with --show day option")
    parser.add_argument("-m", "--month", type=int, help="Specify month of the year. Used for date of current entry or with --show day option")
    parser.add_argument("-s", "--show", type=str, choices={TODAY, YESTERDAY, MONTH, DAY}, help="Show summary")

    args = parser.parse_args()

    if not are_args_validated(args):
        exit()

    data_dir = os.path.expanduser(load_config()["data_dir"])

    selected_date = date.today()
    if args.day:
        selected_date = date(year=selected_date.year, month=selected_date.month, day=args.day)
    if args.month:
        selected_date = date(year=selected_date.year, month=args.month, day=selected_date.day)

    file_name = f"{data_dir}/{selected_date.year}-{selected_date.month:02d}.txt"

    if args.add and args.time:
        save_entry(file_name, args.add, args.time, selected_date)  
    elif args.show:
        table = read_file(file_name)
        display(args.show, table, selected_date)
        