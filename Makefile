DESTDIR=/usr
DATADIR=$(DESTDIR)/share/langtable
DEBUG=
PWD := $(shell pwd)
SRCDIR=$(PWD)

install:
	perl -pi -e "s%datadir = '(.*)'%datadir = '$(DATADIR)'%" langtable.py
	DISTUTILS_DEBUG=$(DEBUG) python ./setup.py install --prefix=$(DESTDIR) --install-data=$(DATADIR)

.PHONY: test-local
test-local:
	(cd data/; PYTHONPATH=.. python -m doctest ../test_cases.txt)

.PHONY: test
test:
	(cd $(DATADIR); python -m doctest $(SRCDIR)/test_cases.txt)

.PHONY: dist
dist:
	DISTUTILS_DEBUG=$(DEBUG) python ./setup.py sdist

.PHONY: clean
clean:
	git clean -dxf

MOCK_CONFIG=fedora-rawhide-x86_64
.PHONY: mockbuild
mockbuild: dist
	mkdir -p ./mockbuild-results/
	mock --root $(MOCK_CONFIG) --buildsrpm --spec langtable.spec --sources ./dist/
	cp /var/lib/mock/$(MOCK_CONFIG)/result/* ./mockbuild-results
	mock --rebuild ./mockbuild-results/*.src.rpm
	cp /var/lib/mock/$(MOCK_CONFIG)/result/* ./mockbuild-results

.PHONY: review
review: mockbuild
	cp *.spec ./mockbuild-results/
	(cd ./mockbuild-results/; fedora-review -n langtable -m $(MOCK_CONFIG) )
