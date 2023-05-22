import pandas as pd


def apply_format(col: pd.Series,
                 mapping: dict,
                 ordered: bool = False,
                 remove_unused: bool = False) -> pd.Series:
    series = (col.map(mapping)
            .astype(pd.CategoricalDtype(categories=list(pd.unique(list(mapping.values()))),
                                        ordered = ordered)))
    if remove_unused:
        return series.cat.remove_unused_categories()
    return series