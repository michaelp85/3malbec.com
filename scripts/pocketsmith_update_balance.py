#!/usr/bin/env python3
"""
Fetch an account balance from PocketSmith and write it to a Hugo data file.
 
Security notes (see README.md for the full explanation):
- The PocketSmith developer key is read ONLY from the POCKETSMITH_KEY
  environment variable. It is never logged, printed, or written to disk.
- The script fails closed: any unexpected API shape or network error
  raises, rather than silently writing bad/zero data over a good value.
- The output file only ever contains the derived fields we choose to
  publish (amount, currency, as-of date) - never the raw API response,
  which may contain other account metadata you don't want committed.
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