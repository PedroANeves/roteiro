import re
from datetime import timedelta
from os import path

import docx  # type: ignore

ROTEIRO_LINE = r"^(?P<start>\d{4})\t(?P<description>.*?)(?:\t(?P<end>\d{4}))?$"


def extract_lines(filename: str) -> list[str]:
    document = docx.Document(filename)
    lines = [paragraph.text for paragraph in document.paragraphs]
    return lines


def extract_timestamp(string: str) -> tuple[str, str, str | None]:
    m = re.match(ROTEIRO_LINE, string)
    if not m:
        raise ValueError()

    matches = m.groupdict()

    start: str = matches["start"]
    description: str = matches["description"]

    end: str | None = matches.get("end")

    return (start, description, end)


def format_timestamp(
    start: str, description: str, end: str
) -> tuple[str, timedelta, timedelta, str]:
    name = start

    start_minute = start[:2]
    start_seconds = start[2:]
    start_time = timedelta(
        hours=0, minutes=int(start_minute), seconds=int(start_seconds)
    )

    if end:
        end_minute = end[:2]
        end_seconds = end[2:]
        end_time = timedelta(
            hours=0, minutes=int(end_minute), seconds=int(end_seconds)
        )

        duration = end_time - start_time
    else:
        duration = timedelta(seconds=10)

    return (name, start_time, duration, description)


def format_timedelta(delta: timedelta) -> str:
    minute = (delta.seconds // 60) % 60
    second = delta.seconds % 60
    return f"{minute:02}:{second:02}.000"


def format_line(name: str, start: str, duration: str, description: str) -> str:
    sep = ","
    sep = "\t"
    return (
        f"{name}{sep}"
        f"{start}{sep}"
        f"{duration}{sep}"
        f"decimal{sep}"
        f"Subclip{sep}"
        f"{description}"
    )


def main():
    filename = input("filepath for .docx: ")
    filename = filename.strip()
    filename = filename.strip("'")
    if not path.isfile(filename):
        print(f"'{filename}' is not a file")
        return 1

    lines = extract_lines(filename)

    values = []
    for line in lines:
        try:
            timestamp = extract_timestamp(line)
        except ValueError:
            timestamp = None

        if timestamp:
            start, description, end = timestamp

            name, start_time, duration, description = format_timestamp(
                start, description, end
            )
            formated_line = format_line(
                name,
                format_timedelta(start_time),
                format_timedelta(duration),
                description,
            )
            values.append(formated_line)

    for i in values:
        print(i)

    return 0


if __name__ == "__main__":
    main()
