import sys
import argparse
import get
import parse01
import parse02
import insert
import logging

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p",
    # filename="./error.log",
    # filemode="a"
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", help="get db.conf")
    args = parser.parse_args()
    if len(sys.argv) == 1:
        get.get_pdf()
        v1 = parse01.parse_pdf01("./pdf/")
        v2 = parse02.parse_pdf02("./pdf/")
        insert.insert(v1, v2, 'test')
    elif len(sys.argv) == 3:
        get.get_pdf()
        v1 = parse01.parse_pdf01("./pdf/")
        v2 = parse02.parse_pdf02("./pdf/")
        insert.insert(v1, v2, args.env)
    else:
        print("error param!")
        sys.exit(1)


if __name__ == "__main__":
    main()