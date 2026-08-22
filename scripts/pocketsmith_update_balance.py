#!/usr/bin/env python3
"""
Fetch an account balance from PocketSmith and write it to a Hugo data file.
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

# Where Hugo will read the data from: {{ .Site.Data.balance }}
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "pocketsmith_balance.json"


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

    # PocketSmith nests the live balance under the account's transaction
    # account(s). Adjust this extraction if your account has more than one
    # transaction_account and you want a specific one.
    tx_accounts = account.get("transaction_accounts") or []
    if not tx_accounts:
        raise RuntimeError(
            f"Account {account_id} has no transaction_accounts in the API response."
        )
    tx = tx_accounts[0]

    return {
        "amount": tx["current_balance"],
        "currency": tx["currency_code"],
        "as_of": tx.get("current_balance_date"),
    }


def write_if_changed(data: dict) -> bool:
    """Write the balance file only if the content actually changed.

    Keeps the git history (and any downstream deploy triggers) limited to
    real balance changes instead of a commit every time the workflow runs.
    """
    payload = {
        **data,
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    if OUTPUT_PATH.exists():
        existing = json.loads(OUTPUT_PATH.read_text())
        # Compare everything except the fetched_at timestamp.
        existing_comparable = {k: v for k, v in existing.items() if k != "fetched_at"}
        new_comparable = {k: v for k, v in payload.items() if k != "fetched_at"}
        if existing_comparable == new_comparable:
            return False

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n")
    return True


def main() -> None:
    key = get_developer_key()
    if not ACCOUNT_ID:
        sys.exit("POCKETSMITH_ACCOUNT_ID environment variable is not set.")

    balance = fetch_balance(key, ACCOUNT_ID)
    changed = write_if_changed(balance)

    # GITHUB_OUTPUT lets the workflow decide whether to commit, without
    # ever needing to print the balance itself to the Actions log.
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")


if __name__ == "__main__":
    main()