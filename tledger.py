import argparse
import pandas as pd
from datetime import date, timedelta
from tabulate import tabulate



def save_entry(ttype: str, amount: int, date=date.today()):
    file_name = f"{str(date.year)}-{str(date.month)}.txt"
    with open(file_name, 'a') as file:
        file.write(f"{date} {ttype} {amount}\n")


def read_file(file_name: str):
    data_frame = pd.read_csv(file_name, sep=" ", names=["date", "type", "value"])
    
    table = data_frame.pivot_table(index="date", columns="type", values="value", aggfunc="sum", fill_value=0)
    table = table.astype(int)
    table["total"] = table.sum(axis=1)
    table["h:m"] = table["total"].apply(lambda x: f"{int(x) // 60}h {int(x) % 60}m")
    table = table.replace(0, "-")
    return table


def show(type: str):
    file_name = f"{date.today().year}-{date.today().month}.txt"
    print(f"Reading file: {file_name}")
    print(f"Displaying: {type}")

    table = read_file(file_name)
 
    if type == "today":
        show_single_day(date.today(), table)
    elif type == "yesterday":
        show_single_day(date.today()-timedelta(days=1), table)
    elif type == "month":
        show_month(table)


def show_single_day(day: date, table):
    day_str = str(day)
    print(f"Date: {day_str}")
    single_day = table.loc[[day_str]]
    print(tabulate(single_day, headers="keys", tablefmt="rounded_outline"))


def show_month(table):
    print(tabulate(table, headers="keys", tablefmt="rounded_outline"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="tledger")
    parser.add_argument("-a", "--add", type=str, help="Add entry, requires category.  Defaults to today's date.")
    parser.add_argument("-t", "--time", type=int, help="Time in minutes.")
    parser.add_argument("-d", "--day", type=int, help="Specify day of the month. Used for date of current entry.")
    parser.add_argument("-s", "--show", type=str, choices={"today", "yesterday", "month"}, help="Show summary")

    args = parser.parse_args()

    if args.add and not args.time:
        print("Error: --add option requires --time (-t) option")

    if args.add and args.time:
        print(f"{date.today()} {args.add} {args.time}")

        if args.day:
            day = date(year=date.today().year, month=date.today().month, day=args.day)
            save_entry(args.add, args.time, day)
        else:
            save_entry(args.add, args.time)
    elif args.show:
        show(args.show)
        