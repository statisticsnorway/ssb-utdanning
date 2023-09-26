import os

def sjekk_miljo() -> str:
    if os.path.isdir("/ssb/bruker/felles"):
        miljo = "PROD"
    elif "dapla" in str(dict(os.environ).values()):
        miljo = "DAPLA"
    else:
        raise OSError("Ikke i prodsonen, eller på Dapla?")
    return miljo