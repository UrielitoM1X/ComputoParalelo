#!/usr/bin/env bash
# Ejecutar desde practicas/practica1/src: bash ../scripts/run_all.sh
set -e; mkdir -p ../results; make -s

echo "variant,n,rep,seconds,gflops,checksum" > ../results/c.csv
for n in 256 512 1024; do
    for v in 00 02 03; do 
        ./matmul_$v $n 5 c_$v >> ../results/c.csv
    done
done

echo "variant,n,rep,seconds,gflops,checksum" > ../results/py_puro.csv
for n in 64 128 256; do 
    python3 matmul_pure.py $n 5 >> ../results/py_puro.csv
done

echo "variant,n,rep,seconds,gflops,cpu_over_wall" > ../results/numpy.csv
for n in 256 512 1024 2048; do
    python3 matmul_numpy.py $n 5 >> ../results/numpy.csv
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    python3 matmul_numpy.py $n 5 | sed 's/^numpy/numpy_1hilo/' >> ../results/numpy.csv
done