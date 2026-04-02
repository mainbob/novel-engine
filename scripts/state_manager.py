#!/usr/bin/env python3
"""
State manager — atomic read/write operations for state.json.
Provides CLI interface for agents to query and update state.
"""

import json
import sys
import shutil
from pathlib import Path
from datetime import datetime


def load_state(project_path: str) -> dict:
    """Load state.json with validation."""
    state_path = Path(project_path) / "state" / "state.json"
    if not state_path.exists():
        return {"error": f"state.json not found at {state_path}"}
    with open(state_path) as f:
        return json.load(f)


def save_state(project_path: str, state: dict) -> dict:
    """Atomic save — write to temp then rename."""
    state_dir = Path(project_path) / "state"
    state_path = state_dir / "state.json"
    backup_path = state_dir / f"state.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    tmp_path = state_dir / "state.json.tmp"

    # Backup current
    if state_path.exists():
        shutil.copy2(state_path, backup_path)

    # Write to temp
    with open(tmp_path, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    # Atomic rename
    tmp_path.rename(state_path)

    # Clean old backups (keep last 10)
    backups = sorted(state_dir.glob("state.backup.*.json"))
    for old in backups[:-10]:
        old.unlink()

    return {"status": "OK", "backup": str(backup_path)}


def query_character(project_path: str, name: str) -> dict:
    """Query character card by name."""
    cards_dir = Path(project_path) / "character-cards"
    for card_path in cards_dir.glob("*.json"):
        with open(card_path) as f:
            card = json.load(f)
        if card.get("name") == name or card.get("id") == name:
            return card
    return {"error": f"Character '{name}' not found"}


def query_hooks(project_path: str, status: str = None) -> list:
    """Query hooks, optionally filtered by status."""
    state = load_state(project_path)
    if "error" in state:
        return [state]
    hooks = state.get("hooks", [])
    if status:
        hooks = [h for h in hooks if h.get("status") == status]
    return hooks


def query_facts(project_path: str, chapter: int = None, known_by: str = None) -> list:
    """Query facts, optionally filtered by chapter or knowledge holder."""
    state = load_state(project_path)
    if "error" in state:
        return [state]
    facts = state.get("facts", [])
    if chapter:
        facts = [f for f in facts if f.get("established_chapter") == chapter]
    if known_by:
        facts = [f for f in facts if known_by in f.get("known_by", [])]
    return facts


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: state_manager.py <project_path> <command> [args...]")
        print("Commands: load, character <name>, hooks [status], facts [--chapter N] [--known-by id]")
        sys.exit(1)

    project = sys.argv[1]
    command = sys.argv[2]

    if command == "load":
        print(json.dumps(load_state(project), ensure_ascii=False, indent=2))
    elif command == "character" and len(sys.argv) > 3:
        print(json.dumps(query_character(project, sys.argv[3]), ensure_ascii=False, indent=2))
    elif command == "hooks":
        status = sys.argv[3] if len(sys.argv) > 3 else None
        print(json.dumps(query_hooks(project, status), ensure_ascii=False, indent=2))
    elif command == "facts":
        chapter = None
        known_by = None
        args = sys.argv[3:]
        for i, arg in enumerate(args):
            if arg == "--chapter" and i + 1 < len(args):
                chapter = int(args[i + 1])
            elif arg == "--known-by" and i + 1 < len(args):
                known_by = args[i + 1]
        print(json.dumps(query_facts(project, chapter, known_by), ensure_ascii=False, indent=2))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
