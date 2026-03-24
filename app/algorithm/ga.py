"""
Genetic Algorithm operators for timetabling.

Ported from GA-GWO15 notebook — uses numpy matrix representation:
    mapel_matrix : np.ndarray — shape (JUMLAH_KELAS, SLOT_PER_KELAS)
    guru_matrix  : np.ndarray — shape (JUMLAH_KELAS, SLOT_PER_KELAS)
"""

import random

import numpy as np

from app.algorithm.dictionary import DataDictionary
from app.algorithm.evaluation import Evaluator
from app.core.logging import get_logger

logger = get_logger(__name__)

# GA Parameters
CROSSOVER_PROB = 0.7
MUTATION_PROB = 0.8


class GeneticAlgorithm:
    """Encapsulates GA operators for the timetabling problem."""

    def __init__(self, data_dict: DataDictionary, evaluator: Evaluator) -> None:
        self._d = data_dict
        self._evaluator = evaluator

    # ── Selection ────────────────────────────────────────────────────

    def tournament_selection(
        self,
        pop_mapel: np.ndarray,
        pop_guru: np.ndarray,
        hasil_populasi: list[dict],
        tournament_size: int,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Select an individual via tournament selection.

        Returns:
            Copies of (mapel_matrix, guru_matrix) of the selected individual.
        """
        kandidat = random.sample(hasil_populasi, min(tournament_size, len(hasil_populasi)))
        terbaik = min(kandidat, key=lambda x: x["fitness"])
        idx = terbaik["index"]

        return pop_mapel[idx].copy(), pop_guru[idx].copy()

    # ── Crossover ────────────────────────────────────────────────────

    def crossover(
        self,
        parent1_mapel: np.ndarray,
        parent1_guru: np.ndarray,
        parent2_mapel: np.ndarray,
        parent2_guru: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Perform single-point crossover at the class level.

        Returns:
            (child1_mapel, child1_guru, child2_mapel, child2_guru)
        """
        jumlah_kelas = self._d.jumlah_kelas
        split = random.randint(1, jumlah_kelas - 1)

        child1_mapel = np.zeros_like(parent1_mapel)
        child1_guru = np.zeros_like(parent1_guru)
        child2_mapel = np.zeros_like(parent1_mapel)
        child2_guru = np.zeros_like(parent1_guru)

        # Child 1: first part from parent1, second from parent2
        child1_mapel[:split] = parent1_mapel[:split]
        child1_mapel[split:] = parent2_mapel[split:]
        child1_guru[:split] = parent1_guru[:split]
        child1_guru[split:] = parent2_guru[split:]

        # Child 2: first part from parent2, second from parent1
        child2_mapel[:split] = parent2_mapel[:split]
        child2_mapel[split:] = parent1_mapel[split:]
        child2_guru[:split] = parent2_guru[:split]
        child2_guru[split:] = parent1_guru[split:]

        return child1_mapel, child1_guru, child2_mapel, child2_guru

    # ── Mutation ─────────────────────────────────────────────────────

    def mutasi(
        self,
        mapel_matrix: np.ndarray,
        guru_matrix: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Adaptive mutation — targets the constraint with the highest violation.

        Directly matches the notebook's `mutasi()` function.
        """
        evaluasi = self._evaluator.evaluasi_individu(mapel_matrix, guru_matrix)

        # Find the worst constraint
        constraint = max(evaluasi, key=evaluasi.get)  # type: ignore[arg-type]

        jumlah_kelas = self._d.jumlah_kelas
        slot_per_kelas = self._d.slot_per_kelas
        kelas_ids = self._d.kelas_ids
        kelas_tingkatan = self._d.kelas_tingkatan
        guru_valid_mapel = self._d.guru_valid_mapel

        kelas = random.randint(0, jumlah_kelas - 1)

        if constraint == "distribusiMapel":
            # Swap two adjacent slots
            slot1 = random.randint(0, slot_per_kelas - 2)
            slot2 = slot1 + 1

            mapel_matrix[kelas, slot1], mapel_matrix[kelas, slot2] = (
                mapel_matrix[kelas, slot2],
                mapel_matrix[kelas, slot1],
            )
            guru_matrix[kelas, slot1], guru_matrix[kelas, slot2] = (
                guru_matrix[kelas, slot2],
                guru_matrix[kelas, slot1],
            )

        elif constraint == "guruBentrok":
            # Re-assign a random teacher for a random slot
            slot = random.randint(0, slot_per_kelas - 1)
            mapel = int(mapel_matrix[kelas, slot])
            tingkatan = kelas_tingkatan[kelas_ids[kelas]]
            guru_valid = guru_valid_mapel.get((mapel, tingkatan))

            if guru_valid:
                guru_matrix[kelas, slot] = random.choice(guru_valid)

        else:
            # Swap two random slots
            slot1 = random.randint(0, slot_per_kelas - 1)
            slot2 = random.randint(0, slot_per_kelas - 1)

            mapel_matrix[kelas, slot1], mapel_matrix[kelas, slot2] = (
                mapel_matrix[kelas, slot2],
                mapel_matrix[kelas, slot1],
            )
            guru_matrix[kelas, slot1], guru_matrix[kelas, slot2] = (
                guru_matrix[kelas, slot2],
                guru_matrix[kelas, slot1],
            )

        return mapel_matrix, guru_matrix
