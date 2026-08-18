#!/usr/bin/env python3
"""Pull a snapshot from NX Witness, push it to Bunny Storage, purge the CDN."""

from __future__ import annotations

import logging
import os
import sys

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

NX_BASE    = os.environ.get("NX_BASE")
NX_USER    = os.environ["NX_USER"]
NX_PASS    = os.environ["NX_PASS"]
DEVICE_ID  = os.environ["NX_DEVICE_ID"] # Make sure to keep the braces
IMAGE_SIZE = os.environ.get("IMAGE_SIZE", "1440x804")
NX_VERIFY = os.environ.get("NX_VERIFY", "true").lower() not in ("false", "0", "no")
if not NX_VERIFY:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

STORAGE_HOST = os.environ.get("BUNNY_STORAGE_HOST", "syd.storage.bunnycdn.com")
STORAGE_ZONE = os.environ.get("BUNNY_ZONE", "3malbec-storage")
STORAGE_PATH = os.environ.get("BUNNY_PATH", "latest.jpg")
STORAGE_KEY  = os.environ["BUNNY_STORAGE_KEY"]
BUNNY_API_KEY = os.environ["BUNNY_API_KEY"]
PURGE_URL    = os.environ.get("PURGE_URL", "https://3malbec.b-cdn.net/latest.jpg")

TIMEOUT   = 30
MIN_BYTES = 10_000

def build_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET", "PUT", "POST"),
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session

def get_token(session: requests.Session) -> str:
    resp = session.post(
        f"{NX_BASE}/rest/v4/login/sessions",
        json={"username": NX_USER, "password": NX_PASS, "setCookie": False},
        timeout=TIMEOUT,
        verify=NX_VERIFY,
    )
    resp.raise_for_status()
    return resp.json()["token"]

def fetch_image(session: requests.Session, token: str) -> bytes:
    resp = session.get(
        f"{NX_BASE}/rest/v3/devices/{DEVICE_ID}/image",
        params={"size": IMAGE_SIZE},
        headers={"Authorization": f"Bearer {token}"},
        timeout=TIMEOUT,
        verify=NX_VERIFY,
    )
    resp.raise_for_status()

    ctype = resp.headers.get("Content-Type", "")
    if not ctype.startswith("image/"):
        raise RuntimeError(f"expected an image, got {ctype!r}")
    if len(resp.content) < MIN_BYTES:
        raise RuntimeError(f"image only {len(resp.content)} bytes, refusing to publish")

    return resp.content

def upload(session: requests.Session, data: bytes) -> None:
    resp = session.put(
        f"https://{STORAGE_HOST}/{STORAGE_ZONE}/{STORAGE_PATH}",
        data=data,
        headers={"AccessKey": STORAGE_KEY, "Content-Type": "image/jpeg"},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()

def purge(session: requests.Session) -> None:
    resp = session.post(
        "https://api.bunny.net/purge",
        params={"url": PURGE_URL, "async": "false"},
        headers={"AccessKey": BUNNY_API_KEY},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()

def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        session = build_session()
        data = fetch_image(session, get_token(session))
        logging.info("fetched %d bytes", len(data))
        upload(session, data)
        purge(session)
        logging.info("published")
        return 0
    except Exception:
        logging.exception("run failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())