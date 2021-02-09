# Fellesfunksjoner for 360
> En test for å se om fellesfunksjonene våre kan organiseres som ett nbdev-prosjekt


This file will become your README and also the index of your documentation.

## Install

`pip install ssb_fellesfunksjoner_360`

## Bruk help() på modulene

```python
import ssb_fellesfunksjoner_360 as ssb360
```

```python
help(ssb360)
```

    Help on package ssb_fellesfunksjoner_360:
    
    NAME
        ssb_fellesfunksjoner_360
    
    PACKAGE CONTENTS
        _nbdev
        klass
        sporre
    
    VERSION
        0.0.1
    
    FILE
        /home/jovyan/ssb_fellesfunksjoner_360/ssb_fellesfunksjoner_360/__init__.py
    
    


```python
help(ssb360.klass)
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-25-3ec725b7345e> in <module>
    ----> 1 help(ssb360.klass)
    

    AttributeError: module 'ssb_fellesfunksjoner_360' has no attribute 'klass'


## Hvordan bruke modulen

Etter å ha importert modulen, så kan du feks bruke denne funksjonen for å hente noe fra KLASS-apiet som en pandas dataframe.

```python
from ssb_fellesfunksjoner_360 import klass
```

```python
gjeld_fylke = klass.get_pandas('http://data.ssb.no/api/klass/v1/versions/1158', 'classificationItems')
gjeld_fylke
```
