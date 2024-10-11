#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import argparse
import re
import requests

def main():
    load_dotenv()
    API_KEY = os.getenv('API_KEY')

    parser = argparse.ArgumentParser(description="Stock Analysis Tool")
    parser.add_argument('--stock', type=str, help='Stock symbol to analyze')
    args = parser.parse_args()

    stock_symbol_pattern = re.compile(r"^\$\w+$")

    if args.stock:
        if stock_symbol_pattern.match(args.stock):
                print(f"Analyzing stock: {args.stock}")
        else:
            print("Invalid stock symbol format. Please use the format: $SYMBOL")
    else:
        args.stock = input("No stock symbol provided. Please enter a stock symbol wiht this format '$SYMBOL': ")
        if stock_symbol_pattern.match(args.stock):
            print(f"Analyzing stock: {args.stock}")
        else:
            print("Invalid stock symbol format. Please use the format: $SYMBOL")

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={args.stock[1:]}&datatype=csv&apikey={API_KEY}"

    stockData = requests.get(url).text

    if "Error Message" in stockData:
        print(f"Error: Could not find stock data for symbol: {args.stock}")
        exit(1)

    lines = stockData.split("\n")
    startDate = lines[1].split(",")[0]
    endDate = lines[-2].split(",")[0]
    print(f"\n----------------------------------------------------------\n")
    print(f"Stock: {args.stock}\n{startDate} to {endDate}")
    print ("{:<8} {:<15} {:<10} {:<10}".format('Date','Open','High','Low','Close'))

    for line in lines:
        data = line.split(",")
        print(data)
        if "timestamp" in data[0]:
            continue
        print ("{:<8} {:<15} {:<10} {:<10}".format(data[0],data[1],data[2],data[3],data[4]))


if __name__ == "__main__":
    main()