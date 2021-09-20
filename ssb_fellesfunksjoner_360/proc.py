# AUTOGENERATED! DO NOT EDIT! File to edit: 04_proc.ipynb (unless otherwise specified).

__all__ = ['df', 'freq']

# Cell
import pandas as pd

# Cell
#stubdata
df = pd.DataFrame(
    [["143612748",	"11.070",	"03", 	"Oslo", 	"66"],
    ["341274090",	"10.130",	"02",	"Akershus(-2019)"	"53"],
    ["884412708",	"10.920",	"03",	"Oslo",	"59"],
    ["595597122",	"46.693",   "12",	"Hordaland (-2019)",	"50"],
    ["084588991",	"09.900",	"02",	"Akershus (-2019)",	"100"]],
    columns = ["work_id",	"nace",	"region_code",	"region",	"employee_points"]
)

# Cell
from IPython.display import display

def freq(df, cols = [], order = 'data', nopercent = False, nocum = False, freq_limit = 0):

    """
    This function tries to mimic some of the functionality of "PROC FREQ" from SAS.\n
    When using crosstab, by using an asterix in a string 'col1*col2', only frequencies are included.\n
    You may use numbers for columns, even negative ones, with an asterix. For example: cols = 'col1*-1', for the column "col1" crosstabbed with the last column.


    Parameters
    ----------
    first "df" : dataframe\n
        Send in the pandas dataframe you want to analyze.
    second "cols" : string, int or list of ints and or strings\n
        Strings may also contain an asterisk '*' between two column-names / ints. To create crosstabs of two columns.
        A list of several strings / ints, will generate multiple frequency-tables from the same dataframe and
    third "order" : string\n
        Only possible alternative to the default 'data' is currently 'freq', actually, if passed anything other than 'data', it will sort by frequency.
    fourth "nopercent" : bool\n
        Will remove the columns 'Percent' and 'Cumulative Percent' if True
    fifth "nocum" : bool\n
        Will remove the columns 'Cumulative Frequency' and 'Cumulative Percent' if True
    sixth "freq_limit" : int \n
        Lower limit for frequency-rows in non-crosstabbed tables. It will remove rows with frequency values below this.

    Returns
    -------
    None\n
        Only displays the frequency tables, does not return a dataframe.

    Raises
    ------
    ValueError\n
        If no cols-parameter is specified.
    """


    # Make a copy of the dataframe, not to mess it up
    dft = df.copy()

    # We need to know which tables to look at
    # 0 alone is a valid input, but not empty strings or lists
    if not cols and cols != 0:
        raise ValueError('Please pass a "cols" parameter witht he columns youd like to take a look at.')

    # Convert cols to list, if its a string
    cols = [cols] if isinstance(cols, str) or isinstance(cols, int) else cols

    # Loop over all the cols you want
    for col in cols:
        #print(col)
        # If int try to get that numbered column
        if isinstance(col, int):
            col = dft.columns[col]
        # If string, try to pick that column

        # What if there is a star in the string?
        if col.find('*') !=-1 :

            # Clean up ints / strings on their way in with asteriks
            col0 = col.split('*')[0]
            try:
                col0 = int(col0)
                if col0 < 0: col0 = dft.shape[1] - col0 - 2
                col0 = dft.columns[col0]
            except:
                ...

            col1 = col.split('*')[1]
            try:
                col1 = int(col1)
                if col1 < 0: col1 = dft.shape[1] - col1 - 2
                col1 = dft.columns[col1]
            except:
                ...

            # Print
            print(col0, '*', col1)

            # Crosstab-function
            datab = pd.crosstab(dft[col0], dft[col1], margins=True, margins_name="Total")

            display(datab)
            # We will exit here if crosstab, since it becomes too complicated otherwise?

        else:
            dfts = dft[col]

            datax = dfts.value_counts()
            if order == 'data':
                datax = datax.sort_index()
            datay = pd.DataFrame({
                    col: datax.index,
                    'Frequency': datax.values,
                    'Percent': ((datax.values/datax.values.sum())*100).round(2),
                    'Cumulative Frequency': datax.values.cumsum(),
                    'Cumulative Percent': ((datax.values.cumsum()/datax.values.sum())*100).round(2)
                    })

            if nopercent:
                datay = datay.drop('Percent', axis = 1)
            if nocum:
                datay = datay.drop('Cumulative Frequency', axis = 1)
            if nocum or nopercent:
                datay = datay.drop('Cumulative Percent', axis = 1)

            if freq_limit and isinstance(freq_limit, int):
                datay = datay[datay['Frequency'] >= freq_limit]

            display(datay.style.hide_index())

    return None