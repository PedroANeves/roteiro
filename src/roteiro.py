from __future__ import annotations

import re
import sys
import tkinter as tk
from datetime import timedelta
from os import path
from tkinter import filedialog
from typing import Callable

import docx  # type: ignore

from __version__ import VERSION

# DDDD<tab>Description[<tab>DDDD]
ROTEIRO_TIMESTAMP_FORMAT = (
    r"^(?P<start>\d{4})\t(?P<description>.*?)(?:\t(?P<end>\d{4}))?$"
)


def extract_lines(filename: str) -> list[str]:
    document = docx.Document(filename)
    lines = [paragraph.text for paragraph in document.paragraphs]
    return lines


def extract_timestamp_or_none(
    string: str,
) -> tuple[str, str, str | None] | None:
    m = re.match(ROTEIRO_TIMESTAMP_FORMAT, string)
    if not m:
        return None

    matches = m.groupdict()

    start: str = matches["start"]
    description: str = matches["description"]

    end: str | None = matches.get("end")

    return (start, description, end)


def format_timestamp(
    start: str, description: str, end: str | None
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
    sep = "\t"

    time_format = "decimal"
    range_export_format = "Subclip"
    return (
        f"{name}{sep}"
        f"{start}{sep}"
        f"{duration}{sep}"
        f"{time_format}{sep}"
        f"{range_export_format}{sep}"
        f"{description}"
    )


def get_markers(filename: str) -> list[str]:
    lines = extract_lines(filename)

    values = []
    for line in lines:
        timestamp = extract_timestamp_or_none(line)

        if timestamp is None:
            continue

        start, description, end = timestamp

        name, start_time, duration, description = format_timestamp(
            start, description, end
        )
        formatted_line = format_line(
            name,
            format_timedelta(start_time),
            format_timedelta(duration),
            description,
        )
        values.append(formatted_line)

    return values


TITLE = f"Roteiro Extractor - {VERSION}"


def cli(markers_strategy: Callable):
    print(TITLE)

    filename_raw = input("enter filepath for .docx: ")
    filename = filename_raw.strip().strip("'")

    if not path.isfile(filename):
        print(f"'{filename}' is not a file")
        return 1

    markers = markers_strategy(filename)

    for marker in markers:
        print(marker)

    return 0


def gui(markers_strategy: Callable):
    bg_color = "#2E2E2E"
    fg_color = "white"

    def _pick_file():
        filename = filedialog.askopenfilename(
            filetypes=(("docx", "*.docx"),),
        )

        if not filename:  # user hit 'cancel' or closed dialog
            return

        markers = markers_strategy(filename)

        file_contents = "\n".join(markers)
        text_display.delete(1.0, tk.END)
        text_display.insert(tk.END, file_contents)

    def _copy_all():
        all_text = text_display.get(1.0, tk.END)
        root.clipboard_clear()
        root.clipboard_append(all_text)
        root.update()

    def _save_tsv():
        f = filedialog.asksaveasfile(
            mode="w",
            defaultextension=".tsv",
            initialfile="Markers",
            filetypes=(("tsv", "*.tsv"),),
        )

        if not f:  # user hit 'cancel' or closed dialog
            return

        text2save = text_display.get(1.0, tk.END)
        f.write(text2save)
        f.close()

    root = tk.Tk()
    root.title(TITLE)
    root.config(bg=bg_color)

    # pick button
    pick_button = tk.Button(
        root,
        text="Pick the .docx",
        command=_pick_file,
        bg=bg_color,
        fg=fg_color,
    )
    pick_button.pack(pady=10)

    # marker display
    text_display = tk.Text(
        root,
        wrap=tk.WORD,
        bg=bg_color,
        fg=fg_color,
        insertbackground=fg_color,
    )
    text_display.pack(expand=True, fill=tk.BOTH)

    # copy button
    copy_button = tk.Button(
        root,
        text="Copy All",
        command=_copy_all,
        bg=bg_color,
        fg=fg_color,
    )
    copy_button.pack(pady=10)

    # save button
    save_button = tk.Button(
        root,
        text="Save .tsv",
        command=_save_tsv,
        bg=bg_color,
        fg=fg_color,
    )
    save_button.pack(pady=10)

    root.mainloop()

    return 0


def main():
    if "--cli" in sys.argv:
        ui = cli
    else:
        ui = gui

    ui(get_markers)


if __name__ == "__main__":
    main()
