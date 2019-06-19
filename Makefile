DESTDIR=/usr
DATADIR=$(DESTDIR)/share/langtable/
DEBUG=
PWD := $(shell pwd)
SRCDIR=$(PWD)

.PHONY: gzip
gzip:
	gzip --keep --force --best langtable/data/*.xml

.PHONY: test
test: gzip
	(cd langtable; python2 langtable.py)
	(cd langtable; python3 langtable.py)
	python2 test_cases.py
	python3 test_cases.py
	(cd langtable; xmllint --noout --relaxng schemas/keyboards.rng data/keyboards.xml.gz)
	(cd langtable; xmllint --noout --relaxng schemas/languages.rng data/languages.xml.gz)
	(cd langtable; xmllint --noout --relaxng schemas/territories.rng data/territories.xml.gz)
	(cd langtable; xmllint --noout --relaxng schemas/timezones.rng data/timezones.xml.gz)
	(cd langtable; xmllint --noout --relaxng schemas/timezoneidparts.rng data/timezoneidparts.xml.gz)

.PHONE: check
check: test

.PHONY: dist
dist: gzip
	DISTUTILS_DEBUG=$(DEBUG) python3 ./setup.py sdist bdist_egg bdist_wheel

.PHONY: install
install: dist
	perl -pi -e "s,_datadir = '(.*)',_DATADIR = '$(DATADIR)'," langtable/langtable.py
	DISTUTILS_DEBUG=$(DEBUG) python3 ./setup.py install --prefix=$(DESTDIR)
#	DISTUTILS_DEBUG=$(DEBUG) python3 ./setup.py install_data --install-dir=$(DATADIR)

# check it here: https://test.pypi.org/manage/project/langtable/releases/
.PHONY: twine-upload-test
twine-upload-test: dist
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# check it here: https://pypi.org/manage/project/langtable/releases/
.PHONY: twine-upload
twine-upload: dist
	python3 -m twine upload dist/*

.PHONY: pip-install-test
pip-install-test:
	(cd /tmp; python3 -m pip install --user --ignore-installed --index-url https://test.pypi.org/simple/ --no-deps langtable)

.PHONY: pip-install
pip-install:
	(cd /tmp; python3 -m pip install --user --ignore-installed --no-deps langtable)

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
