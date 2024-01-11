from datetime import timedelta

from pytest import MonkeyPatch

from src.__version__ import VERSION
from src.roteiro import (
    cli,
    extract_lines,
    extract_timestamp_or_none,
    format_line,
    format_timedelta,
    format_timestamp,
)


def test_extract_lines():
    assert extract_lines("tests/sample.docx") == [
        "0000	Description	0100",
        "Not a line",
        "0130	A Larger Description with symbols such as … or , or ?!@#		0200",
        "0300	No Final timestamp",
        "",
        "Another Not a line after a empty line",
        "",
    ]


def test_extract_lines_accents():
    assert extract_lines("tests/sample_accents.docx") == [
        "Not a line",
        "0000	Description	0100",
        "Not a line either",
        "0130	Description with accents çáã	0200",
        "0300	No Final timestamp",
        "",
        "Another Not a line after a empty line",
        "",
    ]


def test_extract_timestamp():
    assert extract_timestamp_or_none("0848	Description	1006") == (
        "0848",
        "Description",
        "1006",
    )


def test_extract_timestamp_optional_duration():
    assert extract_timestamp_or_none("0848	Description") == (
        "0848",
        "Description",
        None,
    )


def test_extract_timestamp_no_valid_timestamp():
    assert extract_timestamp_or_none("Not a valid timestamp") is None


def test_format_timestamp():
    assert format_timestamp("0848", "Description", "1006") == (
        "0848",  # Name
        timedelta(hours=0, minutes=8, seconds=48),  # Start
        timedelta(hours=0, minutes=1, seconds=18),  # Duration
        "Description",  # Description
    )


def test_format_timedelta():
    delta = timedelta(hours=0, minutes=8, seconds=48)
    assert format_timedelta(delta) == "08:48.000"


def test_format_line():
    assert (
        format_line("0848", "08:48.000", "01:18.000", "Description")
        == "0848	08:48.000	01:18.000	decimal	Subclip	Description"
    )


def test_cli_prints_table(capsys, monkeypatch: MonkeyPatch):
    user_inputs = ["tests/sample.docx", ""]
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))

    cli(
        lambda _filename: [
            "0000	Description	0100",
        ]
    )

    out, _ = capsys.readouterr()
    assert out == f"Roteiro Extractor - {VERSION}\n0000	Description	0100\n"


def test_cli_prints_table_accents(capsys, monkeypatch: MonkeyPatch):
    user_inputs = ["tests/sample_accents.docx", ""]
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))

    cli(
        lambda _filename: [
            "0000	Description	0100",
            "0130	Description with accents çáã	0200",
        ]
    )

    out, _ = capsys.readouterr()
    assert out == (
        f"Roteiro Extractor - {VERSION}\n"
        "0000	Description	0100\n"
        "0130	Description with accents çáã	0200\n"
    )
