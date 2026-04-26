srpm:
	curl -fsSL -o $(outdir)/source.tar.gz $$(grep -m1 '^Source0:' $(spec) | awk '{print $$2}')
	rpmbuild -bs $(spec) --define "_sourcedir $(outdir)" --define "_srcrpmdir $(outdir)"
