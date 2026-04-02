#!/usr/bin/env python3
"""
Preflight check — validates project integrity before writing.
Called by /novel-write Step 0.
"""

import json
import sys
import os
from pathlib import Path


def check_project(project_path: str) -> dict:
    """Check project directory for required files and structure."""
    p = Path(project_path)
    issues = []
    warnings = []

    # Required files
    required = {
        "blueprint.json": p / "blueprint.json",
        "state.json": p / "state" / "state.json",
    }

    for name, path in required.items():
        if not path.exists():
            issues.append(f"Missing required file: {name}")

    # Required directories
    required_dirs = [
        "generated-rules",
        "character-cards",
        "outline",
        "chapters",
        "state",
        "summaries",
    ]

    for d in required_dirs:
        if not (p / d).is_dir():
            issues.append(f"Missing required directory: {d}/")

    # Check generated-rules has at least one file
    rules_dir = p / "generated-rules"
    if rules_dir.is_dir():
        rules = list(rules_dir.glob("*.md"))
        if not rules:
            issues.append("No rule documents found in generated-rules/")

    # Check blueprint validity
    bp_path = p / "blueprint.json"
    if bp_path.exists():
        try:
            with open(bp_path) as f:
                bp = json.load(f)
            if "narrative_structure" not in bp:
                issues.append("blueprint.json missing narrative_structure")
            if "required_rules" not in bp:
                issues.append("blueprint.json missing required_rules")
        except json.JSONDecodeError:
            issues.append("blueprint.json is not valid JSON")

    # Check state validity
    state_path = p / "state" / "state.json"
    if state_path.exists():
        try:
            with open(state_path) as f:
                state = json.load(f)
            if "project" not in state:
                issues.append("state.json missing project section")
        except json.JSONDecodeError:
            issues.append("state.json is not valid JSON")

    # Warnings (non-blocking)
    settings_dir = p / "settings"
    if not settings_dir.is_dir() or not list(settings_dir.glob("*.md")):
        warnings.append("No setting documents found in settings/ — writing without reference material")

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "warnings": warnings,
    }


def check_chapter(project_path: str, chapter: int) -> dict:
    """Check readiness for writing a specific chapter."""
    p = Path(project_path)
    issues = []

    # Check outline exists
    outline_path = p / "outline" / "chapters" / f"chapter-{chapter:03d}.md"
    if not outline_path.exists():
        # Try alternative naming
        outline_path = p / "outline" / "chapters" / f"chapter-{chapter}.md"
        if not outline_path.exists():
            issues.append(f"No outline found for chapter {chapter}")

    # Check previous chapter state is settled (if not first chapter)
    if chapter > 1:
        state_path = p / "state" / "state.json"
        if state_path.exists():
            with open(state_path) as f:
                state = json.load(f)
            current = state.get("project", {}).get("current_chapter", 0)
            if current < chapter - 1:
                issues.append(
                    f"State only settled through chapter {current}, "
                    f"but trying to write chapter {chapter}"
                )

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: preflight.py <project_path> [chapter_number]")
        sys.exit(1)

    project = sys.argv[1]
    result = check_project(project)

    if len(sys.argv) > 2:
        chapter = int(sys.argv[2])
        chapter_result = check_chapter(project, chapter)
        result["chapter_check"] = chapter_result
        if chapter_result["status"] == "FAIL":
            result["status"] = "FAIL"
            result["issues"].extend(chapter_result["issues"])

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1)
