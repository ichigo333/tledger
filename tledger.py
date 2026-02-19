import argparse
import pandas as pd
from pandas import DataFrame
from datetime import date, timedelta
from tabulate import tabulate
from typing import cast


TABLE_FORMAT = "fancy_outline"
TODAY = "today"
YESTERDAY = "yesterday"
MONTH = "month"
DAY = "day"


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

    table.loc["Total"] = table.sum()
    total_min = cast(int, table.at["Total", "total"])
    table.loc["Total", "h:m"] = f"{total_min // 60}h {total_min % 60}m"

    table = table.replace(0, "-")
    return table


def show(type: str, day: date | None = None):
    file_name = f"{date.today().year}-{date.today().month}.txt"
    print(f"Reading file: {file_name}")
    print(f"Displaying: {type}")

    table = read_file(file_name)
 
    if type == TODAY:
        show_single_day(date.today(), table)
    elif type == YESTERDAY:
        show_single_day(date.today()-timedelta(days=1), table)
    elif type == DAY:
        show_single_day(day, table)
    elif type == MONTH:
        show_month(table)
        

def show_single_day(day: date | None , table: DataFrame):
    if not day:
        day_str = str(date.today())
    else:
        day_str = str(day)

    print(f"Date: {day_str}")

    if day_str not in table.index:
        print(f"No entry found for {day_str}")
        return

    single_day = table.loc[[day_str]]

    # know issue with tabulate type stubs, have to ignore type
    print(tabulate(single_day, headers="keys", tablefmt=TABLE_FORMAT)) # type: ignore[arg-type]


def show_month(table: DataFrame):
    if "Total" in table.index:
        rows = table.drop("Total")
        separator = pd.Series(["─" * 3] * len(table.columns), index=table.columns, name="─" * 10)
        display = pd.concat([rows, separator.to_frame().T, table.loc[["Total"]]])

    print(tabulate(display, headers="keys", tablefmt=TABLE_FORMAT)) # type: ignore[arg-type]


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

        show(args.show, selected_day)
        