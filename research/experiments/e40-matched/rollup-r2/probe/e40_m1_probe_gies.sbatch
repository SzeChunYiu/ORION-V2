#!/bin/bash
#SBATCH -A lu2026-2-51
#SBATCH --partition=lu48
#SBATCH --job-name=o2-e40m1-gies
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
module load GCC/11.3.0 OpenMPI/4.1.2 Python/3.10.4
source /projects/hep/fs9/users/scyiu/orion-v2-e45/venv-causal/bin/activate
D=/projects/hep/fs9/users/scyiu/orion-v2-e45/campaign-e40-m1-probe
export E40M_ROOT=$D
cd $D
for cell in "observational 0.05 510005" "interventional 0.05 510006" "partial_interventional 0.05 510007" "interventional 1.0 510008"; do
  set -- $cell
  echo "=== $1 subset=$2 exp=$3 model=gies ==="
  python probe_driver_gies.py "$1" "$2" "$3" gies || echo "CELL_FAIL $1 $2"
done
echo E40M1_GIES_PROBE_ALL_DONE
