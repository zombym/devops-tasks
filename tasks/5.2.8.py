#!/usr/bin/python3
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, nargs="+")
    parser.add_argument("-r", "--ratio", required=True, nargs=1)
    parser.add_argument("-v", dest="verbose", action="count", default=0)

    args = parser.parse_args()
    msg = ""
    if int(args.verbose) > 0:
        print(f"Коэффициент: {int(args.ratio[0])}")
    if int(args.verbose) > 1:
        for a in args.input:
            print(f"{a} * {int(args.ratio[0])} = {int(a) * int(args.ratio[0])}")

    for a in args.input:
        msg = msg + " " + str(int(a) * int(args.ratio[0]))
    print(msg.strip())
