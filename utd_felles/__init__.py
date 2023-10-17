from importlib import import_module


__version__ = "0.0.1"
__all__ = []

# Everything we want to be directly importable from under "klass"-package
local_imports = {
    "utd_felles_config": ["UtdFellesConfig"],
    "katalog.kataloger.nuskat": ["get_nuskat"],
    "katalog.kataloger.skoleregister": ["get_skoleregister", "skoleregister_dates"],
    "katalog.katalog": ["UtdKatalog", "create_new_utd_katalog", "open_utd_katalog_from_metadata"],
}

# Loop that imports local files into this namespace and appends to __all__ for star imports
for file, funcs in local_imports.items():
    for func in funcs:
        globals()[func] = getattr(import_module(f"utd_felles.{file}", func), func)
        __all__.append(func)
