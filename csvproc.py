# pylint: disable=locally-disabled,missing-docstring,invalid-name,line-too-long
# -*- coding: utf-8 -*-

import csv
from pathlib import Path
from os import unlink
import openpyxl
from tqdm import tqdm

def file_len(filename):
    with open(filename) as fname:
        i = 0
        for i, l in enumerate(fname):
            pass
    return i + 1

prev = None

p = Path('./')
csvlist = list(p.glob('*.csv'))

if len(csvlist) > 0:
    for item in tqdm(csvlist):
        filecsvin = item
        f = Path(filecsvin)
        filecsvout = f.stem + '-proc.csv'
        filexlsout = f.stem + '.xlsx'

        with open(str(filecsvin), 'r') as csvin:
            with open(filecsvout, 'w') as csvout:
                myreader = csv.reader(csvin, delimiter=',', quotechar='"')
                mywriter = csv.writer(csvout, lineterminator='\n', delimiter=',', quotechar='"')

                lc = file_len(csvin.name)

                processed = []
                header = next(myreader)
                header.insert(0, '')
                processed.append(header)

                for row in myreader:
                    if myreader.line_num >= lc - 1:
                        row.insert(0, '')
                        processed.append(row)
                    elif myreader.line_num % 2 != 0:
                        row.insert(0, str(prev).strip("[").strip("]"))
                        processed.append(row)
                    prev = row
                mywriter.writerows(processed)
                csvout.flush()

        wb = openpyxl.Workbook()
        ws = wb.active
        with open(filecsvout, 'r') as csvproc:
            myreader = csv.reader(csvproc, delimiter=',', quotechar='"')
            for row in myreader:
                ws.append(row)
        wb.save(filexlsout)
        unlink(filecsvout)
else:
    print("Nessun file da elaborare")
