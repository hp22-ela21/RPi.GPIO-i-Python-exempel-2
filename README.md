# RPi.GPIO-i-Python-exempel-2
Eventdetektering samt användning av listor i Python.
I detta exempel lagras tre led-objekt i en lista. Eventdetektering sker på stigande flank för en tryckknapp för att toggla lysdiodernas tillstånd mellan
att blinka i en sekvens samt vara släckta vid nedtryckning av tryckknappen, då en callback-rutin anropas, vilket fungerar ungefär som en avbrottsrutin.
En bounce-tid på 500 ms används för att minska påverkan av kontaktstudsar vid nedtryckning av tryckknappen.
