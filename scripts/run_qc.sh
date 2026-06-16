#!/usr/bin/env bash
# Diagnose -> fix -> re-diagnose. Generates the messy data, runs QC before and after
# cleaning with fastp, and aggregates with MultiQC.
set -euo pipefail

THREADS="${THREADS:-4}"
DATA_DIR="${DATA_DIR:-data}"
mkdir -p "$DATA_DIR" qc_raw qc_trim trimmed results

# 0. Generate messy data (idempotent).
if [ ! -f "${DATA_DIR}/S1_clean_R1.fastq.gz" ]; then
  python scripts/make_messy_data.py
fi

SAMPLES=(S1_clean S2_adapter S3_lowqual S4_overrep)

# 1. QC the raw data.
echo "[qc] FastQC on raw reads..."
fastqc -q -t "$THREADS" -o qc_raw "${DATA_DIR}"/*.fastq.gz
multiqc -f -q -o results -n multiqc_raw qc_raw >/dev/null 2>&1

# 2. Clean each sample with fastp (adapter + quality trimming), capturing before/after JSON.
for s in "${SAMPLES[@]}"; do
  echo "[fix] fastp ${s}..."
  fastp -i "${DATA_DIR}/${s}_R1.fastq.gz" -I "${DATA_DIR}/${s}_R2.fastq.gz" \
        -o "trimmed/${s}_R1.fastq.gz" -O "trimmed/${s}_R2.fastq.gz" \
        --detect_adapter_for_pe --qualified_quality_phred 20 --length_required 36 \
        -j "results/${s}.fastp.json" -h "results/${s}.fastp.html" \
        -w "$THREADS" >/dev/null 2>&1
done

# 3. QC the cleaned data.
echo "[qc] FastQC on cleaned reads..."
fastqc -q -t "$THREADS" -o qc_trim trimmed/*.fastq.gz
multiqc -f -q -o results -n multiqc_trimmed qc_trim >/dev/null 2>&1

echo "[done] fastp JSON + MultiQC reports in results/"
