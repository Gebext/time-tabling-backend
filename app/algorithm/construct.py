"""
Population constructor for the GA-GWO scheduling algorithm.

Refactored from the original production/construct/construct.py.
"""

import random

import numpy as np

from app.algorithm.dictionary import DataDictionary
from app.core.logging import get_logger

logger = get_logger(__name__)


class PopulationConstructor:
    """Constructs initial population of timetable individuals."""

    def __init__(self, data_dict: DataDictionary) -> None:
        self._d = data_dict

    def _generate_per_kelas(self, tingkatan: int) -> tuple[np.ndarray, np.ndarray]:
        """Generate a random timetable for a single class of a given grade level."""
        blok_list: list[tuple[int, int, int]] = []

        for mapel_id, jam in self._d.jam_per_minggu_mapel.items():
            guru_valid = self._d.guru_valid_mapel.get((mapel_id, tingkatan))
            if not guru_valid:
                continue
            guru = random.choice(guru_valid)
            bloks = self._d.blok_mapel[mapel_id]
            for b in bloks:
                blok_list.append((mapel_id, guru, b))

        random.shuffle(blok_list)

        mapel_arr: list[int] = []
        guru_arr: list[int] = []

        for mapel_id, guru, panjang in blok_list:
            mapel_arr.extend([mapel_id] * panjang)
            guru_arr.extend([guru] * panjang)

        mapel_np = np.array(mapel_arr, dtype=np.int16)
        guru_np = np.array(guru_arr, dtype=np.int16)

        max_slot = self._d.slot_per_kelas

        # Trim if too long
        if len(mapel_np) > max_slot:
            mapel_np = mapel_np[:max_slot]
            guru_np = guru_np[:max_slot]

        # Pad if too short
        while len(mapel_np) < max_slot:
            mapel = random.choice(self._d.mapel_ids)
            guru_valid = self._d.guru_valid_mapel.get((mapel, tingkatan))
            if guru_valid:
                guru = random.choice(guru_valid)
                mapel_np = np.append(mapel_np, mapel)
                guru_np = np.append(guru_np, guru)

        return mapel_np, guru_np

    def _individu_construct(self) -> tuple[np.ndarray, np.ndarray]:
        """Generate one complete timetable individual (all classes)."""
        n_kelas = self._d.jumlah_kelas
        slot_kelas = self._d.slot_per_kelas

        mapel_matrix = np.zeros((n_kelas, slot_kelas), dtype=np.int16)
        guru_matrix = np.zeros((n_kelas, slot_kelas), dtype=np.int16)

        kelas_ids = self._d.kelas_ids
        kelas_tingkatan = self._d.kelas_tingkatan

        for i, kelas_id in enumerate(kelas_ids):
            tingkatan = kelas_tingkatan[kelas_id]
            mapel_row, guru_row = self._generate_per_kelas(tingkatan)
            mapel_matrix[i] = mapel_row
            guru_matrix[i] = guru_row

        return mapel_matrix, guru_matrix

    def generate_individual(self) -> list[list]:
        """
        Generate a single individual for GA.

        Returns individual as list of kelas:
        [
            [hari_0, hari_1, ..., hari_4, guru_mapel_list],  # kelas 1
            [hari_0, hari_1, ..., hari_4, guru_mapel_list],  # kelas 2
            ...
        ]

        Where:
        - hari_i = list of mapel_ids for day i
        - guru_mapel_list = list of guru_ids for each mapel
        """
        individual = []
        kelas_ids = self._d.kelas_ids
        kelas_tingkatan = self._d.kelas_tingkatan

        for kelas_id in kelas_ids:
            tingkatan = kelas_tingkatan[kelas_id]

            # Generate mapel and guru assignments
            mapel_np, guru_np = self._generate_per_kelas(tingkatan)

            # Distribute mapel into days
            slot_per_hari = self._d.slot_per_hari
            hari_schedule = []

            slot_idx = 0
            for hari_id in range(5):
                hari_slots = slot_per_hari[hari_id]
                hari_mapel = list(mapel_np[slot_idx : slot_idx + hari_slots])
                hari_schedule.append(hari_mapel)
                slot_idx += hari_slots

            # Create guru_mapel list (one guru per mapel)
            mapel_guru_mapping = {}
            for i, mapel_id in enumerate(mapel_np):
                if mapel_id > 0 and mapel_id not in mapel_guru_mapping:
                    mapel_guru_mapping[mapel_id] = guru_np[i]

            guru_mapel_list = [mapel_guru_mapping.get(m + 1, 0) for m in range(13)]

            # Build kelas structure
            kelas = hari_schedule + [guru_mapel_list]
            individual.append(kelas)

        return individual

    def generate_population(self, size: int) -> tuple[np.ndarray, np.ndarray]:
        """Generate an initial population of *size* individuals."""
        n_kelas = self._d.jumlah_kelas
        slot_kelas = self._d.slot_per_kelas

        pop_mapel = np.zeros((size, n_kelas, slot_kelas), dtype=np.int16)
        pop_guru = np.zeros((size, n_kelas, slot_kelas), dtype=np.int16)

        for i in range(size):
            mapel_matrix, guru_matrix = self._individu_construct()
            pop_mapel[i] = mapel_matrix
            pop_guru[i] = guru_matrix

        logger.info("Generated initial population of %d individuals", size)
        return pop_mapel, pop_guru
