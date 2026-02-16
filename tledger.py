import argparse
from datetime import date


def saveEntry(ttype: str, amount: int, date=date.today()):
    file_name = f"{str(date.year)}-{str(date.month)}.txt"
    print(file_name)
    with open(file_name, 'a') as file:
        file.write(f"{date} {ttype} {amount}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="tledger")
    parser.add_argument("-a", "--add", type=str, help="Add entry, requires category.  Defaults to today's date.")
    parser.add_argument("-t", "--time", type=int, help="Time in minutes.")
    parser.add_argument("-d", "--day", type=int, help="Specify day of the month. Used for date of current entry.")


    args = parser.parse_args()

    if args.add and args.time:
        print(f"{date.today()} {args.add} {args.time}")

        if args.day:
            day = date(year=date.today().year, month=date.today().month, day=args.day)
            saveEntry(args.add, args.time, day)
        else:
            saveEntry(args.add, args.time)
    