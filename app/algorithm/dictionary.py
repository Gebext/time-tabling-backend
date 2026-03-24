import os

from collections import defaultdict

from typing import Any

import numpy as np

import pandas as pd

from app.core.logging import get_logger

logger = get_logger(__name__)

class DataDictionary:

    HARI_MAP = {

        "Senin": 1,

        "Selasa": 2,

        "Rabu": 3,

        "Kamis": 4,

        "Jumat": 5,

    }

    def __init__(self, data_dir: str) -> None:

        self._data_dir = data_dir

        self._load_all()

        logger.info("DataDictionary initialized from %s", data_dir)

    def _csv(self, name: str) -> pd.DataFrame:

        return pd.read_csv(os.path.join(self._data_dir, name))

    def _load_all(self) -> None:

        self.guru_df = self._csv("guru.csv")

        self.mapel_df = self._csv("mapel.csv")

        self.kelas_df = self._csv("kelas.csv")

        self.slot_df = self._csv("slot.csv")

        self.relasi_df = self._csv("relasi_guru_mapel.csv")

        self.wali_df = self._csv("wali_kelas.csv")

    def reload(self) -> None:

        self._load_all()

        logger.info("DataDictionary reloaded")

    @property

    def slot_per_hari(self) -> np.ndarray:

        counts = self.slot_df["hari"].value_counts().to_dict()

        mapped = {self.HARI_MAP[k]: v for k, v in counts.items()}

        return np.array([mapped[i] for i in range(1, 6)])

    @property

    def slot_hari(self) -> np.ndarray:

        return np.array([self.HARI_MAP[row.hari] for row in self.slot_df.itertuples()])

    @property

    def slot_per_kelas(self) -> int:

        return len(self.slot_hari)

    @property

    def slot_awal_hari(self) -> np.ndarray:

        return np.concatenate(([0], np.cumsum(self.slot_per_hari)[:-1]))

    @property

    def slot_akhir_hari(self) -> np.ndarray:

        return np.cumsum(self.slot_per_hari)

    @property

    def kelas_tingkatan(self) -> dict[int, int]:

        return dict(zip(self.kelas_df["kelas_id"], self.kelas_df["tingkatan"]))

    @property

    def kelas_ids(self) -> np.ndarray:

        return np.array(sorted(self.kelas_tingkatan.keys()))

    @property

    def jumlah_kelas(self) -> int:

        return len(self.kelas_ids)

    @property

    def total_slot(self) -> int:

        return self.jumlah_kelas * self.slot_per_kelas

    @property

    def jam_per_minggu_mapel(self) -> dict[int, int]:

        return dict(zip(self.mapel_df["mapel_id"], self.mapel_df["jam_per_minggu"]))

    @property

    def mapel_ids(self) -> np.ndarray:

        return np.array(list(self.jam_per_minggu_mapel.keys()))

    @property

    def jam_mapel(self) -> np.ndarray:

        return np.array(list(self.jam_per_minggu_mapel.values()))

    @property

    def mgmp_mapel(self) -> dict[int, int]:

        mgmp = dict(zip(self.mapel_df["mapel_id"], self.mapel_df["MGMP"]))

        return {mid: self.HARI_MAP[hari] for mid, hari in mgmp.items()}

    @property

    def guru_valid_mapel(self) -> dict[tuple[int, int], list[int]]:

        d: dict[tuple[int, int], list[int]] = defaultdict(list)

        for row in self.relasi_df.itertuples():

            d[(row.mapel_id, row.tingkatan)].append(row.guru_id)

        return dict(d)

    @property

    def max_jam_guru(self) -> dict[int, int]:

        return self.relasi_df.groupby("guru_id")["durasi"].sum().to_dict()

    @property

    def wali_kelas(self) -> dict[int, int]:

        return dict(zip(self.wali_df["guru_id"], self.wali_df["kelas_id"]))

    @property

    def batas_siang(self) -> np.ndarray:

        return np.array([5, 5, 4, 5, 4])

    @property

    def batas_mgmp(self) -> np.ndarray:

        return np.array([2, 2, 2, 2, 1])

    @property

    def relasi_guru_mapel(self) -> pd.DataFrame:

        return self.relasi_df

    @property

    def mapel_jam_per_minggu(self) -> dict[int, int]:

        return self.jam_per_minggu_mapel

    def fitness_weight(self) -> dict[str, int]:

        return {

            "guruBentrok": 100,

            "distribusiMapel": 20,

            "konsistensiGuruMapel": 20,

            "durasiGuru": 10,

            "waktuMGMP": 5,

            "mapelSiang": 5,

            "cekWaliKelas": 5,

        }

    @staticmethod

    def blok_distribusi(jam: int) -> list[int]:

        if jam == 2:

            return [2]

        if jam == 3:

            return [3]

        if jam == 4:

            return [2, 2]

        if jam == 5:

            return [2, 3]

        return [jam]

    @property

    def blok_mapel(self) -> dict[int, list[int]]:

        return {

            mid: self.blok_distribusi(jam)

            for mid, jam in self.jam_per_minggu_mapel.items()

        }
