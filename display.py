import pandas as pd
from pandas import DataFrame
from datetime import date, timedelta
from tabulate import tabulate
from options import *

TABLE_FORMAT = "fancy_outline"

def display(type: str, table: DataFrame, selected_date: date):
    print(f"Displaying: {type}")

    table = table.replace(0, "-")
    
    if type == TODAY:
        display_single_day(date.today(), table)
    elif type == YESTERDAY:
        display_single_day(date.today()-timedelta(days=1), table)
    elif type == DAY:
        display_single_day(selected_date, table)
    elif type == MONTH:
        display_month(table)


def display_single_day(selected_date: date, table: DataFrame):
    print(f"Date: {selected_date}")

    if str(selected_date) not in table.index:
        print(f"No entry found for {selected_date}")
        return

    single_day = table.loc[[str(selected_date)]]

    # know issue with tabulate type stubs, have to ignore type
    print(tabulate(single_day, headers="keys", tablefmt=TABLE_FORMAT)) # type: ignore[arg-type]


def display_month(table: DataFrame):
    if "Total" in table.index:
        rows = table.drop("Total")
        separator = pd.Series(["─" * 3] * len(table.columns), index=table.columns, name="─" * 10)
        display = pd.concat([rows, separator.to_frame().T, table.loc[["Total"]]])

    print(tabulate(display, headers="keys", tablefmt=TABLE_FORMAT)) # type: ignore[arg-type]
