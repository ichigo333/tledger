import pandas as pd
import os
from datetime import date
from typing import cast


def save_entry(file_name: str, ttype: str, amount: int, selected_date=date.today()):
    print(f"Entry: {selected_date} {ttype} {amount}")
    print(f"Writing to file: {file_name}")

    with open(file_name, 'a') as file:
        file.write(f"{selected_date} {ttype} {amount}\n")


def read_file(file_name: str):
    if not os.path.isfile(file_name):
        print(f"No data found.  File name: {file_name}")
        exit()

    print(f"Reading file: {file_name}")
    data_frame = pd.read_csv(file_name, sep=" ", names=["date", "type", "value"])
    
    table = data_frame.pivot_table(index="date", columns="type", values="value", aggfunc="sum", fill_value=0)
    table = table.astype(int)
    table["total"] = table.sum(axis=1)
    table["h:m"] = table["total"].apply(lambda x: f"{int(x) // 60}h {int(x) % 60}m")

    table.loc["Total"] = table.sum()
    total_min = cast(int, table.at["Total", "total"])
    table.loc["Total", "h:m"] = f"{total_min // 60}h {total_min % 60}m"

    return table