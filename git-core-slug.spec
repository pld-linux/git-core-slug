
%define 	module	git_slug
Summary:	Tools to interact with PLD git repositories
Name:		git-core-slug
Version:	0.5
Release:	1
License:	GPL v2
Group:		Development/Building
Source0:	https://github.com/draenog/slug/tarball/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	abf8a43c5e0759cfa3a2294a839b70e6
URL:		https://github.com/draenog/slug
BuildRequires:	asciidoc
BuildRequires:	docbook-dtd45-xml
BuildRequires:	python3-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	xmlto
Requires:	git-core
Requires:	python3-modules
Suggests:	openssh-clients
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python tools to interact with PLD git repositories.

%prep
%setup -qc
mv draenog-slug-*/* .

%build
%{__python3} setup.py build
%{make} man

%install
rm -rf $RPM_BUILD_ROOT
%{__python3} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%{make} man-install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/git-core
ln -s %{_bindir}/slug.py $RPM_BUILD_ROOT%{_libdir}/git-core/git-pld
echo ".so slug.py.1" > $RPM_BUILD_ROOT%{_mandir}/man1/git-pld.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HOWTO Changelog
%attr(755,root,root) %{_bindir}/slug.py
%{_libdir}/git-core/git-pld
%{_mandir}/man1/*.1*
%{py3_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py3_sitescriptdir}/git_core_slug-*.egg-info
%endif
