Name:           lang-table
Version:        0.0.1
Release:        1%{?dist}
Summary:        For guessing reasonable defaults for locale, keyboard, territory, …
Group:          Development/Tools
# the translations in languages.xml and territories.xml are (mostly)
# imported from CLDR and are thus under the Unicode license, the
# short name for this license is "MIT", see:
# https://fedoraproject.org/wiki/Licensing:MIT?rd=Licensing/MIT#Modern_Style_without_sublicense_.28Unicode.29
License:        GPLv3+ and MIT
URL:            https://github.com/mike-fabian/lang-table
Source0:        http://mfabian.fedorapeople.org/lang-table/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-lxml
BuildRequires:  python2-devel

%description
lang-table is used to guess reasonable defaults for locale, keyboard,
territory, …, if part of that information is already known. For
example, guess the territory and the keyboard layout if the language
is known or guess the language and keyboard layout if the territory is
already known.

%package python
Summary:        Python module to query the lang-table-data
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-data = %{version}-%{release}
Requires:       python-lxml

%description python
This package contains a Python module to query the data
from lang-table-data.

%package data
Summary:        Data files for lang-table
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description data
This package contains the data files for lang-table.

%prep
%setup -q

%build
perl -pi -e "s%datadir = '(.*)'%datadir = '%{_datadir}/lang-table'%" langtable.py
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --prefix=%{_prefix} --install-data=%{_datadir}/lang-table --root $RPM_BUILD_ROOT

%check
(cd $RPM_BUILD_DIR/%{name}-%{version}; %{__python} -m doctest test_cases.txt)

%files
%doc README COPYING ChangeLog unicode-license.txt test_cases.txt

%files python
%{python_sitelib}/*

%files data
%{_datadir}/lang-table/*

%changelog
* Tue May 07 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.1-1
- initial package



