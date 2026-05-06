import json
import os
import threading
from datetime import datetime
from typing import Any

import pandas as pd

from app.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

SCHEDULE_DIR = os.path.join(get_settings().DATA_DIR, "schedules")
SUMMARY_FILE = os.path.join(SCHEDULE_DIR, "_summary.csv")


class ScheduleRepository:

    def __init__(self) -> None:
        self._lock = threading.Lock()
        os.makedirs(SCHEDULE_DIR, exist_ok=True)
        if not os.path.exists(SUMMARY_FILE):
            pd.DataFrame(
                columns=[
                    "schedule_id",
                    "filename",
                    "fitness",
                    "total_conflicts",
                    "conflict_details",
                    "created_at",
                ]
            ).to_csv(SUMMARY_FILE, index=False)
        logger.info("ScheduleRepository ready at %s", SCHEDULE_DIR)

    def save(
        self,
        detail_per_kelas: list[dict[str, Any]],
        fitness: float,
        total_conflicts: int,
        conflict_details: dict[str, int] | None = None,
    ) -> dict[str, Any]:
        with self._lock:
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            filename = f"schedule_{timestamp}.csv"
            filepath = os.path.join(SCHEDULE_DIR, filename)

            rows: list[dict[str, Any]] = []
            for kelas_data in detail_per_kelas:
                kelas_id = kelas_data["kelas_id"]
                kelas_nama = kelas_data["kelas_nama"]
                for slot in kelas_data["jadwal"]:
                    rows.append(
                        {
                            "kelas_id": kelas_id,
                            "kelas_nama": kelas_nama,
                            "slot_id": slot["slot_id"],
                            "hari": slot["hari"],
                            "jam_mulai": slot["jam_mulai"],
                            "jam_selesai": slot["jam_selesai"],
                            "mapel_id": slot["mapel_id"],
                            "mapel_nama": slot["mapel_nama"],
                            "guru_id": slot["guru_id"],
                            "guru_nama": slot["guru_nama"],
                        }
                    )

            df = pd.DataFrame(rows)
            df.to_csv(filepath, index=False)

            summary_df = pd.read_csv(SUMMARY_FILE)
            schedule_id = 1 if summary_df.empty else int(summary_df["schedule_id"].max()) + 1
            new_entry = {
                "schedule_id": schedule_id,
                "filename": filename,
                "fitness": fitness,
                "total_conflicts": total_conflicts,
                "conflict_details": json.dumps({k: int(v) for k, v in conflict_details.items()}) if conflict_details else "{}",
                "created_at": now.isoformat(),
            }
            summary_df = pd.concat(
                [summary_df, pd.DataFrame([new_entry])], ignore_index=True
            )
            summary_df.to_csv(SUMMARY_FILE, index=False)

            logger.info("Schedule saved: %s (fitness=%.2f)", filename, fitness)
            return new_entry

    def get_all_summaries(self) -> list[dict[str, Any]]:
        with self._lock:
            if not os.path.exists(SUMMARY_FILE):
                return []
            df = pd.read_csv(SUMMARY_FILE)
            records = df.to_dict(orient="records")
            for rec in records:
                cd = rec.get("conflict_details")
                if isinstance(cd, str):
                    try:
                        rec["conflict_details"] = json.loads(cd)
                    except (json.JSONDecodeError, TypeError):
                        rec["conflict_details"] = {}
                elif not isinstance(cd, dict):
                    rec["conflict_details"] = {}
            return records

    def get_all_summaries_paginated(
        self,
        page: int = 1,
        per_page: int = 10,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> tuple[list[dict[str, Any]], int]:
        with self._lock:
            if not os.path.exists(SUMMARY_FILE):
                return [], 0
            df = pd.read_csv(SUMMARY_FILE)
            if start_date:
                start_dt = pd.to_datetime(start_date, errors="coerce")
                if pd.notna(start_dt):
                    created_at_series = pd.to_datetime(df["created_at"], errors="coerce")
                    df = df[created_at_series >= start_dt]
            if end_date:
                end_dt = pd.to_datetime(end_date, errors="coerce")
                if pd.notna(end_dt):
                    created_at_series = pd.to_datetime(df["created_at"], errors="coerce")
                    end_of_day = end_dt + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
                    df = df[created_at_series <= end_of_day]
            df = df.sort_values("created_at", ascending=False).reset_index(drop=True)
            total = len(df)
            start = (page - 1) * per_page
            end = start + per_page
            sliced = df.iloc[start:end]
            records = sliced.to_dict(orient="records")
            for rec in records:
                cd = rec.get("conflict_details")
                if isinstance(cd, str):
                    try:
                        rec["conflict_details"] = json.loads(cd)
                    except (json.JSONDecodeError, TypeError):
                        rec["conflict_details"] = {}
                elif not isinstance(cd, dict):
                    rec["conflict_details"] = {}
            return records, total

    def get_by_id(self, schedule_id: int) -> dict[str, Any]:
        with self._lock:
            summary_df = pd.read_csv(SUMMARY_FILE)
            mask = summary_df["schedule_id"] == schedule_id
            if not mask.any():
                raise FileNotFoundError(f"Schedule #{schedule_id} tidak ditemukan")
            entry = summary_df.loc[mask].iloc[0].to_dict()
            filepath = os.path.join(SCHEDULE_DIR, entry["filename"])
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"File {entry['filename']} tidak ditemukan")
            schedule_df = pd.read_csv(filepath)
            entry_dict = entry.to_dict() if hasattr(entry, 'to_dict') else dict(entry)
            cd = entry_dict.get("conflict_details")
            if isinstance(cd, str):
                try:
                    entry_dict["conflict_details"] = json.loads(cd)
                except (json.JSONDecodeError, TypeError):
                    entry_dict["conflict_details"] = {}
            elif not isinstance(cd, dict):
                entry_dict["conflict_details"] = {}
            return {
                "summary": entry_dict,
                "data": schedule_df.to_dict(orient="records"),
            }

    def get_csv_path(self, schedule_id: int) -> str:
        with self._lock:
            summary_df = pd.read_csv(SUMMARY_FILE)
            mask = summary_df["schedule_id"] == schedule_id
            if not mask.any():
                raise FileNotFoundError(f"Schedule #{schedule_id} tidak ditemukan")
            entry = summary_df.loc[mask].iloc[0].to_dict()
            filepath = os.path.join(SCHEDULE_DIR, entry["filename"])
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"File {entry['filename']} tidak ditemukan")
            return filepath

    def delete(self, schedule_id: int) -> None:
        with self._lock:
            summary_df = pd.read_csv(SUMMARY_FILE)
            mask = summary_df["schedule_id"] == schedule_id
            if not mask.any():
                raise FileNotFoundError(f"Schedule #{schedule_id} tidak ditemukan")
            entry = summary_df.loc[mask].iloc[0].to_dict()
            filepath = os.path.join(SCHEDULE_DIR, entry["filename"])
            if os.path.exists(filepath):
                os.remove(filepath)
            summary_df = summary_df[~mask].reset_index(drop=True)
            summary_df.to_csv(SUMMARY_FILE, index=False)
            logger.info("Schedule deleted: %s", entry["filename"])
