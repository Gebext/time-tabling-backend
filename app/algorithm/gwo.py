"""
Grey Wolf Optimizer operators for timetabling.

Ported from GA-GWO15 notebook — uses numpy matrix representation.
GWO updates wolf positions by copying partial schedules from the
alpha/beta/delta leaders, with optional local swap improvement
followed by a repair step.
"""

import random

import numpy as np

from app.algorithm.dictionary import DataDictionary
from app.algorithm.evaluation import Evaluator
from app.core.logging import get_logger

logger = get_logger(__name__)


class GreyWolfOptimizer:
    """Encapsulates GWO operators for the timetabling problem."""

    def __init__(self, data_dict: DataDictionary, evaluator: Evaluator) -> None:
        self._d = data_dict
        self._evaluator = evaluator
        # Import here to avoid circular imports
        from app.algorithm.repair import RepairOperator
        self._repair = RepairOperator(data_dict, evaluator)

    def run_gwo(
        self,
        pop_mapel: np.ndarray,
        pop_guru: np.ndarray,
        hasil_populasi: list[dict],
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Perform one GWO iteration: update all wolves based on
        alpha, beta, delta leaders.

        Args:
            pop_mapel: Population mapel matrices — shape (POP, KELAS, SLOT)
            pop_guru: Population guru matrices — shape (POP, KELAS, SLOT)
            hasil_populasi: Evaluation results with fitness & index

        Returns:
            Updated (pop_mapel, pop_guru)
        """
        jumlah_kelas = self._d.jumlah_kelas
        slot_awal_hari = self._d.slot_awal_hari
        slot_akhir_hari = self._d.slot_akhir_hari

        # Sort by fitness (lower is better)
        hasil_sorted = sorted(hasil_populasi, key=lambda x: x["fitness"])

        alpha_idx = hasil_sorted[0]["index"]
        beta_idx = hasil_sorted[1]["index"]
        delta_idx = hasil_sorted[2]["index"]

        alpha_mapel = pop_mapel[alpha_idx]
        alpha_guru = pop_guru[alpha_idx]

        beta_mapel = pop_mapel[beta_idx]
        beta_guru = pop_guru[beta_idx]

        delta_mapel = pop_mapel[delta_idx]
        delta_guru = pop_guru[delta_idx]

        new_pop_mapel = []
        new_pop_guru = []

        for i in range(len(pop_mapel)):
            mapel = pop_mapel[i].copy()
            guru = pop_guru[i].copy()

            # Preserve alpha (elitism)
            if i == alpha_idx:
                new_pop_mapel.append(mapel)
                new_pop_guru.append(guru)
                continue

            # ── Pick random class & day ──
            kelas = random.randint(0, jumlah_kelas - 1)
            hari = random.randint(0, 4)

            start = int(slot_awal_hari[hari])
            end = int(slot_akhir_hari[hari])

            # ── Pick wolf guide ──
            r = random.random()
            if r < 0.5:
                src_mapel = alpha_mapel
                src_guru = alpha_guru
            elif r < 0.8:
                src_mapel = beta_mapel
                src_guru = beta_guru
            else:
                src_mapel = delta_mapel
                src_guru = delta_guru

            # ── Partial slot copy ──
            panjang = end - start
            size = random.randint(1, max(1, panjang // 2))
            s = random.randint(start, end - size)

            mapel[kelas, s : s + size] = src_mapel[kelas, s : s + size]
            guru[kelas, s : s + size] = src_guru[kelas, s : s + size]

            # ── Local swap improvement (50% chance) ──
            if random.random() < 0.5:
                slot1 = random.randint(start, end - 1)
                slot2 = random.randint(start, end - 1)

                mapel[kelas, slot1], mapel[kelas, slot2] = (
                    mapel[kelas, slot2],
                    mapel[kelas, slot1],
                )
                guru[kelas, slot1], guru[kelas, slot2] = (
                    guru[kelas, slot2],
                    guru[kelas, slot1],
                )

            # ── Repair constraints ──
            mapel, guru = self._repair.repair(mapel, guru)

            new_pop_mapel.append(mapel)
            new_pop_guru.append(guru)

        return np.array(new_pop_mapel), np.array(new_pop_guru)
