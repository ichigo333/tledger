import pandas as pd
from datetime import date
from typing import cast


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

    return table