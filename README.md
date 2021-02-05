# Fellesfunksjoner for 360
> En test for å se om fellesfunksjonene våre kan organiseres som ett nbdev-prosjekt


This file will become your README and also the index of your documentation.

## Install

`pip install ssb_fellesfunksjoner_360`

## Hvordan bruke modulen

Etter å ha importert modulen, så kan du feks bruke denne funksjonen for å hente noe fra KLASS-apiet som en pandas dataframe.

```python
from ssb_fellesfunksjoner_360 import klass
```

```python
gjeld_fylke = klass.get_pandas('http://data.ssb.no/api/klass/v1/versions/1158', 'classificationItems')
gjeld_fylke
```
