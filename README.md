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




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>code</th>
      <th>parentCode</th>
      <th>level</th>
      <th>name</th>
      <th>shortName</th>
      <th>notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>03</td>
      <td></td>
      <td>1</td>
      <td>Oslo</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>1</th>
      <td>11</td>
      <td></td>
      <td>1</td>
      <td>Rogaland</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>15</td>
      <td></td>
      <td>1</td>
      <td>Møre og Romsdal</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>18</td>
      <td></td>
      <td>1</td>
      <td>Nordland</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>30</td>
      <td></td>
      <td>1</td>
      <td>Viken</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>5</th>
      <td>34</td>
      <td></td>
      <td>1</td>
      <td>Innlandet</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>6</th>
      <td>38</td>
      <td></td>
      <td>1</td>
      <td>Vestfold og Telemark</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>7</th>
      <td>42</td>
      <td></td>
      <td>1</td>
      <td>Agder</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>8</th>
      <td>46</td>
      <td></td>
      <td>1</td>
      <td>Vestland</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>9</th>
      <td>50</td>
      <td></td>
      <td>1</td>
      <td>Trøndelag - Trööndelage</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>10</th>
      <td>54</td>
      <td></td>
      <td>1</td>
      <td>Troms og Finnmark – Romsa ja Finnmárku – Troms...</td>
      <td>None</td>
      <td></td>
    </tr>
    <tr>
      <th>11</th>
      <td>99</td>
      <td></td>
      <td>1</td>
      <td>Uoppgitt</td>
      <td>None</td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>


