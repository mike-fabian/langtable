Name:           langtable
Version:        0.0.8
Release:        1%{?dist}
Summary:        Guessing reasonable defaults for locale, keyboard layout, territory, and language.
Group:          Development/Tools
# the translations in languages.xml and territories.xml are (mostly)
# imported from CLDR and are thus under the Unicode license, the
# short name for this license is "MIT", see:
# https://fedoraproject.org/wiki/Licensing:MIT?rd=Licensing/MIT#Modern_Style_without_sublicense_.28Unicode.29
License:        GPLv3+
URL:            https://github.com/mike-fabian/langtable
Source0:        http://mfabian.fedorapeople.org/langtable/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel

%description
langtable is used to guess reasonable defaults for locale, keyboard layout,
territory, and language, if part of that information is already known. For
example, guess the territory and the keyboard layout if the language
is known or guess the language and keyboard layout if the territory is
already known.

%package python
Summary:        Python module to query the langtable-data
Group:          Development/Tools
License:        GPLv3+
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-data = %{version}-%{release}

%description python
This package contains a Python module to query the data
from langtable-data.

%package data
Summary:        Data files for langtable
Group:          Development/Tools
License:        GPLv3+ and MIT
Requires:       %{name} = %{version}-%{release}

%description data
This package contains the data files for langtable.

%prep
%setup -q

%build
perl -pi -e "s,_datadir = '(.*)',_datadir = '%{_datadir}/langtable'," langtable.py
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --prefix=%{_prefix} --install-data=%{_datadir}/langtable --root $RPM_BUILD_ROOT
gzip --force --best $RPM_BUILD_ROOT/%{_datadir}/langtable/*.xml

%check
(cd $RPM_BUILD_DIR/%{name}-%{version}/data; PYTHONPATH=.. %{__python} -m doctest ../test_cases.txt; %{__python} ../langtable.py)
xmllint --noout --relaxng $RPM_BUILD_ROOT/%{_datadir}/langtable/schemas/keyboards.rng $RPM_BUILD_ROOT/%{_datadir}/langtable/keyboards.xml.gz
xmllint --noout --relaxng $RPM_BUILD_ROOT/%{_datadir}/langtable/schemas/languages.rng $RPM_BUILD_ROOT/%{_datadir}/langtable/languages.xml.gz
xmllint --noout --relaxng $RPM_BUILD_ROOT/%{_datadir}/langtable/schemas/territories.rng $RPM_BUILD_ROOT/%{_datadir}/langtable/territories.xml.gz

%files
%doc README COPYING ChangeLog unicode-license.txt test_cases.txt
%{_datadir}/langtable/schemas

%files python
%{python_sitelib}/*

%files data
%{_datadir}/langtable/*.xml.gz

%changelog
* Tue Jul 30 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.8-1
- Update to 0.0.8
- Add endonym for Maithili
- Return True by default from supports_ascii (by Vratislav Podzimek)
- Add grc, eo, ak, GH, cop, dsb, fj, FJ, haw, hil, la, VA, ln, kg, CD, CG, AO, mos, BF, ny, MW, smj, tet, TL, tpi, PG (Resolves: rhbz#985332 - some language codes are missing)
- Import more translations from CLDR
- Give pa_IN.UTF-8 higher weight than pa_PK.UTF-8 (Resolves: rhbz#986658, rhbz#986155)

* Thu Jul 04 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.7-1
- Update to 0.0.7
- Add examples for list_consolefonts()
- Add a list_timezones() function
- Add functions languageId() and territoryId()
- Fix some translations of language names to get unique results returned by languageId()

* Wed Jun 12 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.6-1
- Update to 0.0.6
- Add RelaxNG schemas for the XML files (Vratislav Podzimek <vpodzime@redhat.com>)
- Use SAX instead of the ElementTree (Vratislav Podzimek <vpodzime@redhat.com>)
- Use 'trName' instead of 'name' for translated names (Vratislav Podzimek <vpodzime@redhat.com>)

* Fri Jun 07 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.5-1
- Update to 0.0.5
- Accept script names as used by glibc locales as well
- Support reading gzipped xml files
- Set ASCII support to “True” for cz and sk keyboard layouts

* Mon May 27 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.4-1
- Update to 0.0.4
- Remove backwards compatibility init() function
- Add ia (Interlingua), see https://bugzilla.redhat.com/show_bug.cgi?id=872423

* Thu May 16 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.3-1
- Update to 0.0.3
- Move the examples from the README to the source code
- Some tweaks for the translation of Serbian
- Prefix all global functions and global variables which are internal with “_”
- Rename country → territory, countries → territories in keyboards.xml
- Add keyboard “in(eng)” and make it the default for all Indian languages
- Add a comment stating which functions should be considered public API
- Add a supports_ascii() function
- Run Python’s doctest also on langtable.py, not only the extra test_cases.txt

* Fri May 10 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.2-1
- update to 0.0.2
- Prefer values for language, script, and territory found in languageId over those found in the other parameters

* Tue May 07 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.1-1
- initial package



