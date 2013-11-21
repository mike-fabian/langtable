%if 0%{?fedora}
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

Name:           langtable
Version:        0.0.21
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
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif # if with_python3

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

%if 0%{?with_python3}
%package python3
Summary:        Python module to query the langtable-data
Group:          Development/Tools
License:        GPLv3+
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-data = %{version}-%{release}

%description python3
This package contains a Python module to query the data
from langtable-data.

%endif # with_python3

%package data
Summary:        Data files for langtable
Group:          Development/Tools
License:        GPLv3+ and MIT
Requires:       %{name} = %{version}-%{release}

%description data
This package contains the data files for langtable.

%prep
%setup -q

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
perl -pi -e "s,_datadir = '(.*)',_datadir = '%{_datadir}/langtable'," langtable.py
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
perl -pi -e "s,_datadir = '(.*)',_datadir = '%{_datadir}/langtable'," langtable.py
%{__python3} setup.py build
popd
%endif # with_python3

%install
%{__python} setup.py install --skip-build --prefix=%{_prefix} --install-data=%{_datadir}/langtable --root $RPM_BUILD_ROOT
gzip --force --best $RPM_BUILD_ROOT/%{_datadir}/langtable/*.xml

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --prefix=%{_prefix} --install-data=%{_datadir}/langtable --root $RPM_BUILD_ROOT
popd
# the .xml files copied by the “python3 setup.py install” are identical
# to those copied in the “python2 setup.py install”,
# it does not hurt to gzip them again:
gzip --force --best $RPM_BUILD_ROOT/%{_datadir}/langtable/*.xml
%endif # with_python3

%check
(cd $RPM_BUILD_DIR/%{name}-%{version}/data; PYTHONPATH=.. %{__python} ../test_cases.py; %{__python} ../langtable.py)
%if 0%{?with_python3}
(cd $RPM_BUILD_DIR/%{name}-%{version}/data; LC_CTYPE=en_US.UTF-8 PYTHONPATH=.. %{__python3} ../test_cases.py; %{__python3} ../langtable.py)
%endif # with_python3
xmllint --noout --relaxng $RPM_BUILD_ROOT/%{_datadir}/langtable/schemas/keyboards.rng $RPM_BUILD_ROOT/%{_datadir}/langtable/keyboards.xml.gz
xmllint --noout --relaxng $RPM_BUILD_ROOT/%{_datadir}/langtable/schemas/languages.rng $RPM_BUILD_ROOT/%{_datadir}/langtable/languages.xml.gz
xmllint --noout --relaxng $RPM_BUILD_ROOT/%{_datadir}/langtable/schemas/territories.rng $RPM_BUILD_ROOT/%{_datadir}/langtable/territories.xml.gz

%files
%doc README COPYING ChangeLog unicode-license.txt test_cases.py
%{_datadir}/langtable/schemas

%files python
%{python_sitelib}/*

%if 0%{?with_python3}
%files python3
%{python3_sitelib}/*
%endif # with_python3

%files data
%{_datadir}/langtable/*.xml.gz

%changelog
* Thu Nov 21 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.21-1
- Make America/New_York the highest ranked timezone for US and yi (Resolves: rhbz#1031319)

* Wed Nov 20 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.20-1
- add entries for several layouts known to be non-ASCII by systemd/s-c-k (patch by Adam Williamson)

* Mon Nov 11 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.19-1
- Add SS
- More translations for anp from CLDR
- Add information about default input methods and a query function

* Mon Nov 04 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.18-1
- Add anp
- Do not fail if a timezone id part cannot be found in the database (Vratislav Podzimek reported that error)

* Tue Oct 22 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.17-1
- Add “be(oss)” as a possible keyboard layout for language nl (Resolves: rhbz#885345)

* Tue Oct 08 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.16-1
- Make it work with python3 (and keep it working with python2) (Resolves: rhbz#985317)

* Mon Sep 16 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.15-1
- Update to 0.0.15
- Add keyboards "ara", "ara(azerty)", "iq", and "sy" (Resolves: rhbz#1008389)

* Sun Sep 15 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.14-1
- Update to 0.0.14
- add some more languages: ay, ayc, ayr, niu, szl, nhn
- make languageId() work even if the name of the language or the territory contain spaces (Resolves: rhbz#1006718)
- Add the default script if not specified in queries for Chinese
- Import improved translations from CLDR
- Always return the territory name as well if queried in language_name()
- Add timezones.xml and timezoneidparts.xml to be able to offer translations for timezone ids
- Import translations for timezone cities from CLDR
- Add some more territories and translations
- test cases for timezone id translations

* Thu Sep 05 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.13-1
- Update to 0.0.13
- Serbian keyboards are 'rs' not 'sr' (by Vratislav Podzimek)

* Wed Aug 28 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.12-1
- Update to 0.0.12
- Match case insensitively in languageId() (Resolves: rhbz#1002000 (case insensitive languageId function needed))

* Mon Aug 19 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.11-1
- Update to 0.0.11
- Add translations for DE and NL territories in nds (reported by Vratislav Podzimek)

* Tue Aug 13 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.10-1
- Update to 0.0.10
- Add translations for Belarusian and Belarus in Latin script (reported by Vratislav Podzimek)

* Sat Aug 03 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.9-1
- Update to 0.0.9
- Add endonyms for pa_Arab (and pa_PK) and translation of country name for Pakistan for pa_Arab
- make languageId() return something even if a language name like "language (territory)" is given (Resolves: rhbz#986659 - some language name to its locale code failed)

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



