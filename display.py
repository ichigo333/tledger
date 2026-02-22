import pandas as pd
from pandas import DataFrame
from datetime import date, timedelta
from tabulate import tabulate
from options import *

TABLE_FORMAT = "fancy_outline"

def display(type: str, table: DataFrame, day: date | None = None):
    print(f"Displaying: {type}")

    table = table.replace(0, "-")
    
    if type == TODAY:
        display_single_day(date.today(), table)
    elif type == YESTERDAY:
        display_single_day(date.today()-timedelta(days=1), table)
    elif type == DAY:
        display_single_day(day, table)
    elif type == MONTH:
        display_month(table)


def display_single_day(day: date | None , table: DataFrame):
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


def display_month(table: DataFrame):
    if "Total" in table.index:
        rows = table.drop("Total")
        separator = pd.Series(["─" * 3] * len(table.columns), index=table.columns, name="─" * 10)
        display = pd.concat([rows, separator.to_frame().T, table.loc[["Total"]]])

    print(tabulate(display, headers="keys", tablefmt=TABLE_FORMAT)) # type: ignore[arg-type]
