# Makefile for basics topic
TOPIC = supervised
SLIDES_DIR = slides
ASSETS_DIR = assets
SHARED_DIR = ../shared

# Find all .tex files in slides directory
TEX_FILES := $(wildcard $(SLIDES_DIR)/*.tex)
PDF_FILES := $(TEX_FILES:.tex=.pdf)

# Default target
all:
	@echo "uD83DuDCCA Building $(words $(TEX_FILES)) slides in $(TOPIC)..."
	@$(MAKE) $(PDF_FILES)
	@echo "uD83DuDCCA u2705 Topic $(TOPIC) completed: $(words $(PDF_FILES)) PDFs generated"

# Rule to compile LaTeX to PDF
# Rule to compile LaTeX to PDF using XeLaTeX for Inter font support
$(SLIDES_DIR)/%.pdf: $(SLIDES_DIR)/%.tex $(SHARED_DIR)/styles/*.sty $(SHARED_DIR)/notation/*.sty
	@echo "  🔨 Compiling $(notdir $<)..."
	@cd $(SLIDES_DIR) && xelatex -interaction=batchmode $(notdir $<) > /dev/null 2>&1 || true
	@cd $(SLIDES_DIR) && xelatex -interaction=batchmode $(notdir $<) > /dev/null 2>&1 || true
	@if [ ! -f $@ ]; then echo "    ❌ ERROR: Failed to generate $@"; exit 1; else echo "    ✅ Generated $@"; fi

# Clean auxiliary files
clean:
	cd $(SLIDES_DIR) && rm -f *.aux *.log *.nav *.out *.snm *.toc *.vrb *.fls *.fdb_latexmk *.synctex.gz *.dat *.script

# Clean all generated files (only PDFs that have corresponding .tex files)
distclean: clean
	cd $(SLIDES_DIR) && for tex in *.tex; do [ -f "$$tex" ] && rm -f "$${tex%.tex}.pdf"; done

# Copy PDFs to main slides directory for Quarto
deploy: $(PDF_FILES)
	@echo "Copying PDFs to main slides directory..."
	cp $(PDF_FILES) ../slides/

# Show status
status:
	@echo "Topic: $(TOPIC)"
	@echo "LaTeX files: $(TEX_FILES)"
	@echo "PDF files: $(PDF_FILES)"

.PHONY: all clean distclean deploy status