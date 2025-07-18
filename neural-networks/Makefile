# Makefile for basics topic
TOPIC = neural-networks
SLIDES_DIR = slides
ASSETS_DIR = assets
SHARED_DIR = ../shared

# Find all .tex files in slides directory
TEX_FILES := $(wildcard $(SLIDES_DIR)/*.tex)
PDF_FILES := $(TEX_FILES:.tex=.pdf)

# Default target
all: $(PDF_FILES)

# Rule to compile LaTeX to PDF
$(SLIDES_DIR)/%.pdf: $(SLIDES_DIR)/%.tex
	@echo "Compiling $< to $@"
	cd $(SLIDES_DIR) && pdflatex -interaction=nonstopmode $(notdir $<)
	cd $(SLIDES_DIR) && pdflatex -interaction=nonstopmode $(notdir $<)

# Clean auxiliary files
clean:
	cd $(SLIDES_DIR) && rm -f *.aux *.log *.nav *.out *.snm *.toc *.vrb *.fls *.fdb_latexmk *.synctex.gz

# Clean all generated files
distclean: clean
	cd $(SLIDES_DIR) && rm -f *.pdf

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