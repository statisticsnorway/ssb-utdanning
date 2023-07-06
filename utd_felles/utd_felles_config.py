import os

class Singleton():
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.singleton_init(*args, **kwds)
        return it


class UtdFellesConfig(Singleton):
    def singleton_init(self):
        self.MILJO = self.sjekk_miljo()
        self.TESTING = False
        self.MOCKING = False

    @staticmethod
    def sjekk_miljo() -> str:
        if "FELLES" in os.environ.keys():
            miljo = "PROD"
        elif "dapla" in str(dict(os.environ).values()):
            miljo = "DAPLA"
        else:
            raise OSError("Ikke i prodsonen, eller på Dapla?")
        return miljo
