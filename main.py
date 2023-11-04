# x Proof-of-concept scraping
# Lage analyse av scraping data.
# Lage database og lagre scraping data.
# Visualisere resultatene: Nettside med liste over interessante stillinger


import requests
from bs4 import BeautifulSoup
import time


# https://www.finn.no/job/fulltime/search.html?location=1.20001.20061&occupation=0.23
def parse_finn_stillingsliste(url):
    list_of_stillinger = []

    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html.parser")

    articles = soup.select("article > .flex")
    for a in articles:
        title_link = a.select_one("h2 > a")
        stillingstittel = a.select_one("div.font-bold")
        arbeidsgiver = a.select_one("div.flex-col > span:nth-of-type(1)")

        utlysningstittel = title_link.text
        url = title_link["href"]
        if stillingstittel:
            stillingstittel = stillingstittel.text
        if arbeidsgiver:
            arbeidsgiver = arbeidsgiver.text

        list_of_stillinger.append(
            {
                "utlysningstittel": utlysningstittel,
                "url": url,
                "stillingstittel": stillingstittel,
                "arbeidsgiver": arbeidsgiver,
            }
        )

    return list_of_stillinger


def les_finn_stilling(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    body = soup.select_one("div.import-decoration")
    if body:
        return body.text
    else:
        return None


liste_med_stillinger = parse_finn_stillingsliste(
    "https://www.finn.no/job/fulltime/search.html?location=1.20001.20061&occupation=0.23"
)
for stilling in liste_med_stillinger:
    print(stilling)
    print(les_finn_stilling(stilling["url"]))

    # print(les_finn_stilling("https://www.finn.no/job/fulltime/ad.html?finnkode=327073903"))

    time.sleep(3)

# for stilling in liste_med_stillinger:
#    print(stilling)
