from collections import defaultdict

from typing import Any

import numpy as np

from app.algorithm.dictionary import DataDictionary

from app.core.logging import get_logger

logger = get_logger(__name__)

class Evaluator:

    def __init__(self, data_dict: DataDictionary) -> None:

        self._d = data_dict

    def guru_bentrok(self, guru_matrix: np.ndarray) -> int:

        pelanggaran = 0

        slot_per_kelas = self._d.slot_per_kelas

        for slot in range(slot_per_kelas):

            guru_slot = guru_matrix[:, slot]

            unik = np.unique(guru_slot)

            pelanggaran += len(guru_slot) - len(unik)

        return int(pelanggaran)

    def durasi_guru(self, guru_matrix: np.ndarray) -> int:

        pelanggaran = 0

        max_jam_guru = self._d.max_jam_guru

        semua_guru = guru_matrix.flatten()

        guru_ids, counts = np.unique(semua_guru, return_counts=True)

        for guru, jam in zip(guru_ids, counts):

            max_jam = max_jam_guru.get(int(guru), 0)

            if jam > max_jam:

                pelanggaran += jam - max_jam

        return int(pelanggaran)

    def distribusi_mapel(self, mapel_matrix: np.ndarray) -> int:

        pelanggaran = 0

        jumlah_kelas = self._d.jumlah_kelas

        slot_hari = self._d.slot_hari

        blok_mapel = self._d.blok_mapel

        for kelas in range(jumlah_kelas):

            jadwal = mapel_matrix[kelas]

            mapel_slot: dict[int, list[int]] = defaultdict(list)

            for slot, mapel in enumerate(jadwal):

                mapel_slot[int(mapel)].append(slot)

            for mapel, slots in mapel_slot.items():

                blok_expected = blok_mapel.get(mapel, [])

                if len(blok_expected) <= 1:

                    continue

                blok_real = self._hitung_blok(slots)

                if sorted(blok_real) != sorted(blok_expected):

                    pelanggaran += 1

                hari_set = set(int(slot_hari[s]) for s in slots)

                if len(hari_set) < len(blok_expected):

                    pelanggaran += 1

        return pelanggaran

    def mapel_siang(self, mapel_matrix: np.ndarray) -> int:

        TARGET_MAPEL = 8

        pelanggaran = 0

        slot_per_kelas = self._d.slot_per_kelas

        slot_hari = self._d.slot_hari

        batas_siang = self._d.batas_siang

        slot_awal_hari = self._d.slot_awal_hari

        for slot in range(slot_per_kelas):

            hari = int(slot_hari[slot])

            batas = batas_siang[hari - 1]

            slot_hari_ke = slot - int(slot_awal_hari[hari - 1])

            if slot_hari_ke < batas:

                continue

            pelanggaran += int(np.sum(mapel_matrix[:, slot] == TARGET_MAPEL))

        return pelanggaran

    def waktu_mgmp(self, mapel_matrix: np.ndarray) -> int:

        pelanggaran = 0

        jumlah_kelas = self._d.jumlah_kelas

        mgmp_mapel = self._d.mgmp_mapel

        slot_awal_hari = self._d.slot_awal_hari

        slot_akhir_hari = self._d.slot_akhir_hari

        batas_mgmp = self._d.batas_mgmp

        for kelas in range(jumlah_kelas):

            jadwal = mapel_matrix[kelas]

            for mapel, hari_mgmp in mgmp_mapel.items():

                hari_idx = hari_mgmp - 1

                start = int(slot_awal_hari[hari_idx])

                end = int(slot_akhir_hari[hari_idx])

                jumlah = int(np.sum(jadwal[start:end] == mapel))

                if jumlah > batas_mgmp[hari_idx]:

                    pelanggaran += jumlah - batas_mgmp[hari_idx]

        return pelanggaran

    def cek_wali_kelas(self, guru_matrix: np.ndarray) -> int:

        pelanggaran = 0

        wali_kelas = self._d.wali_kelas

        for guru, kelas in wali_kelas.items():

            if guru not in guru_matrix[kelas - 1]:

                pelanggaran += 1

        return pelanggaran

    def konsistensi_guru_mapel(

        self, mapel_matrix: np.ndarray, guru_matrix: np.ndarray

    ) -> int:

        pelanggaran = 0

        jumlah_kelas = self._d.jumlah_kelas

        for kelas in range(jumlah_kelas):

            jadwal_mapel = mapel_matrix[kelas]

            jadwal_guru = guru_matrix[kelas]

            for mapel in np.unique(jadwal_mapel):

                guru_set = np.unique(jadwal_guru[jadwal_mapel == mapel])

                if len(guru_set) > 1:

                    pelanggaran += len(guru_set) - 1

        return pelanggaran

    def evaluasi_individu(

        self, mapel_matrix: np.ndarray, guru_matrix: np.ndarray

    ) -> dict[str, int]:

        return {

            "guruBentrok": self.guru_bentrok(guru_matrix),

            "distribusiMapel": self.distribusi_mapel(mapel_matrix),

            "mapelSiang": self.mapel_siang(mapel_matrix),

            "durasiGuru": self.durasi_guru(guru_matrix),

            "waktuMGMP": self.waktu_mgmp(mapel_matrix),

            "cekWaliKelas": self.cek_wali_kelas(guru_matrix),

            "konsistensiGuruMapel": self.konsistensi_guru_mapel(

                mapel_matrix, guru_matrix

            ),

        }

    def hitung_fitness(self, hasil_evaluasi: dict[str, int]) -> float:

        fitness_weight = self._d.fitness_weight()

        fitness = 0.0

        for k, v in hasil_evaluasi.items():

            fitness += fitness_weight[k] * v

        return fitness

    def evaluate(

        self, mapel_matrix: np.ndarray, guru_matrix: np.ndarray

    ) -> tuple[float, dict[str, int]]:

        evaluasi = self.evaluasi_individu(mapel_matrix, guru_matrix)

        fitness = self.hitung_fitness(evaluasi)

        return fitness, evaluasi

    def evaluasi_populasi(

        self,

        pop_mapel: np.ndarray,

        pop_guru: np.ndarray,

    ) -> list[dict[str, Any]]:

        hasil_populasi = []

        for i in range(pop_mapel.shape[0]):

            mapel_matrix = pop_mapel[i]

            guru_matrix = pop_guru[i]

            evaluasi = self.evaluasi_individu(mapel_matrix, guru_matrix)

            fitness = self.hitung_fitness(evaluasi)

            hasil_populasi.append(

                {"fitness": fitness, "evaluasi": evaluasi, "index": i}

            )

        return hasil_populasi

    @staticmethod

    def _hitung_blok(slots: list[int]) -> list[int]:

        slots = sorted(slots)

        blok: list[int] = []

        panjang = 1

        for i in range(1, len(slots)):

            if slots[i] == slots[i - 1] + 1:

                panjang += 1

            else:

                blok.append(panjang)

                panjang = 1

        blok.append(panjang)

        return blok
