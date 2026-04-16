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
                    "created_at",
                ]
            ).to_csv(SUMMARY_FILE, index=False)
        logger.info("ScheduleRepository ready at %s", SCHEDULE_DIR)

    def save(
        self,
        detail_per_kelas: list[dict[str, Any]],
        fitness: float,
        total_conflicts: int,
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
            return df.to_dict(orient="records")

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
            return {
                "summary": entry,
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
