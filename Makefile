.phony: build drafts deploydry deployreal

build:
	@echo 'Build hugo site'
	@hugo

drafts:
	echo 'local server, with draft posts'
	@hugo server -D

deploydry:
	@hugo
	@hugo deploy --dryRun -v

deployreal:
	@hugo
	@hugo deploy -v
