import random

import numpy as np

from app.algorithm.dictionary import DataDictionary

from app.algorithm.evaluation import Evaluator

from app.core.logging import get_logger

logger = get_logger(__name__)

CROSSOVER_PROB = 0.7

MUTATION_PROB = 0.8

class GeneticAlgorithm:

    def __init__(self, data_dict: DataDictionary, evaluator: Evaluator) -> None:

        self._d = data_dict

        self._evaluator = evaluator

    def tournament_selection(

        self,

        pop_mapel: np.ndarray,

        pop_guru: np.ndarray,

        hasil_populasi: list[dict],

        tournament_size: int,

    ) -> tuple[np.ndarray, np.ndarray]:

        kandidat = random.sample(hasil_populasi, min(tournament_size, len(hasil_populasi)))

        terbaik = min(kandidat, key=lambda x: x["fitness"])

        idx = terbaik["index"]

        return pop_mapel[idx].copy(), pop_guru[idx].copy()

    def crossover(

        self,

        parent1_mapel: np.ndarray,

        parent1_guru: np.ndarray,

        parent2_mapel: np.ndarray,

        parent2_guru: np.ndarray,

    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

        jumlah_kelas = self._d.jumlah_kelas

        split = random.randint(1, jumlah_kelas - 1)

        child1_mapel = np.zeros_like(parent1_mapel)

        child1_guru = np.zeros_like(parent1_guru)

        child2_mapel = np.zeros_like(parent1_mapel)

        child2_guru = np.zeros_like(parent1_guru)

        child1_mapel[:split] = parent1_mapel[:split]

        child1_mapel[split:] = parent2_mapel[split:]

        child1_guru[:split] = parent1_guru[:split]

        child1_guru[split:] = parent2_guru[split:]

        child2_mapel[:split] = parent2_mapel[:split]

        child2_mapel[split:] = parent1_mapel[split:]

        child2_guru[:split] = parent2_guru[:split]

        child2_guru[split:] = parent1_guru[split:]

        return child1_mapel, child1_guru, child2_mapel, child2_guru

    def mutasi(

        self,

        mapel_matrix: np.ndarray,

        guru_matrix: np.ndarray,

    ) -> tuple[np.ndarray, np.ndarray]:

        evaluasi = self._evaluator.evaluasi_individu(mapel_matrix, guru_matrix)

        constraint = max(evaluasi, key=evaluasi.get)

        jumlah_kelas = self._d.jumlah_kelas

        slot_per_kelas = self._d.slot_per_kelas

        kelas_ids = self._d.kelas_ids

        kelas_tingkatan = self._d.kelas_tingkatan

        guru_valid_mapel = self._d.guru_valid_mapel

        kelas = random.randint(0, jumlah_kelas - 1)

        if constraint == "distribusiMapel":

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

            slot = random.randint(0, slot_per_kelas - 1)

            mapel = int(mapel_matrix[kelas, slot])

            tingkatan = kelas_tingkatan[kelas_ids[kelas]]

            guru_valid = guru_valid_mapel.get((mapel, tingkatan))

            if guru_valid:

                guru_matrix[kelas, slot] = random.choice(guru_valid)

        else:

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
