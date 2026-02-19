import argparse
import pandas as pd
from pandas import DataFrame
from datetime import date, timedelta
from tabulate import tabulate, SEPARATING_LINE
from typing import cast

TABLE_FORMAT = "fancy_outline"
TODAY = "today"
YESTERDAY = "yesterday"
MONTH = "month"

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


def show(type: str):
    file_name = f"{date.today().year}-{date.today().month}.txt"
    print(f"Reading file: {file_name}")
    print(f"Displaying: {type}")

    table = read_file(file_name)
 
    if type == TODAY:
        show_single_day(date.today(), table)
    elif type == YESTERDAY:
        show_single_day(date.today()-timedelta(days=1), table)
    elif type == MONTH:
        show_month(table)


def show_single_day(day: date, table):
    day_str = str(day)
    print(f"Date: {day_str}")
    single_day = table.loc[[day_str]]
    print(tabulate(single_day, headers="keys", tablefmt=TABLE_FORMAT))


def show_month(table):
    if "Total" in table.index:
        rows = table.drop("Total")
        separator = pd.Series(["─" * 3] * len(table.columns), index=table.columns, name="")
        display = pd.concat([rows, separator.to_frame().T, table.loc[["Total"]]])
        assert isinstance(display, DataFrame)

    print(tabulate(display, headers="keys", tablefmt=TABLE_FORMAT)) # type: ignore[arg-type]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="tledger")
    parser.add_argument("-a", "--add", type=str, help="Add entry, requires category.  Defaults to today's date.")
    parser.add_argument("-t", "--time", type=int, help="Time in minutes.")
    parser.add_argument("-d", "--day", type=int, help="Specify day of the month. Used for date of current entry.")
    parser.add_argument("-s", "--show", type=str, choices={TODAY, YESTERDAY, MONTH}, help="Show summary")

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
        