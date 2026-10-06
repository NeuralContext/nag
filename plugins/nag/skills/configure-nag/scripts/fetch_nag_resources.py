#!/usr/bin/env python3
"""Fetch verified NAG bootstrap resources into an ephemeral staging directory."""

from __future__ import annotations

import hashlib
import shutil
import signal
import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

PINNED_COMMIT = "ba3bfe15408d523db5df467d72601493b294368e"
SOURCE_REPOSITORY = "https://github.com/NeuralContext/nag"
RAW_REPOSITORY = "https://raw.githubusercontent.com/NeuralContext/nag"
REQUIRED_RESOURCES = (
    ("AGENTS.md", "2c82fbaa129fbb4a486797e4971fd89fc0bc2497578093529627cb960a32b88e", "markdown"),
    (".agents/NAG-AGENTS.md", "35ed17b28541617cfc4d06815c0d9ca70cbceeb2fb3c3b1c1694f5bb56e5505a", "markdown"),
    (".agents/NAG-CONFIG.md", "c63c28a561946bf55d75574ba8c1df9c11d73c6c9bf86571e62aa9b62a6650cf", "markdown"),
)
CODEX_RESOURCES = (
    ("templates/.codex/config.toml", "210eab80c20e41b50bd1efcbd4ba96365ad460de5f8bd154bfbecb99aaf9da61", "toml"),
    ("templates/.codex/agents/implementer.toml", "bd8178a4d1168395f5ae966ce82ac667ccbb6120dc18ef2a50ac0030dc57f0b8", "toml"),
)


class FetchError(Exception):
    def __init__(self, exit_code: int, message: str) -> None:
        super().__init__(message)
        self.exit_code = exit_code


class NoRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        return None


def fail_if_invalid_arguments(arguments: list[str]) -> bool:
    if not arguments:
        return False
    if arguments == ["--include-codex"]:
        return True
    raise FetchError(2, "Usage: fetch_nag_resources.py [--include-codex]")


def validate_shape(content: bytes, resource_path: str, resource_kind: str) -> None:
    if not content:
        raise FetchError(4, f"Downloaded file is empty: {resource_path}")
    text = content.decode("utf-8", errors="replace")
    if resource_kind == "markdown" and not text.startswith("#"):
        raise FetchError(4, f"Downloaded Markdown has no heading: {resource_path}")
    if resource_kind == "toml" and not any(line.strip() and not line.lstrip().startswith("#") for line in text.splitlines()):
        raise FetchError(4, f"Downloaded TOML has no content: {resource_path}")


def download_resource(opener, staging_directory: Path, resource: tuple[str, str, str]) -> None:
    resource_path, expected_checksum, resource_kind = resource
    url = f"{RAW_REPOSITORY}/{PINNED_COMMIT}/{resource_path}"
    try:
        with opener.open(Request(url, headers={"User-Agent": "nag-configure-fetcher"}), timeout=30) as response:
            if response.status != 200:
                raise FetchError(3, f"Unexpected HTTP status {response.status} for {url}")
            content = response.read()
    except FetchError:
        raise
    except (HTTPError, URLError, OSError) as error:
        raise FetchError(3, f"Could not retrieve {url}: {error}") from error

    actual_checksum = hashlib.sha256(content).hexdigest()
    if actual_checksum != expected_checksum:
        raise FetchError(4, f"Checksum mismatch for {resource_path}")
    validate_shape(content, resource_path, resource_kind)
    destination = staging_directory / resource_path
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
    except OSError as error:
        raise FetchError(4, f"Could not stage validated resource {resource_path}: {error}") from error


def main(arguments: list[str]) -> int:
    if sys.version_info < (3, 8):
        raise FetchError(2, "Python 3.8 or newer is required")
    include_codex = fail_if_invalid_arguments(arguments)
    try:
        staging_directory = Path(tempfile.mkdtemp(prefix="nag-resources."))
    except OSError as error:
        raise FetchError(2, f"Could not create a staging directory: {error}") from error
    completed = False

    def interrupted(signum, frame) -> None:
        raise FetchError(3, "fetch_nag_resources.py interrupted")

    signal.signal(signal.SIGINT, interrupted)
    signal.signal(signal.SIGTERM, interrupted)
    try:
        resources = REQUIRED_RESOURCES + (CODEX_RESOURCES if include_codex else ())
        opener = build_opener(NoRedirectHandler())
        for resource in resources:
            download_resource(opener, staging_directory, resource)
        completed = True
        print(staging_directory)
        return 0
    finally:
        if not completed:
            shutil.rmtree(staging_directory, ignore_errors=True)


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except FetchError as error:
        print(error, file=sys.stderr)
        raise SystemExit(error.exit_code)
