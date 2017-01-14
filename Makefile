
all: essays
	@mkdir -p output

essays:
	@mkdir -p output/essays; \
	for file in `ls content/essays`; \
	do \
		output=`echo $$file | cut -d '.' -f1`'.html'; \
		pandoc --from markdown --to html5 "content/essays/$$file" -o "output/essays/$$output"; \
	done

clean:
	@rm -rf output
