import pandas as pd
from io import StringIO


class UtdKatalog:
    def __init__(self,
                 data: pd.DataFrame,
                 key_col: str,
                 **metadata,
                ):
        self.data = data
        self.key_col = key_col
        for key, value in metadata.items():
            setattr(self, key, value)

    def __str__(self):
        result = "En Katalog fra utdannings-fellesfunksjonene."
        for key, attr in vars(self).items():
            if key != "data":
                result += f"\n{key}: {attr}"
        result += "\n\nKolonne-info:\n"
        buf = StringIO()
        self.data.info(buf=buf)
        result += buf.getvalue()
        return result

    def to_dict(self, 
                col: str = "", 
                level: int = 0,
                key_col: str = "",) -> dict:
        if not key_col:  # If not passed in to function
            key_col = self.key_col
        if not key_col:  # If not registred in class-instance
            key_col = self.data.columns[0]  # Just pick the first column
        if not col:
            col = self.data.columns[1]  # Just pick the second column
        if level:
            mask = self.data[key_col].str.len() == level
            return dict(zip(self.data[mask][key_col], self.data[col]))
        return dict(zip(self.data[key_col], self.data[col]))

    def apply_format(self,
                     df: pd.DataFrame,
                     catalog_col_name: str = "",
                     data_key_col_name: str = "",
                     catalog_key_col_name: str = "",
                     new_col_data_name: str = "",
                     level: int = 0,
                     ordered: bool = False,
                     remove_unused: bool = False) -> pd.DataFrame:
        # Guessing on key column name
        if not data_key_col_name:
            data_key_col_name = catalog_key_col_name
        if not data_key_col_name:
            data_key_col_name = self.key_col
        if not data_key_col_name:
            self.data.columns[0]
        if not catalog_key_col_name:
            catalog_key_col_name = data_key_col_name

        # Guessing on col name
        if not catalog_col_name:
            catalog_col_name = self.data.columns[1]
        if not new_col_data_name:
            new_col_data_name = catalog_col_name

        print(f"""
        {new_col_data_name=}
        {data_key_col_name=}
        {catalog_col_name=}
        {catalog_key_col_name=}""")

        mapping = self.to_dict(col=catalog_col_name,
                               level=level,
                               key_col=catalog_key_col_name)
        mapping_unique_vals = list(pd.unique(list(mapping.values())))
        df[new_col_data_name] = (df[data_key_col_name]
                                 .map(mapping))
        try:
            series = df[new_col_data_name].copy()
            series = (series.astype(
                pd.CategoricalDtype(
                    categories=mapping_unique_vals,
                    ordered=ordered)
                        )
                     )
            if remove_unused:
                series = series.cat.remove_unused_categories()
            df[new_col_data_name] = series
        except ValueError as e:
            print(f"Couldnt convert column {new_col_data_name} to categorical because of error: {e}")
        
        return df
