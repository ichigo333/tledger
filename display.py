import pandas as pd
from pandas import DataFrame
from datetime import date, timedelta
from tabulate import tabulate
from options import *

TABLE_FORMAT = "fancy_outline"

EXCLUDE_COLS  = {"total", "h:m"}
EXCLUDE_ROWS  = {"Total"}
SQUARE        = "▇"
HALF_SQUARE   = "▪"
SEP           = "\u200a"
RESET         = "\033[0m"
PASTEL_COLORS = [
    "\033[38;5;153m",  # soft blue
    "\033[38;5;183m",  # soft purple
    "\033[38;5;120m",  # soft green
    "\033[38;5;222m",  # soft yellow
    "\033[38;5;210m",  # soft pink
    "\033[38;5;159m",  # soft cyan
    "\033[38;5;216m",  # soft peach
    "\033[38;5;147m",  # soft lavender
    "\033[38;5;157m",  # soft mint
    "\033[38;5;228m",  # soft cream
    "\033[38;5;219m",  # soft rose
    "\033[38;5;195m",  # soft sky
    "\033[38;5;194m",  # soft sage
    "\033[38;5;225m",  # soft lilac
    "\033[38;5;189m",  # soft periwinkle
]


def display_bar_chart(table: DataFrame, scale: int = 15):
    columns = [col for col in table.columns if col not in EXCLUDE_COLS]
    rows    = table.loc[table.index.difference(EXCLUDE_ROWS)]

    col_totals = {col: int(rows[col].sum()) for col in columns}

    if not col_totals or all(v == 0 for v in col_totals.values()):
        print("Not enough data for graph.")
        return

    label_width = max(len(str(col)) for col in columns)

    print(f"\n  {SQUARE} = {scale} min  {HALF_SQUARE} = {scale // 2} min\n")

    for i, col in enumerate(columns):
        total  = col_totals[col]
        full   = total // scale
        half   = 1 if (total % scale) >= (scale // 2) else 0
        color  = PASTEL_COLORS[i % len(PASTEL_COLORS)]
        blocks = ([SQUARE] * full) + ([HALF_SQUARE] if half else [])
        bar    = SEP.join(blocks) if blocks else ""
        hm     = f"{total // 60}h {total % 60}m"
        label  = str(col).rjust(label_width)
        suffix = f"  {total}m ({hm})" if total > 0 else ""
        
        print(f"  {label}  {color}{bar}{RESET}{suffix}")

    print()


def display(type: str, table: DataFrame, selected_date: date):
    print(f"Displaying: {type}")
    
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
    display = single_day.replace(0, "-")
    # know issue with tabulate type stubs, have to ignore type
    print(tabulate(display, headers="keys", tablefmt=TABLE_FORMAT)) # type: ignore[arg-type]
    display_bar_chart(single_day)


def display_month(table: DataFrame):
    if "Total" in table.index:
        rows = table.drop("Total")
        separator = pd.Series(["─" * 3] * len(table.columns), index=table.columns, name="─" * 10)
        display = pd.concat([rows, separator.to_frame().T, table.loc[["Total"]]])

    display = display.replace(0, "-")
    print(tabulate(display, headers="keys", tablefmt=TABLE_FORMAT)) # type: ignore[arg-type]
    display_bar_chart(table, 60)
