#!/usr/bin/env python3
"""Generate four paired-end FASTQ samples with KNOWN, deliberately-injected problems.

Because we inject the defects ourselves, the QC step can be *validated*: it should detect
exactly what we put in. This is a reproducible stand-in for the messy real-world data clients
send ("my run looks weird / why are my numbers off?").

Samples
-------
S1_clean    : well-behaved baseline (high quality, proper inserts, no adapters)
S2_adapter  : short inserts -> 3' adapter read-through (Illumina TruSeq adapters)
S3_lowqual  : quality collapses toward the 3' end (needs quality trimming)
S4_overrep  : ~45% of reads are one overrepresented/contaminant sequence (duplication)
"""
import gzip
import os
import random

random.seed(42)

OUT = os.environ.get("DATA_DIR", "data")
os.makedirs(OUT, exist_ok=True)

READLEN = 150
N_PAIRS = 40_000
GENOME_LEN = 30_000
BASES = "ACGT"
ADAPTER_R1 = "AGATCGGAAGAGCACACGTCTGAACTCCAGTCA"
ADAPTER_R2 = "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT"
COMP = str.maketrans("ACGTN", "TGCAN")

genome = "".join(random.choice(BASES) for _ in range(GENOME_LEN))
# A single fixed sequence that will be over-represented in S4 (e.g. an rRNA-like contaminant).
CONTAM = "".join(random.choice(BASES) for _ in range(READLEN))


def revcomp(s):
    return s.translate(COMP)[::-1]


def qual_string(length, hi=38, lo=38, taper=False):
    """Phred+33 quality string. If taper, quality ramps from hi (5') down to lo (3')."""
    out = []
    for i in range(length):
        if taper:
            q = int(hi - (hi - lo) * (i / max(1, length - 1)))
        else:
            q = hi
        q = max(2, min(40, q + random.randint(-1, 1)))
        out.append(chr(q + 33))
    return "".join(out)


def fragment(insert):
    start = random.randint(0, GENOME_LEN - insert - 1)
    return genome[start:start + insert]


def make_pair(kind):
    """Return (r1_seq, r1_qual, r2_seq, r2_qual) for one read pair of the given defect kind."""
    if kind == "adapter":
        insert = random.randint(60, 110)             # shorter than read -> read-through
        frag = fragment(insert)
        r1 = (frag + ADAPTER_R1 + "A" * READLEN)[:READLEN]
        r2 = (revcomp(frag) + ADAPTER_R2 + "A" * READLEN)[:READLEN]
        return r1, qual_string(READLEN), r2, qual_string(READLEN)
    if kind == "lowqual":
        frag = fragment(READLEN)
        r2 = revcomp(frag)
        return frag, qual_string(READLEN, hi=38, lo=8, taper=True), \
            r2, qual_string(READLEN, hi=38, lo=8, taper=True)
    if kind == "overrep" and random.random() < 0.45:
        return CONTAM, qual_string(READLEN), revcomp(CONTAM), qual_string(READLEN)
    # clean (and the non-contaminant fraction of overrep)
    frag = fragment(random.randint(200, 400))
    r1 = frag[:READLEN]
    r2 = revcomp(frag)[:READLEN]
    return r1, qual_string(READLEN), r2, qual_string(READLEN)


def write_sample(name, kind):
    r1p = os.path.join(OUT, f"{name}_R1.fastq.gz")
    r2p = os.path.join(OUT, f"{name}_R2.fastq.gz")
    with gzip.open(r1p, "wt") as f1, gzip.open(r2p, "wt") as f2:
        for i in range(N_PAIRS):
            r1, q1, r2, q2 = make_pair(kind)
            rid = f"{name}:{i}"
            f1.write(f"@{rid}/1\n{r1}\n+\n{q1}\n")
            f2.write(f"@{rid}/2\n{r2}\n+\n{q2}\n")
    print(f"[make] {name}: {N_PAIRS:,} pairs ({kind}) -> {r1p}")


if __name__ == "__main__":
    write_sample("S1_clean", "clean")
    write_sample("S2_adapter", "adapter")
    write_sample("S3_lowqual", "lowqual")
    write_sample("S4_overrep", "overrep")
    print("[make] done.")
