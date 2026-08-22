#!/usr/bin/env python3
"""
Fetch an account balance from PocketSmith and append it to a Hugo data file
as a growing daily history, so it can be charted over time.

Data model: data/balance_history.json is a JSON array, one entry per
calendar day (UTC) the workflow has run, e.g.:

    [
      {"date": "2026-08-24", "amount": 1234.56, "currency": "AUD",
       "as_of": "2026-08-23", "fetched_at": "2026-08-24T07:15:03Z"},
      {"date": "2026-08-25", "amount": 1198.02, "currency": "AUD",
       "as_of": "2026-08-25", "fetched_at": "2026-08-25T07:15:04Z"}
    ]

"date" is the day this workflow ran (its dedup key - re-running the
workflow twice in one day overwrites that day's entry rather than adding
a duplicate point). "as_of" is PocketSmith's own current_balance_date,
kept alongside so you can tell if the underlying bank feed was stale that
day. Old entries are never rewritten or deleted automatically - the file
only grows, which is what a "chart this over time" history needs.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

API_BASE = "https://api.pocketsmith.com/v2"

# The PocketSmith *account id* (not name) whose balance you want to publish.
# Find it by calling GET /users/{id}/accounts once manually and reading the
# "id" field of the account you care about - see README.md.
ACCOUNT_ID = os.environ.get("POCKETSMITH_ACCOUNT_ID")

# Where Hugo will read the data from: {{ hugo.Data.balance_history }}
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "pocketsmith_balance_history.json"


def get_developer_key() -> str:
    key = os.environ.get("POCKETSMITH_KEY")
    if not key:
        sys.exit("POCKETSMITH_KEY environment variable is not set.")
    return key


def api_get(path: str, key: str) -> dict:
    resp = requests.get(
        f"{API_BASE}{path}",
        headers={
            "X-Developer-Key": key,
            "Accept": "application/json",
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def fetch_balance(key: str, account_id: str) -> dict:
    account = api_get(f"/accounts/{account_id}", key)

    # The Account object exposes its own current_balance / currency_code /
    # current_balance_date directly - use those rather than reaching into
    # account["transaction_accounts"][0]. An account can "compose" more
    # than one transaction account (PocketSmith's own term), and there's
    # no guarantee the first entry in that list is the one you want. The
    # top-level fields are correct regardless of how many transaction
    # accounts make up this particular account.
    if "current_balance" not in account:
        raise RuntimeError(
            f"Account {account_id} response has no current_balance field: {account!r}"
        )

    return {
        "amount": account["current_balance"],
        "currency": account["currency_code"],
        "as_of": account.get("current_balance_date"),
    }


def load_history() -> list:
    """Load the existing history array, tolerating a missing, empty, or
    corrupted file rather than crashing (e.g. a placeholder committed with
    no content, or a hand-edited file with a typo)."""
    if not OUTPUT_PATH.exists():
        return []

    text = OUTPUT_PATH.read_text().strip()
    if not text:
        return []

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []

    if not isinstance(data, list):
        # Old single-object balance.json format, or something unexpected -
        # don't try to merge into it, just start a fresh history.
        return []

    return data


def append_or_update(history: list, balance: dict) -> tuple[list, bool]:
    """Add today's entry, overwriting an existing entry for today if the
    workflow has already run once today (e.g. a manual re-run), rather than
    appending a duplicate point for the same day."""
    now = datetime.now(timezone.utc)
    entry = {
        "date": now.strftime("%Y-%m-%d"),
        "amount": balance["amount"],
        "currency": balance["currency"],
        "as_of": balance.get("as_of"),
        "fetched_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    for i, existing in enumerate(history):
        if existing.get("date") == entry["date"]:
            comparable_existing = {k: v for k, v in existing.items() if k != "fetched_at"}
            comparable_new = {k: v for k, v in entry.items() if k != "fetched_at"}
            if comparable_existing == comparable_new:
                return history, False
            history[i] = entry
            return history, True

    history.append(entry)
    return history, True


def write_history(history: list) -> None:
    history.sort(key=lambda e: e["date"])
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(history, indent=2) + "\n")


def main() -> None:
    key = get_developer_key()
    if not ACCOUNT_ID:
        sys.exit("POCKETSMITH_ACCOUNT_ID environment variable is not set.")

    balance = fetch_balance(key, ACCOUNT_ID)
    history = load_history()
    history, changed = append_or_update(history, balance)

    if changed:
        write_history(history)

    # GITHUB_OUTPUT lets the workflow decide whether to commit, without
    # ever needing to print the balance itself to the Actions log.
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")


if __name__ == "__main__":
    main()