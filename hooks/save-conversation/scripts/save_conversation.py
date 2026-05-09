#!/usr/bin/env python3
"""
Save a Claude Code / Codex CLI conversation transcript (JSONL) as Markdown.

Usage:
  1) As a Claude Code Stop hook (reads JSON from stdin):
       python save_conversation.py --out-dir ./log

  2) Manual / Codex usage (explicit transcript path):
       python save_conversation.py --transcript <path.jsonl> --out-dir ./log

Output:
  <out-dir>/<session-start-timestamp>.md
  Each Stop event overwrites the same file with the full session so far,
  so one session == one md file, keyed by the session's first message time.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def _read_hook_stdin() -> dict:
    if sys.stdin.isatty():
        return {}
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return {}


def _iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def _extract_text(content) -> str:
    """Content may be a string, or a list of blocks with shapes like:
       {type:"text", text:"..."}, {type:"input_text", text:"..."},
       {type:"output_text", text:"..."}, {type:"tool_use", ...},
       {type:"tool_result", content:[...]}, etc.
    """
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
                continue
            if not isinstance(block, dict):
                continue
            btype = block.get("type", "")
            if btype in ("text", "input_text", "output_text") or "text" in block:
                parts.append(str(block.get("text", "")))
            elif btype == "tool_use":
                name = block.get("name", "tool")
                parts.append(f"\n<tool_use: {name}>")
            elif btype == "tool_result":
                inner = block.get("content", "")
                parts.append(f"\n<tool_result>\n{_extract_text(inner)}\n</tool_result>")
            elif btype == "thinking":
                # Skip internal thinking from the saved log.
                continue
        return "".join(parts).strip()
    if isinstance(content, dict):
        return _extract_text(content.get("content") or content.get("text") or "")
    return str(content)


def _normalize_entry(entry: dict):
    """Return (role, text, timestamp) or None if not a user/assistant message."""
    if not isinstance(entry, dict):
        return None

    # Claude Code format: {"type":"user"|"assistant","message":{"role":..,"content":..},"timestamp":..}
    # Codex format:       {"type":"message","role":..,"content":[..],"timestamp":..}
    role = entry.get("role")
    msg = entry.get("message")
    if not role and isinstance(msg, dict):
        role = msg.get("role")
    if not role:
        etype = entry.get("type")
        if etype in ("user", "assistant"):
            role = etype

    if role not in ("user", "assistant"):
        return None

    content = None
    if isinstance(msg, dict):
        content = msg.get("content")
    if content is None:
        content = entry.get("content")

    text = _extract_text(content)
    if not text:
        return None

    ts = entry.get("timestamp") or (msg.get("timestamp") if isinstance(msg, dict) else None)
    return role, text, ts


def _session_start_stamp(entries_iter) -> tuple[str, list]:
    entries = []
    first_ts = None
    for e in entries_iter:
        norm = _normalize_entry(e)
        if norm is None:
            continue
        entries.append(norm)
        if first_ts is None and norm[2]:
            first_ts = norm[2]

    if first_ts:
        try:
            dt = datetime.fromisoformat(first_ts.replace("Z", "+00:00")).astimezone()
        except ValueError:
            dt = datetime.now()
    else:
        dt = datetime.now()
    return dt.strftime("%Y%m%d_%H%M%S"), entries


def _render_markdown(entries: list, transcript_path: Path) -> str:
    lines = [
        f"# Conversation Log",
        "",
        f"- Source: `{transcript_path}`",
        f"- Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
    ]
    for role, text, ts in entries:
        header = "## 🧑 User" if role == "user" else "## 🤖 Assistant"
        if ts:
            header += f"  _({ts})_"
        lines.append(header)
        lines.append("")
        lines.append(text)
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript", type=str, default=None,
                        help="Path to JSONL transcript (Claude Code or Codex).")
    parser.add_argument("--out-dir", type=str, default="log",
                        help="Directory to write the Markdown file into.")
    args = parser.parse_args()

    transcript_path = None
    if args.transcript:
        transcript_path = Path(args.transcript).expanduser()
    else:
        hook = _read_hook_stdin()
        tp = hook.get("transcript_path")
        if tp:
            transcript_path = Path(tp).expanduser()

    if not transcript_path or not transcript_path.is_file():
        print(f"[save_conversation] transcript not found: {transcript_path}", file=sys.stderr)
        return 0  # Never block the hook pipeline.

    out_dir = Path(args.out_dir).expanduser()
    if not out_dir.is_absolute():
        out_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")) / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    stamp, entries = _session_start_stamp(_iter_jsonl(transcript_path))
    if not entries:
        print("[save_conversation] no user/assistant messages found", file=sys.stderr)
        return 0

    out_file = out_dir / f"{stamp}.md"
    out_file.write_text(_render_markdown(entries, transcript_path), encoding="utf-8")
    print(f"[save_conversation] wrote {out_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
