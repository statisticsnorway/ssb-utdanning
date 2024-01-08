from ssb_utdanning import UtdFormat


def test_UtdFormat_simplekey():
    frmt = UtdFormat({"10": "teens"})
    assert frmt["10"] == "teens"


def test_UtdFormat_intstr_confusion():
    frmt = UtdFormat({"10": "teens"})
    assert frmt[10] == "teens"


def test_UtdFormat_range():
    frmt = UtdFormat({"10-20": "teens"})
    assert frmt[12] == "teens"


def test_UtdFormat_add_range():
    frmt = UtdFormat()
    frmt["10-20"] = "teens"
    assert frmt[12] == "teens"


def test_UtdFormat_other():
    frmt = UtdFormat({"oThEr": "teens"})
    assert frmt["other"] == "teens"
    assert frmt[12] == "teens"


def test_UtdFormat_add_other():
    frmt = UtdFormat()
    frmt["oThEr"] = "teens"
    assert frmt[12] == "teens"


def test_UtdFormat_add_NA():
    frmt = UtdFormat()
    frmt[float("nan")] = "teens"
    assert frmt["."] == "teens"
