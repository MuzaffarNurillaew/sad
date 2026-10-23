PANDOC_VERSION := 3.1.11.1
PANDOC_URL := https://github.com/jgm/pandoc/releases/download/$(PANDOC_VERSION)/pandoc-$(PANDOC_VERSION)-linux-amd64.tar.gz
PLANTUML_VERSION := 1.2024.8
PLANTUML_URL := https://github.com/plantuml/plantuml/releases/download/v$(PLANTUML_VERSION)/plantuml-$(PLANTUML_VERSION).jar

PANDOC := tools/bin/pandoc
PLANTUML := tools/plantuml.jar
PYTHON := .venv/bin/python

SECTIONS := 0-business-case.md \
	1-requirements-gathering-process.md \
	2-use-case-diagram.md \
	3-use-cases.md \
	4-data-flow-diagram.md \
	5-activity-diagram.md \
	6-sequence-diagram.md \
	7-requirements-catalogue.md

BUILD := build

.PHONY: all setup reference report clean distclean

all: report

report: $(BUILD)/report.docx
	@echo "Compiled report: $(BUILD)/report.docx"

setup: $(PANDOC) $(PLANTUML) .venv/deps-installed

# --- Toolchain (downloaded once, no sudo required) ---

$(PANDOC):
	mkdir -p tools/bin
	curl -sL --max-time 300 "$(PANDOC_URL)" -o /tmp/pandoc-dl.tar.gz
	tar -xzf /tmp/pandoc-dl.tar.gz -C /tmp pandoc-$(PANDOC_VERSION)/bin/pandoc
	cp /tmp/pandoc-$(PANDOC_VERSION)/bin/pandoc $(PANDOC)
	chmod +x $(PANDOC)
	rm -rf /tmp/pandoc-dl.tar.gz /tmp/pandoc-$(PANDOC_VERSION)

$(PLANTUML):
	mkdir -p tools
	curl -sL --max-time 120 "$(PLANTUML_URL)" -o $(PLANTUML)

.venv/deps-installed:
	python3 -m venv .venv
	.venv/bin/pip install --quiet python-docx
	touch .venv/deps-installed

# --- Report build ---

tools/reference.docx: scripts/build_reference_docx.py | setup
	$(PANDOC) --print-default-data-file reference.docx > tools/reference-base.docx
	$(PYTHON) scripts/build_reference_docx.py tools/reference-base.docx tools/reference.docx

$(BUILD)/combined.md: $(SECTIONS) scripts/render_diagrams.py | setup
	mkdir -p $(BUILD)
	$(PYTHON) scripts/render_diagrams.py \
		--out $(BUILD)/combined.md \
		--diagrams-dir $(BUILD)/diagrams \
		--plantuml-jar $(PLANTUML) \
		$(SECTIONS)

$(BUILD)/report.docx: $(BUILD)/combined.md tools/reference.docx
	$(PANDOC) $(BUILD)/combined.md -o $(BUILD)/report.docx \
		--reference-doc=tools/reference.docx --toc --toc-depth=2

# --- Cleanup ---

clean:
	rm -rf $(BUILD)

distclean: clean
	rm -rf tools/bin tools/plantuml.jar tools/reference.docx tools/reference-base.docx .venv
