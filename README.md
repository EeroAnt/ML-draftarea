# ML-draftarea
readme tässä vaiheessa enempi päiväkirja. repolle järkevä rajenne sit joskus
Luonnoksia potentiaalisista neuroniverkkorakenteista
Alotetaan alusta oikeilla peleillä
Löytyy:
- Kirjan esimerkki ja sitä mukaileva mallin alustus
- sql-tietokanta kuntien väestörakenteista niiltä vuosilta mistä nyt osasin
- python-scripti, jolla yhdistellä eri vuosien exceleitä samasta datasta. vuosikatteet 2002-2014 yhdistetty
Kysymyksiä:
- mitä dataa inputtiin?
    - ikärakenteen lisäksi esim. [työllisyys- ja työttömyysasteet alueittain](https://pxdata.stat.fi/PxWeb/pxweb/fi/StatFin/StatFin__tyokay/statfin_tyokay_pxt_115x.px/table/tableViewLayout1/)
    - [työssäkäynti alueittain (työpaikat alueella)](https://pxdata.stat.fi/PxWeb/pxweb/fi/StatFin/StatFin__tyokay/statfin_tyokay_pxt_115p.px/)
    - alueen työlliset koulutustason mukaan tms. [samassa tilastossa](https://pxdata.stat.fi/PXWeb/pxweb/fi/StatFin/StatFin__tyokay/?tablelist=true)
    - inputissa olisi hyvä mahdollistaa esim. -5 tai -3 vuoden lägi (esim. vuosien 2018-2020 väestörakenteet voivat kaikki olla merkittäviä inputteja vuoden 2021 mallissa)
- mitä dataa outputtiin?
  -   alkuun tärkein **vuosikate**, mutta myös toimintakate voi olla mielenkiintoinen mallin arvioimiseksi
- miten implementoida puuttuvat datat nolliksi?

TODO:
- talousdataexceleistä vuosiltat 2000-2001 ja 2015 eteenpäin uupuu kuntatunnukset

Huomioita:
- vuosikatteiden yksikkö on 1000e tällä hetkellä. Tää ois hyvä skaalaa mallikohtaisesti johonkin järkevään missä tulokset esim välillä 0-100

