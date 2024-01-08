# ML-draftarea
## About

The goal is to build a neural network regression model that utilizes public data from Tilastokeskus to predict financial outcomes, specifically focusing on variables such as population demographics and employment statistics. This project aims to provide a valuable tool for financial decision-making, offering insights based on the analysis of relevant socioeconomic factors. By leveraging the power of neural networks, we seek to enhance the accuracy and effectiveness of our regression model, ultimately assisting users in making informed and data-driven financial decisions.


## Viimeisimpiä muutoksia:
 - Refaktorointia

## Ajo-ohjeet
[Miniconda3](https://docs.conda.io/projects/miniconda/en/latest/) tulee asentaa. Minun tarvitsi myös ajaa 'conda init bash' komento, jotta conda osasi toimittaa asioita. Sen jälkeen juurihakemistossa voi ajaa komennon 'conda create --name <ympäristön nimi> --file requirements.txt' jonka jälkeen 'conda activate <ympäristön nimi>' aktivoi ympäristön. Siellä voi ajaa 'python3 main.py' ja muuta kivaa sitten. 'conda deactivate' deaktivoi ympäristön.
## Löytyy:
 - Kirjan esimerkki ja sitä mukaileva mallin alustus
 - yksittäinen tietokanta, joka sisältää vuosikatteet, väestörakenteet ja bkt:n
 - malleja voi luoda ja kouluttaa ja analysoida jos on paljon aikaa.
 - Päiväkirja pdf muodossa
## Kysymyksiä:
 - mitä dataa inputtiin?
	- ikärakenteen lisäksi esim. [työllisyys- ja työttömyysasteet alueittain](https://pxdata.stat.fi/PxWeb/pxweb/fi/StatFin/StatFin__tyokay/statfin_tyokay_pxt_115x.px/table/tableViewLayout1/). Exceli ladattu
	- [työssäkäynti alueittain (työpaikat alueella)](https://pxdata.stat.fi/PxWeb/pxweb/fi/StatFin/StatFin__tyokay/statfin_tyokay_pxt_115p.px/). Exceli ladattu, näytti sisältävän seuraavan bullet pointin toiveen
	- alueen työlliset koulutustason mukaan tms. [samassa tilastossa](https://pxdata.stat.fi/PXWeb/pxweb/fi/StatFin/StatFin__tyokay/?tablelist=true)
	- inputissa olisi hyvä mahdollistaa esim. -5 tai -3 vuoden lägi (esim. vuosien 2018-2020 väestörakenteet voivat kaikki olla merkittäviä inputteja vuoden 2021 mallissa). Tämä onnistuu kohtuu kevyesti ajoympäristössä. Syö vektoreita. Kolmen vuoden lagi vei vektorien määrän 6800 -> 4400. Pitää ihmetellä testailla ja pyöritellä, mikä tuottaa parhaimmat tulokset.
 - mitä dataa outputtiin?
	- alkuun tärkein **vuosikate**, mutta myös toimintakate voi olla mielenkiintoinen mallin arvioimiseksi
 - miten implementoida puuttuvat datat nolliksi? Tämän pitäisi tapahtua itsekseen, mutta pitää pitää silmällä, ettei kuiteinkin sotke juttuja

## Tietokannasta:
 - Taulukot "Asuinkunnassa" ja "Pendelöivät" sisältävät ikäluokittain ja koulutusasteittain kunnassa asuvat henkilöt, jotka käyvät asuinkunnassaan töissä tai matkustavat muualle töihin. Esim sarake Toinen24 viittaa toisen asteen koulutukseen omaaviin 17-24 vuotiaisiin ja Ei34 25-34-vuotiaisiin ilman korkeampaa koulutusta. Alle 17- ja yli 74-vuotiaat jäivät näistä tauluista (ainakin toistaiseksi) pois.
 - Vaestorakenne jakaa ikäluokat nuoriin (alle 18), aikuisiin (18-64) ja iäkkäisiin (65+) ja jakaa niiden sisällä vielä muutamaan eri kategoriaan.
 - Vuosikate sisältää tällä hetkellä vuosikatteen ja toimintakatteen. Jälkimmäinen on vaihtelevasti saatavilla
 - BKT on ainoa, joka ei sisällä kuntatunnusta

## TODO:
 - Lisää testejä 
 - lisää dataa
 - refaktorointia? Mie helposti kirjotan monoliittia.. Tuli mieleen, että testit voisi eriyttää mainista omiin tiedostoihinsa ja sitten mainista vaan ajaa sen mitä tekee mieli.. 
## Huomioita:
 - vuosikatteiden yksikkö on 1000e tällä hetkellä*. Tää ois hyvä skaalaa mallikohtaisesti johonkin järkevään missä tulokset esim välillä 0-100
 - Kaveri vinkkasi, että  bayesläisen tilastotieteen avuista voisi olla hyötyä meidän prokkiksessa. Hänen kirjasuositukset: 
   - Gelman et al. Bayesian Data Analysis (hieman eksaktimpi ja vähän raskaampi)
   - Kruschke: Doing Bayesian Data Analysis (nimikin kertoo jo että miten eroaa yo kirjasta :D) avaa helpommin käsitteitä ja painopiste soveltamisessa 


*main.py sisältää tällä hetkellä rivin (viime tarkistuksella rivi nro 12), joka skaalaa yksikön miljoonaksi euroksi. Tämä ei suorilta parantanut tuloksia, mutta ehkä silti wörttiä
