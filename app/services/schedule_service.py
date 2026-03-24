import random

import threading

from typing import Any

import numpy as np

from app.algorithm.construct import PopulationConstructor

from app.algorithm.dictionary import DataDictionary

from app.algorithm.evaluation import Evaluator

from app.algorithm.ga import GeneticAlgorithm, CROSSOVER_PROB, MUTATION_PROB

from app.algorithm.gwo import GreyWolfOptimizer

from app.algorithm.repair import RepairOperator

from app.core.exceptions import AlgorithmException

from app.core.logging import get_logger

from app.schemas.schedule import (

    ScheduleRequest,

    ScheduleStatusResponse,

    ScheduleResult,

    ScheduleKelasResult,

    ScheduleSlotDetail,

    FitnessDetail,

)

logger = get_logger(__name__)

DEFAULT_GWO_INTERVAL = 20

DEFAULT_GWO_ITERATIONS = 20

class ScheduleService:

    def __init__(self, data_dict: DataDictionary) -> None:

        self._data_dict = data_dict

        self._status: str = "idle"

        self._progress: float = 0.0

        self._best_fitness: float | None = None

        self._result: dict[str, Any] | None = None

        self._error_message: str = ""

        self._lock = threading.Lock()

        self._fitness_log: list[dict[str, Any]] = []

    def generate(self, params: ScheduleRequest) -> ScheduleStatusResponse:

        with self._lock:

            if self._status == "running":

                return self.get_status()

            self._status = "running"

            self._progress = 0.0

            self._best_fitness = None

            self._result = None

            self._error_message = ""

            self._fitness_log = []

        thread = threading.Thread(

            target=self._run_algorithm,

            args=(params,),

            daemon=True,

        )

        thread.start()

        logger.info(

            "Schedule generation started: pop=%d, iter=%d, tourn=%d",

            params.population_size,

            params.max_iterations,

            params.tournament_size,

        )

        return self.get_status()

    def get_status(self) -> ScheduleStatusResponse:

        with self._lock:

            return ScheduleStatusResponse(

                status=self._status,

                progress=self._progress,

                best_fitness=self._best_fitness,

                message=self._error_message,

            )

    def get_latest_result(self) -> ScheduleResult:

        with self._lock:

            if self._result is None:

                raise AlgorithmException(

                    "Belum ada hasil penjadwalan. Jalankan generate terlebih dahulu."

                )

            return ScheduleResult(**self._result)

    def _run_algorithm(self, params: ScheduleRequest) -> None:

        try:

            constructor = PopulationConstructor(self._data_dict)

            evaluator = Evaluator(self._data_dict)

            ga = GeneticAlgorithm(self._data_dict, evaluator)

            gwo = GreyWolfOptimizer(self._data_dict, evaluator)

            repair = RepairOperator(self._data_dict, evaluator)

            pop_size = params.population_size

            max_iter = params.max_iterations

            tournament_size = params.tournament_size

            gwo_interval = params.gwo_interval

            gwo_iterations = params.gwo_iterations

            logger.info("Generating initial population of %d...", pop_size)

            pop_mapel, pop_guru = constructor.generate_population(pop_size)

            hasil_pop = evaluator.evaluasi_populasi(pop_mapel, pop_guru)

            best_fitness = float("inf")

            best_mapel: np.ndarray | None = None

            best_guru: np.ndarray | None = None

            initial_best = min(hasil_pop, key=lambda x: x["fitness"])

            if initial_best["fitness"] < best_fitness:

                best_fitness = initial_best["fitness"]

                idx = initial_best["index"]

                best_mapel = pop_mapel[idx].copy()

                best_guru = pop_guru[idx].copy()

            logger.info("Initial best fitness: %s", best_fitness)

            for gen in range(max_iter):

                with self._lock:

                    self._progress = (gen / max_iter) * 100

                    self._best_fitness = best_fitness

                new_pop_mapel_list: list[np.ndarray] = []

                new_pop_guru_list: list[np.ndarray] = []

                while len(new_pop_mapel_list) < pop_size:

                    p1_mapel, p1_guru = ga.tournament_selection(

                        pop_mapel, pop_guru, hasil_pop, tournament_size

                    )

                    p2_mapel, p2_guru = ga.tournament_selection(

                        pop_mapel, pop_guru, hasil_pop, tournament_size

                    )

                    if random.random() < CROSSOVER_PROB:

                        c1_mapel, c1_guru, c2_mapel, c2_guru = ga.crossover(

                            p1_mapel, p1_guru, p2_mapel, p2_guru

                        )

                    else:

                        c1_mapel, c1_guru = p1_mapel.copy(), p1_guru.copy()

                        c2_mapel, c2_guru = p2_mapel.copy(), p2_guru.copy()

                    if random.random() < MUTATION_PROB:

                        c1_mapel, c1_guru = ga.mutasi(c1_mapel, c1_guru)

                    if random.random() < MUTATION_PROB:

                        c2_mapel, c2_guru = ga.mutasi(c2_mapel, c2_guru)

                    c1_mapel, c1_guru = repair.repair(c1_mapel, c1_guru)

                    c2_mapel, c2_guru = repair.repair(c2_mapel, c2_guru)

                    new_pop_mapel_list.append(c1_mapel)

                    new_pop_guru_list.append(c1_guru)

                    if len(new_pop_mapel_list) < pop_size:

                        new_pop_mapel_list.append(c2_mapel)

                        new_pop_guru_list.append(c2_guru)

                pop_mapel = np.array(new_pop_mapel_list)

                pop_guru = np.array(new_pop_guru_list)

                hasil_pop = evaluator.evaluasi_populasi(pop_mapel, pop_guru)

                if gen % gwo_interval == 0 and gen != 0:

                    logger.info("GWO phase at generation %d", gen)

                    for iter_gwo in range(gwo_iterations):

                        pop_mapel, pop_guru = gwo.run_gwo(

                            pop_mapel, pop_guru, hasil_pop

                        )

                        hasil_pop = evaluator.evaluasi_populasi(

                            pop_mapel, pop_guru

                        )

                        best_gwo = min(x["fitness"] for x in hasil_pop)

                        logger.debug(

                            "GWO Iter %d Best: %s", iter_gwo, best_gwo

                        )

                gen_best = min(hasil_pop, key=lambda x: x["fitness"])

                avg_fitness = float(

                    np.mean([x["fitness"] for x in hasil_pop])

                )

                if gen_best["fitness"] < best_fitness:

                    best_fitness = gen_best["fitness"]

                    idx = gen_best["index"]

                    best_mapel = pop_mapel[idx].copy()

                    best_guru = pop_guru[idx].copy()

                if gen % 10 == 0:

                    logger.info(

                        "Gen %d | Best: %s | Avg: %.1f",

                        gen,

                        best_fitness,

                        avg_fitness,

                    )

                self._fitness_log.append(

                    {

                        "generation": gen,

                        "best_fitness": best_fitness,

                        "avg_fitness": avg_fitness,

                    }

                )

            assert best_mapel is not None and best_guru is not None

            final_fitness, final_evaluasi = evaluator.evaluate(

                best_mapel, best_guru

            )

            result_data = self._format_result(

                best_mapel, best_guru, final_fitness, final_evaluasi

            )

            with self._lock:

                self._progress = 100.0

                self._best_fitness = final_fitness

                self._status = "completed"

                self._result = result_data

            logger.info(

                "Schedule generation completed. Best fitness: %s",

                final_fitness,

            )

        except Exception as exc:

            logger.exception("Schedule generation failed")

            with self._lock:

                self._status = "failed"

                self._error_message = str(exc)

    def _format_result(

        self,

        mapel_matrix: np.ndarray,

        guru_matrix: np.ndarray,

        fitness: float,

        evaluasi: dict[str, int],

    ) -> dict[str, Any]:

        detail_per_kelas: list[dict[str, Any]] = []

        total_conflict = sum(evaluasi.values())

        kelas_ids = self._data_dict.kelas_ids

        kelas_df = self._data_dict.kelas_df

        mapel_df = self._data_dict.mapel_df

        guru_df = self._data_dict.guru_df

        slot_df = self._data_dict.slot_df

        mapel_lookup = {

            row["mapel_id"]: row["nama_mapel"]

            for _, row in mapel_df.iterrows()

        }

        guru_lookup = {

            row["guru_id"]: row["nama_guru"]

            for _, row in guru_df.iterrows()

        }

        kelas_lookup = {

            row["kelas_id"]: row["nama_kelas"]

            for _, row in kelas_df.iterrows()

        }

        slot_times = []

        for _, row in slot_df.iterrows():

            slot_times.append(

                {

                    "hari": row["hari"],

                    "jam_mulai": row["jam_mulai"],

                    "jam_selesai": row["jam_selesai"],

                }

            )

        for kelas_idx in range(len(kelas_ids)):

            kelas_id = int(kelas_ids[kelas_idx])

            kelas_nama = kelas_lookup.get(kelas_id, f"Kelas {kelas_id}")

            jadwal: list[dict[str, Any]] = []

            for slot_id in range(len(mapel_matrix[kelas_idx])):

                mapel_id = int(mapel_matrix[kelas_idx][slot_id])

                guru_id = int(guru_matrix[kelas_idx][slot_id])

                if mapel_id > 0:

                    mapel_nama = mapel_lookup.get(

                        mapel_id, f"Mapel {mapel_id}"

                    )

                    guru_nama = guru_lookup.get(guru_id, f"Guru {guru_id}")

                    slot_time_info = (

                        slot_times[slot_id]

                        if slot_id < len(slot_times)

                        else {

                            "hari": f"Hari {slot_id}",

                            "jam_mulai": "00:00",

                            "jam_selesai": "00:00",

                        }

                    )

                    jadwal.append(

                        {

                            "slot_id": slot_id,

                            "hari": slot_time_info["hari"],

                            "jam_mulai": slot_time_info["jam_mulai"],

                            "jam_selesai": slot_time_info["jam_selesai"],

                            "mapel_id": mapel_id,

                            "mapel_nama": mapel_nama,

                            "guru_id": guru_id,

                            "guru_nama": guru_nama,

                        }

                    )

            detail_per_kelas.append(

                {

                    "kelas_id": kelas_id,

                    "kelas_nama": kelas_nama,

                    "jadwal": jadwal,

                }

            )

        return {

            "fitness": fitness,

            "total_conflicts": total_conflict,

            "detail_per_kelas": detail_per_kelas,

        }
