from ssb_utdanning.format.formats import UtdFormat


def test_UtdFormat_simplekey() -> None:
    frmt = UtdFormat({"10": "teens"})
    assert frmt["10"] == "teens"


def test_UtdFormat_intstr_confusion() -> None:
    frmt = UtdFormat({"10": "teens"})
    assert frmt[10] == "teens"


def test_UtdFormat_intstr_confusion_intfirst() -> None:
    frmt = UtdFormat({10: "teens"})
    assert frmt["10"] == "teens"


def test_UtdFormat_range() -> None:
    frmt = UtdFormat({"10-20": "teens"})
    assert frmt[12] == "teens"


def test_UtdFormat_add_range() -> None:
    frmt = UtdFormat()
    frmt["10-20"] = "teens"
    assert frmt[12] == "teens"


def test_UtdFormat_other() -> None:
    frmt = UtdFormat({"oThEr": "teens"})
    assert frmt["other"] == "teens"
    assert frmt[12] == "teens"


def test_UtdFormat_add_other() -> None:
    frmt = UtdFormat()
    frmt["oThEr"] = "teens"
    assert frmt[12] == "teens"


def test_UtdFormat_add_NA() -> None:
    frmt = UtdFormat()
    frmt["<NA>"] = "teens"
    assert frmt["."] == "teens"
