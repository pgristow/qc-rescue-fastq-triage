# FASTQ QC rescue — diagnosing and fixing messy sequencing data

[![Reproduce](https://github.com/pgristow/qc-rescue-fastq-triage/actions/workflows/publish.yml/badge.svg)](https://github.com/pgristow/qc-rescue-fastq-triage/actions/workflows/publish.yml)
[![Live report](https://img.shields.io/badge/live%20report-GitHub%20Pages-2e7d32)](https://pgristow.github.io/qc-rescue-fastq-triage/)
[![Made with Quarto](https://img.shields.io/badge/made%20with-Quarto-447099)](https://quarto.org)

> **Roche Principal Scientist (NGS) & PhD — I turn sequencing data into clean, reproducible answers.**

The most common paid bioinformatics request isn't a fancy analysis — it's *"my run looks weird,
what's wrong with my data?"* This repo takes four samples, **diagnoses** each, **fixes** it, and
**proves** the fix worked. The defects are *deliberately injected*, so the diagnosis is verifiable:
QC should detect exactly what was planted.

### 👉 [**See the live report**](https://pgristow.github.io/qc-rescue-fastq-triage/)
### 📄 [**Sample one-page deliverable (PDF)**](https://pgristow.github.io/qc-rescue-fastq-triage/deliverable.pdf) — what lands in your inbox

---

## The question
*Is this data salvageable, what's wrong with it, and can you fix it?*

## The data
Four synthetic paired-end samples with **known injected problems** — so the diagnosis can be checked
against ground truth (fully reproducible, no downloads):

| Sample | Injected problem |
|---|---|
| `S1_clean` | none (baseline) |
| `S2_adapter` | 3' adapter read-through |
| `S3_lowqual` | quality collapse toward the 3' end |
| `S4_overrep` | overrepresented / contaminant sequence |

## Key decisions (and why)
- **Injected, known defects** — makes the diagnosis *validatable* (the honest equivalent of a truth
  set), not a black box.
- **Conservative `fastp` cleaning** — fixes adapters + low quality without over-trimming, which can
  itself introduce bias.
- **Before/after proof** — every read removed has a documented reason.

## The result
A plain-English **diagnosis that matches the injected defects**, cleaned FASTQs, before/after QC
proof (Q30 recovery, reads retained), an embedded MultiQC report, and a go/no-go verdict per sample.

## What you get if you hire me for this
| Deliverable | Included |
|---|---|
| Per-sample diagnosis (what's wrong) | ✅ |
| Cleaned, analysis-ready FASTQs | ✅ |
| Before/after QC proof (FastQC + MultiQC) | ✅ |
| Go / no-go verdict per sample | ✅ |
| Reproducible report + interpretation | ✅ |

## Reproduce it
```bash
git clone https://github.com/pgristow/qc-rescue-fastq-triage
cd qc-rescue-fastq-triage
conda env create -f environment.yml && conda activate qc-rescue
make all      # generate messy data → QC → fix → re-QC → render
```
Or with Docker: `docker build -t qcrescue . && docker run --rm -v "$PWD":/work qcrescue`.

## Note on scope
A reproducible demonstration on synthetic data. Production engagements run an automated triage
across a whole run (and add cross-species contaminant screening and sample-swap detection) on
**your** data under NDA. The demo sells the *service*; the engine stays private.

## Licence & attribution
Code: MIT (see `LICENSE`). Built with [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/),
[fastp](https://github.com/OpenGene/fastp), [MultiQC](https://multiqc.info), and [Quarto](https://quarto.org).
