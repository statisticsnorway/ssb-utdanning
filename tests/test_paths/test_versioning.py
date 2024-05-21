from ssb_utdanning.paths import versioning


def test_bump_path() -> None:
    inpath = "/ssb/folder/structure/filename_p2010_p2011_v2.parquet"
    outpath = "/ssb/folder/structure/filename_p2010_p2011_v3.parquet"
    assert outpath == versioning.bump_path(inpath)


def test_get_version() -> None:
    inpath = "/ssb/folder/structure/filename_p2010_p2011_v2.parquet"
    assert 2 == versioning.get_version(inpath)
