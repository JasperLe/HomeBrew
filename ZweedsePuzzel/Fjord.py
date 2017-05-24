"""
Auteur: Jasper Lelijveld
Datum: 25-april-2017
Time spent: +- 1.5 uur

Dit is een script om Zweedse Puzzels mee op te lossen. Ondanks dat vooral Noorwegen bekend staat
om zijn Fjorden heb ik dit script toch Fjord genoemd.

Hij vraagt om een woord, parsed twee online woordenboeken en filtert de resultaten op
basis van woordlengte. Daarnaast is er een optie om te zoeken naar plaatsen, gemeenten
of provincies. Je bent op zoek naar een plaatsnaam met 3 letters in Flevoland?
Voer Flevoland en 3 in en hij returned de mogelijkheden.
"""
import bs4
import requests


def main():
    # vraag voor eigenschappen van het woord
    zoeken = input('Wat wil je zoeken?: ')
    lengte = int(input('Hoeveel letters heeft het woord?: '))
    plaats = input('Is het een plaats? (y/n): ')
    if plaats is 'y':
        plaats_zoeker(zoeken, lengte)
    else:
        # call de webpagina met de aanwijzing als zoekterm
        res = requests.get('http://synoniemen.net/index.php?zoekterm=%s' % zoeken)
        res2 = requests.get('http://www.mijnwoordenboek.nl/puzzelwoordenboek/%s/1/1' % zoeken)
        res.raise_for_status()
        res2.raise_for_status()
        # creëer de soup
        synoniemenSoup = bs4.BeautifulSoup(res.text, 'html.parser')
        puzzelwoordenSoup = bs4.BeautifulSoup(res2.text, 'html.parser')
        # haal de mogelijkheden uit de soup gebaseerd op de html/css tags
        # puzzelwoordenboek soup
        puzzelwoordentabel = puzzelwoordenSoup.select('tr > td > div')
        # synoniemen soup
        trefwoordtabel = synoniemenSoup.select('.alstrefwoordtabel dd > a')
        synoniemtabel = synoniemenSoup.select('.alssynoniemtabel dd > a')
        # creëer de lijst met ALLE gevonden woorden
        resultaat = trefwoordtabel + synoniemtabel + puzzelwoordentabel
        print('Trefwoorden & synoniemen:')
        # filter op basis van lengte en print de term
        for i in resultaat:
            temp = i.getText()
            if len(temp) == lengte:
                print(temp)


def plaats_zoeker(zoeken, lengte):
    with open('NL.txt') as file:
        # doorzoek iedere line in de txt file
        for line in file:
            words = line.split()
            # kolommen representeren provincie, gemeente en plaats
            if words[2] == zoeken or words[3] == zoeken or words[5] == zoeken:
                if len(words[2]) == lengte:
                    print(words[2])
                elif len(words[3]) == lengte:
                    print(words[3])
                elif len(words[5]) == lengte:
                    print(words[5])

"""main blijft runnen tot je het stop zet"""
while True:
    main()
