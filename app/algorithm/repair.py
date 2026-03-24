"""
Repair operator — fixes constraint violations after GA/GWO operations.

Ported from GA-GWO15 notebook. Currently repairs guru conflicts
(teacher teaching multiple classes at the same time slot).
"""

import random

import numpy as np

from app.algorithm.dictionary import DataDictionary
from app.core.logging import get_logger

logger = get_logger(__name__)


class RepairOperator:
    """Repairs invalid timetable encodings."""

    def __init__(self, data_dict: "DataDictionary", evaluator=None) -> None:
        self._d = data_dict
        self._evaluator = evaluator

    def repair(
        self,
        mapel_matrix: np.ndarray,
        guru_matrix: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Repair an individual to satisfy hard constraints.

        Currently repairs:
        - Guru bentrok (teacher conflict): when a teacher is scheduled
          in multiple classes at the same time slot, randomly reassign
          one of them to a valid alternative teacher.
        """
        # Lazy-import evaluator to avoid circular dependencies
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

                # Find teachers that appear more than once in this slot
                bentrok = unik[counts > 1]

                for g in bentrok:
                    # Find which classes have this conflicting teacher
                    kelas_bentrok = np.where(guru_slot == g)[0]

                    # Pick one class to fix
                    kelas = random.choice(kelas_bentrok)

                    # Get the subject at this slot for this class
                    mapel = int(mapel_matrix[kelas, slot])

                    # Get the grade level for this class
                    tingkatan = kelas_tingkatan[kelas_ids[kelas]]

                    # Find valid teachers for this subject + grade
                    guru_valid = guru_valid_mapel.get((mapel, tingkatan))

                    if guru_valid:
                        guru_matrix[kelas, slot] = random.choice(guru_valid)

        return mapel_matrix, guru_matrix
