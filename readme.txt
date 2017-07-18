Vari script Python realizzati da me.

* mailstat.py
Lo script visualizza alcuni dati statistici relativi alle email presenti in una cartella, leggendo un file .csv creato usando l'estensione ImportExportTools di Thunderbird. Il file di default è index.csv ma è possibile specificarne un altro da riga di comando.
Ecco un esempio di esecuzione:

$ python mailstat.py -i index_small.csv
Analisi del file: index_small.csv

Intervallo di tempo: 09/03/2016 -> 28/04/2017

Conteggio email: assistenza -> 22, totali -> 38

Dettagli giornalieri:
 - Data: 04/05/2016 -> 1/1
 - Data: 05/05/2016 -> 0/1
 - Data: 09/03/2016 -> 1/1
 - Data: 10/05/2016 -> 1/2
 - Data: 18/04/2016 -> 1/2
 - Data: 18/05/2016 -> 1/1
 - Data: 19/04/2016 -> 1/1
 - Data: 19/05/2016 -> 0/5
 - Data: 27/04/2017 -> 9/10
 - Data: 28/04/2017 -> 7/11
 - Data: 29/03/2016 -> 0/1
 - Data: 30/03/2016 -> 0/2

 * test_apiai.py
 Un semplice script di esempio che utilizza l'SDK di api.ai per Python

* pylife/*
Una prova di vita artificiale 

* myclass.py, testmyclass.py
Codice di esempio per l'uso delle classi

* csvproc.py
Lo script esegue delle elaborazioni su tutti i file CSV presenti nella directory corrente (i file CSV sono quelli che si scaricano)
dal portale Paymonitoring, relativi alle vendite dei prodotti) e poi li converte in XLSX.