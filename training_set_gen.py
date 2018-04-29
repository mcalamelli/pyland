# pylint: disable=locally-disabled,missing-docstring,invalid-name,line-too-long
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dict', '-d',
                    type=argparse.FileType('r'),
                    metavar='<dict>',
                    help='Specifica il file dizionario.')
args = parser.parse_args()

#print('Analisi del file: %s\n' % args.dict.name)
with open("training_set.txt", "w") as output_file:
    for line in open(args.dict.name):
        print("Inverti {}".format(line), file=output_file, end='')
        print("Inverti la parola {}".format(line), file=output_file, end='')
