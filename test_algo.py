import sys
sys.path.insert(0, '.')

print('Step 1: imports...', flush=True)

from app.algorithm.dictionary import DataDictionary
from app.algorithm.construct import PopulationConstructor
from app.algorithm.evaluation import Evaluator
import numpy as np

print('Step 2: DataDictionary...', flush=True)
dd = DataDictionary('data/csv')
print(f'  -> {dd.jumlah_kelas} kelas, {dd.slot_per_kelas} slots', flush=True)

print('Step 3: Generate population...', flush=True)
constructor = PopulationConstructor(dd)
pop_mapel, pop_guru = constructor.generate_population(5)
print(f'  -> shape: {pop_mapel.shape}', flush=True)

print('Step 4: Evaluate...', flush=True)
evaluator = Evaluator(dd)
hasil = evaluator.evaluasi_populasi(pop_mapel, pop_guru)
for h in hasil:
    print(f'  Ind {h["index"]}: fitness={h["fitness"]}', flush=True)

print('Step 5: GA crossover...', flush=True)
from app.algorithm.ga import GeneticAlgorithm
ga = GeneticAlgorithm(dd, evaluator)
p1_m, p1_g = pop_mapel[0].copy(), pop_guru[0].copy()
p2_m, p2_g = pop_mapel[1].copy(), pop_guru[1].copy()
c1_m, c1_g, c2_m, c2_g = ga.crossover(p1_m, p1_g, p2_m, p2_g)
print('  -> OK', flush=True)

print('Step 6: GA mutasi...', flush=True)
c1_m, c1_g = ga.mutasi(c1_m, c1_g)
print('  -> OK', flush=True)

print('Step 7: Repair...', flush=True)
from app.algorithm.repair import RepairOperator
repair = RepairOperator(dd, evaluator)
c1_m, c1_g = repair.repair(c1_m, c1_g)
print('  -> OK', flush=True)

print('Step 8: GWO...', flush=True)
from app.algorithm.gwo import GreyWolfOptimizer
gwo = GreyWolfOptimizer(dd, evaluator)
print('  -> GWO init OK, running...', flush=True)
pop_m2, pop_g2 = gwo.run_gwo(pop_mapel, pop_guru, hasil)
print('  -> OK', flush=True)

print('\nALL TESTS PASSED!', flush=True)
