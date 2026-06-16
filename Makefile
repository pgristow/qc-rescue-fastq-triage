.PHONY: all qc report clean

# Generate messy data → QC → fix → re-QC → render the report.
all: report

qc:
	bash scripts/run_qc.sh

report: qc
	quarto render
	cp -f results/multiqc_trimmed.html docs/multiqc.html

clean:
	rm -rf data trimmed qc_raw qc_trim docs .quarto _freeze \
	       results/*.html results/*_data results/*.json results/*.csv
