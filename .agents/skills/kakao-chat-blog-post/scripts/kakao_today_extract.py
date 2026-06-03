#!/usr/bin/env python3
"""Extract one day's messages from a KakaoTalk exported text file."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo


DATE_BANNER_RE = re.compile(
    r"^-+\s*(?P<year>\d{4})년\s*(?P<month>\d{1,2})월\s*(?P<day>\d{1,2})일.*?-+\s*$"
)
INLINE_RE = re.compile(
    r"^(?P<year>\d{4})[.\-/]\s*(?P<month>\d{1,2})[.\-/]\s*(?P<day>\d{1,2})[.\s,]+"
)
BRACKET_MESSAGE_RE = re.compile(
    r"^\[(?P<sender>[^\]]+)\]\s*\[(?:(?P<ampm>오전|오후)\s*)?(?P<hour>\d{1,2}):(?P<minute>\d{2})\]\s*(?P<body>.*)$"
)
INLINE_MESSAGE_RE = re.compile(
    r"^(?P<year>\d{4})[.\-/]\s*(?P<month>\d{1,2})[.\-/]\s*(?P<day>\d{1,2})[.\s,]+"
    r"(?:(?P<ampm>오전|오후)\s*)?(?P<hour>\d{1,2}):(?P<minute>\d{2}),?\s*"
    r"(?P<sender>[^:]+)\s*:\s*(?P<body>.*)$"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract target-date KakaoTalk messages and write a private Markdown source file."
    )
    parser.add_argument("export_file", type=Path, help="KakaoTalk exported .txt file")
    parser.add_argument(
        "--date",
        help="Target date in YYYY-MM-DD. Defaults to today in Asia/Seoul.",
    )
    parser.add_argument(
        "--chat-name",
        default="KakaoTalk",
        help="Chat room or counterpart name used in output headings.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("var/kakao-chat-blog-post"),
        help="Private output directory. This path is ignored by git.",
    )
    return parser.parse_args()


def target_date(value: str | None) -> dt.date:
    if value:
        return dt.date.fromisoformat(value)
    return dt.datetime.now(ZoneInfo("Asia/Seoul")).date()


def parse_banner_date(line: str) -> dt.date | None:
    match = DATE_BANNER_RE.match(line.strip())
    if not match:
        return None
    return dt.date(
        int(match.group("year")),
        int(match.group("month")),
        int(match.group("day")),
    )


def parse_inline_date(line: str) -> dt.date | None:
    match = INLINE_RE.match(line.strip())
    if not match:
        return None
    return dt.date(
        int(match.group("year")),
        int(match.group("month")),
        int(match.group("day")),
    )


def normalize_time(ampm: str | None, hour: str, minute: str) -> str:
    h = int(hour)
    if ampm == "오후" and h != 12:
        h += 12
    if ampm == "오전" and h == 12:
        h = 0
    return f"{h:02d}:{int(minute):02d}"


def extract_messages(text: str, selected_date: dt.date) -> list[str]:
    csv_messages = extract_csv_messages(text, selected_date)
    if csv_messages:
        return csv_messages

    messages: list[str] = []
    current_date: dt.date | None = None
    current_index: int | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue

        banner_date = parse_banner_date(line)
        if banner_date:
            current_date = banner_date
            current_index = None
            continue

        inline_message = INLINE_MESSAGE_RE.match(line)
        if inline_message:
            line_date = dt.date(
                int(inline_message.group("year")),
                int(inline_message.group("month")),
                int(inline_message.group("day")),
            )
            current_date = line_date
            current_index = None
            if line_date == selected_date:
                time = normalize_time(
                    inline_message.group("ampm"),
                    inline_message.group("hour"),
                    inline_message.group("minute"),
                )
                messages.append(
                    f"- {time} {inline_message.group('sender').strip()}: {inline_message.group('body').strip()}"
                )
                current_index = len(messages) - 1
            continue

        inline_date = parse_inline_date(line)
        if inline_date:
            current_date = inline_date
            current_index = None
            continue

        bracket_message = BRACKET_MESSAGE_RE.match(line)
        if bracket_message:
            current_index = None
            if current_date == selected_date:
                time = normalize_time(
                    bracket_message.group("ampm"),
                    bracket_message.group("hour"),
                    bracket_message.group("minute"),
                )
                messages.append(
                    f"- {time} {bracket_message.group('sender').strip()}: {bracket_message.group('body').strip()}"
                )
                current_index = len(messages) - 1
            continue

        if current_date == selected_date and current_index is not None:
            messages[current_index] += f"\n  {line.strip()}"

    return messages


def extract_csv_messages(text: str, selected_date: dt.date) -> list[str]:
    sample = text.lstrip("\ufeff")
    if not sample.startswith("Date,User,Message"):
        return []

    messages: list[str] = []
    reader = csv.DictReader(sample.splitlines())
    for row in reader:
        raw_date = (row.get("Date") or "").strip()
        sender = (row.get("User") or "").strip()
        body = (row.get("Message") or "").strip()
        if not raw_date or not sender:
            continue
        try:
            timestamp = dt.datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
        if timestamp.date() != selected_date:
            continue
        messages.append(f"- {timestamp:%H:%M} {sender}: {body}")
    return messages


def write_output(out_dir: Path, chat_name: str, selected_date: dt.date, messages: list[str]) -> Path:
    safe_chat_name = re.sub(r"[^0-9A-Za-z가-힣._-]+", "-", chat_name).strip("-") or "kakao"
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / f"{selected_date.isoformat()}-{safe_chat_name}-today.md"
    body = "\n".join(messages) if messages else "_당일 대화가 추출되지 않았습니다._"
    output_path.write_text(
        "\n".join(
            [
                f"# {chat_name} {selected_date.isoformat()} 대화 추출",
                "",
                f"- chat: {chat_name}",
                f"- date: {selected_date.isoformat()}",
                f"- message_count: {len(messages)}",
                "",
                "## Messages",
                "",
                body,
                "",
            ]
        ),
        encoding="utf-8",
    )
    return output_path


def main() -> int:
    args = parse_args()
    selected_date = target_date(args.date)
    if not args.export_file.exists():
        print(f"Export file not found: {args.export_file}", file=sys.stderr)
        return 2

    text = args.export_file.read_text(encoding="utf-8-sig", errors="replace")
    messages = extract_messages(text, selected_date)
    output_path = write_output(args.out_dir, args.chat_name, selected_date, messages)
    print(output_path)
    print(f"message_count={len(messages)}")
    return 0 if messages else 1


if __name__ == "__main__":
    raise SystemExit(main())
