index.html : README.md docs/style.html makefile
	pandoc \
	--include-in-header docs/style.html \
	--template docs/template.html \
	--email-obfuscation references \
	--bibliography docs/bibliography.json \
	--metadata link-citations \
	--filter pandoc-citeproc \
	--filter pandoc-scholar.py \
	$< > $@
