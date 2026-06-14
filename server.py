#!/usr/bin/env python3
"""Life Palantir local server.

The first scaffold intentionally uses Python stdlib + SQLite so the platform can
run on a clean machine without package installation.
"""

from __future__ import annotations

import json
import mimetypes
import os
import sqlite3
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("LIFEPALANTIR_DB_PATH", ROOT / "data" / "lifepalantir.sqlite3"))
DEFAULT_PORT = int(os.environ.get("PORT", "8020"))


SUBSYSTEMS = [
    {
        "id": "lifetoolsystem",
        "name": "LifeToolSystem",
        "repo_url": "https://github.com/qi9zg202-source/LifeToolSystem",
        "domain": "Equipment and Service Intelligence",
        "mission": "Manage high-quality life equipment, products, services, hospitals, clothing, shoes, and verified efficiency upgrades.",
        "status": "active",
        "priority": 1,
        "owner": "Summer",
    },
    {
        "id": "tomeofsouls",
        "name": "TomeofSouls",
        "repo_url": "https://github.com/qi9zg202-source/TomeofSouls",
        "domain": "Personal Ontology",
        "mission": "Maintain body attributes, identity, goals, beliefs, context, and AI-agent memory for the person behind the system.",
        "status": "active",
        "priority": 2,
        "owner": "Summer",
    },
    {
        "id": "whattoeat",
        "name": "Whattoeat",
        "repo_url": "https://github.com/qi9zg202-source/Whattoeat",
        "domain": "Food Execution",
        "mission": "Manage daily meals, food choices, meal count, portion size, cooking method, and metabolic execution.",
        "status": "active",
        "priority": 3,
        "owner": "Summer",
    },
    {
        "id": "vancouver",
        "name": "Vancouver",
        "repo_url": "https://github.com/qi9zg202-source/Vancouver",
        "domain": "Migration Operating System",
        "mission": "Manage the long-term Vancouver immigration path, documents, capability building, city research, and settlement readiness.",
        "status": "active",
        "priority": 4,
        "owner": "Summer",
    },
]


ONTOLOGY_OBJECTS = [
    ("lifetoolsystem", "asset_class", "Tesla", "Vehicle and mobility system requiring ownership, maintenance, charging, and cost intelligence.", "candidate", 0.72, "user-brief"),
    ("lifetoolsystem", "asset_class", "Verified apparel", "Sunscreen clothing, socks, underwear, shoes, and other high-quality daily wear that improves comfort and efficiency.", "active", 0.82, "user-brief"),
    ("lifetoolsystem", "service_class", "Hospital network", "Hospitals and clinical services selected by authority, quality, access path, and practical outcome.", "active", 0.78, "user-brief"),
    ("tomeofsouls", "person", "Summer", "The primary human object: identity, body, goals, values, context, constraints, and agent-facing memory.", "active", 0.94, "user-brief"),
    ("tomeofsouls", "goal", "AI Agent architecture mastery", "Long-term professional transition toward AI Agent architecture and development.", "active", 0.86, "memory"),
    ("tomeofsouls", "goal", "Vancouver migration gateway", "Long-horizon migration target and readiness program.", "active", 0.88, "memory"),
    ("whattoeat", "execution_loop", "Daily meal plan", "Meal count, food type, cooking method, quantity, timing, and result tracking.", "active", 0.84, "user-brief"),
    ("whattoeat", "signal", "Metabolic response", "Energy, hunger, sleep, output, body metrics, and adherence signals after meals.", "candidate", 0.70, "memory"),
    ("vancouver", "program", "Immigration roadmap", "Documents, language, work, finance, city research, and settlement milestones.", "active", 0.88, "user-brief"),
    ("vancouver", "milestone", "IELTS 8888", "Language capability milestone for migration readiness.", "active", 0.80, "memory"),
]


INITIAL_DECISIONS = [
    {
        "title": "Set lifepalantir as the master project",
        "subsystem_id": "lifetoolsystem",
        "decision_type": "architecture",
        "rationale": "The user-facing system should coordinate all life-management subsystems from one operational control plane.",
        "status": "accepted",
        "confidence": 0.93,
        "impact": "high",
        "next_action": "Build master subsystem registry and ontology-first dashboard.",
    },
    {
        "title": "Use local SQLite for phase-one operational memory",
        "subsystem_id": "tomeofsouls",
        "decision_type": "data",
        "rationale": "Local SQLite keeps the first scaffold inspectable, portable, and easy to verify before cloud sync is needed.",
        "status": "accepted",
        "confidence": 0.82,
        "impact": "medium",
        "next_action": "Document schema and add import/sync adapters later.",
    },
]


def utc_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with db() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS subsystems (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                repo_url TEXT NOT NULL,
                domain TEXT NOT NULL,
                mission TEXT NOT NULL,
                status TEXT NOT NULL,
                priority INTEGER NOT NULL,
                owner TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS ontology_objects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subsystem_id TEXT NOT NULL REFERENCES subsystems(id),
                object_type TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                state TEXT NOT NULL,
                confidence REAL NOT NULL,
                source_ref TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subsystem_id TEXT NOT NULL REFERENCES subsystems(id),
                object_id INTEGER REFERENCES ontology_objects(id),
                signal_type TEXT NOT NULL,
                name TEXT NOT NULL,
                value TEXT NOT NULL,
                unit TEXT NOT NULL DEFAULT '',
                recorded_at TEXT NOT NULL,
                source_ref TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                subsystem_id TEXT NOT NULL REFERENCES subsystems(id),
                decision_type TEXT NOT NULL,
                rationale TEXT NOT NULL,
                status TEXT NOT NULL,
                confidence REAL NOT NULL,
                impact TEXT NOT NULL,
                next_action TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS action_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                decision_id INTEGER REFERENCES decisions(id),
                subsystem_id TEXT NOT NULL REFERENCES subsystems(id),
                title TEXT NOT NULL,
                owner TEXT NOT NULL,
                status TEXT NOT NULL,
                due_date TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS integrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subsystem_id TEXT NOT NULL REFERENCES subsystems(id),
                name TEXT NOT NULL,
                kind TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                status TEXT NOT NULL,
                last_checked_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                actor TEXT NOT NULL,
                event_type TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                entity_id TEXT NOT NULL,
                summary TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )

        timestamp = utc_now()
        if conn.execute("SELECT COUNT(*) FROM subsystems").fetchone()[0] == 0:
            conn.executemany(
                """
                INSERT INTO subsystems (
                    id, name, repo_url, domain, mission, status, priority,
                    owner, created_at, updated_at
                ) VALUES (
                    :id, :name, :repo_url, :domain, :mission, :status, :priority,
                    :owner, :created_at, :updated_at
                )
                """,
                [{**item, "created_at": timestamp, "updated_at": timestamp} for item in SUBSYSTEMS],
            )

        if conn.execute("SELECT COUNT(*) FROM ontology_objects").fetchone()[0] == 0:
            conn.executemany(
                """
                INSERT INTO ontology_objects (
                    subsystem_id, object_type, name, description, state, confidence,
                    source_ref, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [(*item, timestamp, timestamp) for item in ONTOLOGY_OBJECTS],
            )

        if conn.execute("SELECT COUNT(*) FROM decisions").fetchone()[0] == 0:
            conn.executemany(
                """
                INSERT INTO decisions (
                    title, subsystem_id, decision_type, rationale, status,
                    confidence, impact, next_action, created_at, updated_at
                ) VALUES (
                    :title, :subsystem_id, :decision_type, :rationale, :status,
                    :confidence, :impact, :next_action, :created_at, :updated_at
                )
                """,
                [{**item, "created_at": timestamp, "updated_at": timestamp} for item in INITIAL_DECISIONS],
            )

        if conn.execute("SELECT COUNT(*) FROM action_items").fetchone()[0] == 0:
            conn.execute(
                """
                INSERT INTO action_items (
                    decision_id, subsystem_id, title, owner, status, due_date,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    1,
                    "lifetoolsystem",
                    "Inventory existing subsystem repositories and map them to ontology objects.",
                    "Summer",
                    "open",
                    "",
                    timestamp,
                    timestamp,
                ),
            )

        if conn.execute("SELECT COUNT(*) FROM integrations").fetchone()[0] == 0:
            conn.executemany(
                """
                INSERT INTO integrations (
                    subsystem_id, name, kind, endpoint, status, last_checked_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                [(item["id"], item["name"], "github_repo", item["repo_url"], "registered", timestamp) for item in SUBSYSTEMS],
            )


def clean_text(value: Any, max_len: int = 1000) -> str:
    return str(value or "").strip()[:max_len]


def clamp_float(value: Any, fallback: float, low: float, high: float) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        parsed = fallback
    return min(max(parsed, low), high)


def rows(query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with db() as conn:
        return [dict(row) for row in conn.execute(query, params).fetchall()]


def one(query: str, params: tuple[Any, ...] = ()) -> dict[str, Any]:
    with db() as conn:
        row = conn.execute(query, params).fetchone()
        return dict(row) if row else {}


def bootstrap() -> dict[str, Any]:
    subsystems = rows("SELECT * FROM subsystems ORDER BY priority, name")
    objects = rows("SELECT * FROM ontology_objects ORDER BY subsystem_id, object_type, name")
    decisions = rows("SELECT * FROM decisions ORDER BY created_at DESC, id DESC")
    actions = rows("SELECT * FROM action_items ORDER BY status, id")
    integrations = rows("SELECT * FROM integrations ORDER BY subsystem_id, id")

    return {
        "platform": {
            "name": "Life Palantir",
            "mission": "Master operating layer for Summer's life-management subsystems.",
            "database": str(DB_PATH),
            "updated_at": utc_now(),
        },
        "metrics": {
            "subsystems": len(subsystems),
            "ontology_objects": len(objects),
            "decisions": len(decisions),
            "open_actions": sum(1 for item in actions if item["status"] != "done"),
            "integrations": len(integrations),
        },
        "subsystems": subsystems,
        "ontology_objects": objects,
        "decisions": decisions,
        "action_items": actions,
        "integrations": integrations,
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "LifePalantir/0.1"

    def do_GET(self) -> None:
        init_db()
        path = urlparse(self.path).path
        if path == "/api/health":
            self.send_json({"ok": True, "service": "lifepalantir", "database": str(DB_PATH)})
            return
        if path == "/api/bootstrap":
            self.send_json(bootstrap())
            return
        self.serve_static(path)

    def do_POST(self) -> None:
        init_db()
        path = urlparse(self.path).path
        payload = self.read_json()
        if path == "/api/decisions":
            self.create_decision(payload)
            return
        if path == "/api/actions":
            self.create_action(payload)
            return
        self.send_error_json(HTTPStatus.NOT_FOUND, "Unknown API route.")

    def create_decision(self, payload: dict[str, Any]) -> None:
        title = clean_text(payload.get("title"), 180)
        subsystem_id = clean_text(payload.get("subsystem_id"), 80)
        rationale = clean_text(payload.get("rationale"), 1500)
        if not title or not subsystem_id or not rationale:
            self.send_error_json(HTTPStatus.BAD_REQUEST, "title, subsystem_id, and rationale are required.")
            return

        timestamp = utc_now()
        with db() as conn:
            conn.execute(
                """
                INSERT INTO decisions (
                    title, subsystem_id, decision_type, rationale, status,
                    confidence, impact, next_action, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    title,
                    subsystem_id,
                    clean_text(payload.get("decision_type"), 80) or "manual",
                    rationale,
                    clean_text(payload.get("status"), 40) or "review",
                    clamp_float(payload.get("confidence"), 0.7, 0, 1),
                    clean_text(payload.get("impact"), 40) or "medium",
                    clean_text(payload.get("next_action"), 500),
                    timestamp,
                    timestamp,
                ),
            )
            decision_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            conn.execute(
                """
                INSERT INTO audit_events (
                    actor, event_type, entity_type, entity_id, summary, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                ("user", "create", "decision", str(decision_id), f"Created decision: {title}", timestamp),
            )
        self.send_json(bootstrap(), HTTPStatus.CREATED)

    def create_action(self, payload: dict[str, Any]) -> None:
        title = clean_text(payload.get("title"), 220)
        subsystem_id = clean_text(payload.get("subsystem_id"), 80)
        if not title or not subsystem_id:
            self.send_error_json(HTTPStatus.BAD_REQUEST, "title and subsystem_id are required.")
            return

        timestamp = utc_now()
        with db() as conn:
            conn.execute(
                """
                INSERT INTO action_items (
                    decision_id, subsystem_id, title, owner, status, due_date,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload.get("decision_id") or None,
                    subsystem_id,
                    title,
                    clean_text(payload.get("owner"), 80) or "Summer",
                    clean_text(payload.get("status"), 40) or "open",
                    clean_text(payload.get("due_date"), 40),
                    timestamp,
                    timestamp,
                ),
            )
        self.send_json(bootstrap(), HTTPStatus.CREATED)

    def serve_static(self, raw_path: str) -> None:
        path = "/index.html" if raw_path in {"", "/"} else raw_path
        rel = Path(unquote(path.lstrip("/")))
        candidate = (ROOT / rel).resolve()
        if ROOT not in candidate.parents and candidate != ROOT:
            self.send_error_json(HTTPStatus.FORBIDDEN, "Forbidden.")
            return
        if not candidate.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        body = candidate.read_bytes()
        content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def send_json(self, payload: dict[str, Any], status_code: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, status_code: HTTPStatus, message: str) -> None:
        self.send_json({"error": message}, status_code)

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[{self.log_date_time_string()}] {fmt % args}")


def main() -> None:
    init_db()
    server = ThreadingHTTPServer(("127.0.0.1", DEFAULT_PORT), Handler)
    print(f"Life Palantir: http://127.0.0.1:{DEFAULT_PORT}")
    print(f"SQLite database: {DB_PATH}")
    server.serve_forever()


if __name__ == "__main__":
    main()
