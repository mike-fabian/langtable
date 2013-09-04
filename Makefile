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
	xmllint --noout --relaxng $(DATADIR)/schemas/keyboards.rng $(DATADIR)/keyboards.xml.gz
	xmllint --noout --relaxng $(DATADIR)/schemas/languages.rng $(DATADIR)/languages.xml.gz
	xmllint --noout --relaxng $(DATADIR)/schemas/territories.rng $(DATADIR)/territories.xml.gz
	xmllint --noout --relaxng $(DATADIR)/schemas/timezones.rng $(DATADIR)/timezones.xml.gz
	xmllint --noout --relaxng $(DATADIR)/schemas/timezoneidparts.rng $(DATADIR)/timezoneidparts.xml.gz

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

# .rnc files for editing with Emacs
# https://fedoraproject.org/wiki/How_to_use_Emacs_for_XML_editing
%.rnc: %.rng
	trang $< $@

rnc: schemas/keyboards.rnc schemas/languages.rnc schemas/territories.rnc schemas/timezones.rnc schemas/timezoneidparts.rnc
	cp schemas/*.rnc data/
