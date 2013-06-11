DESTDIR=/usr
DATADIR=$(DESTDIR)/share/langtable
DEBUG=
PWD := $(shell pwd)
SRCDIR=$(PWD)

install:
	perl -pi -e "s,_datadir = '(.*)',_datadir = '$(DATADIR)'," langtable.py
	DISTUTILS_DEBUG=$(DEBUG) python ./setup.py install --prefix=$(DESTDIR) --install-data=$(DATADIR)
	gzip --force --best $(DATADIR)/*.xml

.PHONY: test
test: install
	python langtable.py
	(cd $(DATADIR); python -m doctest $(SRCDIR)/test_cases.txt)
	xmllint --noout --relaxng schemas/keyboards.rng data/keyboards.xml
	xmllint --noout --relaxng schemas/languages.rng data/languages.xml
	xmllint --noout --relaxng schemas/territories.rng data/territories.xml

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
	mock --root $(MOCK_CONFIG) --rebuild ./mockbuild-results/*.src.rpm
	cp /var/lib/mock/$(MOCK_CONFIG)/result/* ./mockbuild-results

.PHONY: review
review: mockbuild
	cp *.spec ./mockbuild-results/
	(cd ./mockbuild-results/; fedora-review -n langtable -m $(MOCK_CONFIG) )
