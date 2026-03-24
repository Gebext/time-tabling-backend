import random

import numpy as np

from app.algorithm.dictionary import DataDictionary

from app.core.logging import get_logger

logger = get_logger(__name__)

class RepairOperator:

    def __init__(self, data_dict: "DataDictionary", evaluator=None) -> None:

        self._d = data_dict

        self._evaluator = evaluator

    def repair(

        self,

        mapel_matrix: np.ndarray,

        guru_matrix: np.ndarray,

    ) -> tuple[np.ndarray, np.ndarray]:

        if self._evaluator is None:

            from app.algorithm.evaluation import Evaluator

            self._evaluator = Evaluator(self._d)

        evaluasi = self._evaluator.evaluasi_individu(mapel_matrix, guru_matrix)

        if evaluasi["guruBentrok"] > 0:

            slot_per_kelas = self._d.slot_per_kelas

            kelas_ids = self._d.kelas_ids

            kelas_tingkatan = self._d.kelas_tingkatan

            guru_valid_mapel = self._d.guru_valid_mapel

            for slot in range(slot_per_kelas):

                guru_slot = guru_matrix[:, slot]

                unik, counts = np.unique(guru_slot, return_counts=True)

                bentrok = unik[counts > 1]

                for g in bentrok:

                    kelas_bentrok = np.where(guru_slot == g)[0]

                    kelas = random.choice(kelas_bentrok)

                    mapel = int(mapel_matrix[kelas, slot])

                    tingkatan = kelas_tingkatan[kelas_ids[kelas]]

                    guru_valid = guru_valid_mapel.get((mapel, tingkatan))

                    if guru_valid:

                        guru_matrix[kelas, slot] = random.choice(guru_valid)

        return mapel_matrix, guru_matrix
