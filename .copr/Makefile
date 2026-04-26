srpm:
	spectool -g $(spec)
	rpmbuild -bs $(spec) --define "_sourcedir $(CURDIR)" --define "_srcrpmdir $(outdir)"
