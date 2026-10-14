"""Read requiredsoftwares.csv, ask the ADK agent for each row, write results CSV.

Usage:
    uv run python run_checker.py                       # defaults
    uv run python run_checker.py -i requiredsoftwares.csv -o latest_versions.csv
"""
import argparse
import asyncio
import csv
import json
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from software_cersion.agent import root_agent

APP_NAME = "software_version_checker"
USER_ID = "batch"

OUT_FIELDS = [
    "sno", "name", "current_version", "latest_version",
    "status", "release_date", "source_url", "notes",
]


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = {"sno", "name"} - set(reader.fieldnames or [])
        if missing:
            sys.exit(f"CSV is missing required column(s): {', '.join(sorted(missing))}")
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in reader
            if (row.get("name") or "").strip()
        ]


def extract_json(text: str) -> dict:
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    match = re.search(r"\{.*\}", text, flags=re.S)
    if not match:
        raise ValueError(f"No JSON in response: {text[:200]}")
    return json.loads(match.group(0))


async def check_one(runner: Runner, session_service, row: dict) -> dict:
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
    prompt = (
        f"name: {row['name']}\n"
        f"current_version: {row.get('version') or 'not provided'}\n"
        f"reference_url: {row.get('url') or 'not provided'}"
    )
    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    final_text = ""
    async for event in runner.run_async(
        user_id=USER_ID, session_id=session.id, new_message=message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_text = "".join(p.text or "" for p in event.content.parts)

    try:
        data = extract_json(final_text)
    except Exception as exc:  # keep the batch going
        data = {"latest_version": "ERROR", "notes": str(exc)[:200]}

    return {
        "sno": row["sno"],
        "name": row["name"],
        "current_version": row.get("version", ""),
        "latest_version": data.get("latest_version", ""),
        "status": data.get("status", "unknown"),
        "release_date": data.get("release_date", ""),
        "source_url": data.get("source_url", ""),
        "notes": data.get("notes", ""),
    }


async def main(inp: Path, out: Path) -> None:
    rows = read_rows(inp)
    session_service = InMemorySessionService()
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

    results = []
    for row in rows:
        print(f"[{row['sno']}] {row['name']} ...", flush=True)
        try:
            res = await check_one(runner, session_service, row)
        except Exception as exc:
            res = {k: "" for k in OUT_FIELDS}
            res.update(sno=row["sno"], name=row["name"],
                       latest_version="ERROR", notes=str(exc)[:200])
        print(f"    -> {res['latest_version']} ({res['status']})")
        results.append(res)

    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUT_FIELDS)
        writer.writeheader()
        writer.writerows(results)
    print(f"\nWrote {len(results)} rows to {out}")


if __name__ == "__main__":
    load_dotenv()
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default="requiredsoftwares.csv", type=Path)
    ap.add_argument("-o", "--output", default="latest_versions.csv", type=Path)
    args = ap.parse_args()
    asyncio.run(main(args.input, args.output))
