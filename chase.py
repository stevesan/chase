# Quick script to plot your Chase account balance over time. Download "All activity" as CSV :)

# Useful for skipping large transfers, etc. that aren't typical spending/earning.
LARGE_TRANSACTION_DOLLARS = 9999

import csv
import pylab
import matplotlib
import sys
import datetime

with open(sys.argv[1], 'rb') as csvf:
    reader = csv.reader(csvf, delimiter=',', quotechar='"')
    header = reader.next()
    print header
    balcol = -1
    amtcol = -1
    datecol = -1

    dates = []
    amounts = []

    for i in range(len(header)):
        if header[i] == 'Balance':
            balcol = i
        elif header[i] == 'Amount':
            amtcol = i
        elif header[i] == 'Posting Date':
            datecol = i

    for row in reader:
        amt = float(row[amtcol])
        datestr = row[datecol]
        mm, dd, yyyy = [int(part) for part in datestr.split('/')]
        dt = datetime.datetime(yyyy, mm, dd)

        if abs(amt) > LARGE_TRANSACTION_DOLLARS:
            print 'skipping large transaction: ' + str(row)
            continue
        dates.insert(0, dt)
        amounts.insert(0, amt)

    bals = pylab.cumsum(amounts)

    dates = matplotlib.dates.date2num(dates)
    pylab.plot_date(dates, bals)
    pylab.grid(True)
    pylab.show()
