# Master Makefile for ML Teaching Repository
TOPICS = basics maths supervised unsupervised neural-networks advanced optimization

# Default target - build all topics
all:
	@for topic in $(TOPICS); do \
		echo "Building $$topic..."; \
		$(MAKE) -C $$topic all; \
	done

# Build specific topic
basics maths supervised unsupervised neural-networks advanced:
	$(MAKE) -C $@ all

# Clean all topics
clean:
	@for topic in $(TOPICS); do \
		echo "Cleaning $$topic..."; \
		$(MAKE) -C $$topic clean; \
	done

# Clean all generated files
distclean:
	@for topic in $(TOPICS); do \
		echo "Deep cleaning $$topic..."; \
		$(MAKE) -C $$topic distclean; \
	done

# Deploy all PDFs to slides directory
deploy:
	@for topic in $(TOPICS); do \
		echo "Deploying $$topic..."; \
		$(MAKE) -C $$topic deploy; \
	done

# Show status of all topics
status:
	@for topic in $(TOPICS); do \
		echo "=== $$topic ==="; \
		$(MAKE) -C $$topic status; \
		echo; \
	done

# Build and deploy (useful for Quarto)
build-deploy: all deploy

# Watch for changes (requires entr)
watch:
	@echo "Watching for LaTeX file changes..."
	@find . -name "*.tex" | entr -r make build-deploy

.PHONY: all clean distclean deploy status build-deploy watch $(TOPICS)