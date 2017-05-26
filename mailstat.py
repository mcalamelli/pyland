# pylint: disable=locally-disabled,missing-docstring,invalid-name,unused-variable,line-too-long

import csv
import argparse


def file_len(filename):
    with open(filename) as f:
        i = 0
        for i, l in enumerate(f):
            pass
    return i + 1


donotcount = []
donotcount.append('vierino')  # Veronica
donotcount.append('mcalamelli')  # Io
donotcount.append('bellagamba')  # Massi
donotcount.append('mmagnani')  # Massimo
donotcount.append('avalbonesi')  # Valbo
donotcount.append('lruggeri')  # Lorella
donotcount.append('obucci')  # Oscar
donotcount.append('@wetransfer')  # Wetransfer
donotcount.append('noreply@segre')  # Segretaria24
donotcount.append('info@segre')  # Segretaria24

stats = dict()

count = 0
startdate = ''
enddate = ''

parser = argparse.ArgumentParser()
parser.add_argument('--input',
                    '-i',
                    type=argparse.FileType('r'),
                    default='index.csv',
                    metavar='<inputfile>',
                    help='Specifica il file da controllare (default: index.csv)')
args = parser.parse_args()

print('Analisi del file: %s\n' % args.input.name)

lc = file_len(args.input.name)

mailcounter = csv.reader(args.input, delimiter=',', quotechar='"')

# Iterazione all'interno delle email
for mail in mailcounter:
    # La prima email dell'elenco, da qui prendo la data iniziale
    if mailcounter.line_num == 1:
        startdate = mail[len(mail) - 3].split(' ', 1)[0]
    # L'ultima email dell'elenco, da qui prendo la data finale
    if mailcounter.line_num == lc:
        enddate = mail[len(mail) - 3].split(' ', 1)[0]
    valid = False

    # Iterazione all'interno degli elementi da non considerare
    for item in donotcount:
        if mail[1].find(item) != -1:
            # Un elemento da non considerare è stato trovato
            # Imposto la non validità della email ed esco
            valid = False
            break
        else:
            # Imposto la temporanea validità e proseguo
            valid = True

    # La email è valida?
    if valid:
        # La mail è valida e la conteggio
        count += 1

    # Conteggi statistici
    if stats.get(str(mail[len(mail) - 3].split(' ', 1)[0])) is None:
        # La data corrente non è presente nelle statistiche
        stats[str(mail[len(mail) - 3].split(' ', 1)[0])] = str(int(valid)) + '/1'
    else:
        # La data corrente è presente nelle statistiche
        tp, tc = stats.get(str(mail[len(mail) - 3].split(' ', 1)[0])).split('/')
        stats[str(mail[len(mail) - 3].split(' ', 1)[0])] = str(int(tp) + int(valid)) + '/' + str(int(tc) + 1)

print('Intervallo di tempo: %s -> %s\n' % (startdate, enddate))

print("Conteggio email: assistenza -> %d, totali -> %d\n" % (count, lc))

print("Dettagli giornalieri:")
# Ordino le statistiche
sstats = sorted(stats.items())
for k, v in sstats:
    print(" - Data: %s -> %s" % (k, v))
