import argparse
from datetime import date
from tabulate import tabulate


def save_entry(ttype: str, amount: int, date=date.today()):
    file_name = f"{str(date.year)}-{str(date.month)}.txt"
    with open(file_name, 'a') as file:
        file.write(f"{date} {ttype} {amount}\n")


def read_file(file_name: str):
    result = {}
    with open(file_name, "r") as file:
        lines = file.readlines()
        for line in lines:
            day,type,value = line.strip().split(" ")
            if day in result.keys():
                if type in result[day].keys():
                    result[day][type] += int(value)
                else:
                    result[day][type] = int(value)
            else:
                result[day] = {type : int(value)}
    return {k: v for k,v in sorted(result.items())}


def show(type: str):
    print(type)
 
    if type == "today":
        file_name = f"{date.today().year}-{date.today().month}.txt"
        result = read_file(file_name)
        print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="tledger")
    parser.add_argument("-a", "--add", type=str, help="Add entry, requires category.  Defaults to today's date.")
    parser.add_argument("-t", "--time", type=int, help="Time in minutes.")
    parser.add_argument("-d", "--day", type=int, help="Specify day of the month. Used for date of current entry.")
    parser.add_argument("-s", "--show", type=str, choices={"today", "yesterday"}, help="--show [today|yesterday|month|all] Show summary")

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
        