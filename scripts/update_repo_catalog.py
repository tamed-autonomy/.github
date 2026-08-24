#!/usr/bin/env python3
"""Render an organization repository catalog into a marked README region."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

START_MARKER = "<!-- REPOSITORY-CATALOG:START -->"
END_MARKER = "<!-- REPOSITORY-CATALOG:END -->"


def _is_visible(repository: dict[str, Any], audience: str) -> bool:
    if repository.get("isArchived"):
        return False
    if audience == "public":
        return repository.get("visibility", "").upper() == "PUBLIC"
    if audience == "member":
        return True
    raise ValueError(f"unknown audience: {audience}")


def _escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def validate_private_visibility(
    repositories: list[dict[str, Any]], expected_private_count: int
) -> None:
    """Reject a token-scoped inventory that cannot see every private repository."""
    actual = sum(
        repository.get("visibility", "").upper() == "PRIVATE"
        for repository in repositories
    )
    if actual != expected_private_count:
        raise ValueError(
            f"expected {expected_private_count} private repositories, found {actual}"
        )


def render_catalog(
    repositories: list[dict[str, Any]],
    config: dict[str, Any],
    audience: str,
) -> str:
    """Return a deterministic Markdown table for the selected audience."""
    overrides = config.get("repositories", {})
    excluded = set(config.get("exclude", []))
    visible = [
        repository
        for repository in repositories
        if repository["name"] not in excluded and _is_visible(repository, audience)
    ]
    visible.sort(
        key=lambda repository: (
            overrides.get(repository["name"], {}).get("order", 1000),
            repository["name"].casefold(),
        )
    )

    lines = [
        "| Repository | Role in the architecture | Current status |",
        "|---|---|---|",
    ]
    for repository in visible:
        override = overrides.get(repository["name"], {})
        role = override.get("role") or repository.get("description") or "Description pending."
        status = override.get("status") or (
            "Public repository."
            if repository.get("visibility", "").upper() == "PUBLIC"
            else "Private working repository."
        )
        name = _escape_cell(repository["name"])
        url = repository["url"]
        lines.append(
            f"| [`{name}`]({url}) | {_escape_cell(role)} | {_escape_cell(status)} |"
        )
    if len(lines) == 2:
        lines.append("| _No repositories currently match this view._ | | |")
    return "\n".join(lines)


def update_readme(path: Path, catalog: str) -> None:
    """Replace only the generated region and fail closed if markers are invalid."""
    content = path.read_text(encoding="utf-8")
    if content.count(START_MARKER) != 1 or content.count(END_MARKER) != 1:
        raise ValueError("README must contain exactly one pair of catalog markers")
    before, remainder = content.split(START_MARKER)
    _, after = remainder.split(END_MARKER)
    path.write_text(
        f"{before}{START_MARKER}\n{catalog}\n{END_MARKER}{after}",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--readme", required=True, type=Path)
    parser.add_argument("--audience", required=True, choices=("public", "member"))
    parser.add_argument("--expected-private-count", type=int)
    args = parser.parse_args()

    repositories = json.loads(args.input.read_text(encoding="utf-8"))
    config = json.loads(args.config.read_text(encoding="utf-8"))
    if args.expected_private_count is not None:
        validate_private_visibility(repositories, args.expected_private_count)
    update_readme(args.readme, render_catalog(repositories, config, args.audience))


if __name__ == "__main__":
    main()
