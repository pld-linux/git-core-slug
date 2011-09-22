
%define 	module	git_slug
Summary:	Tools to interact with PLD git repositories
Name:		git-core-slug
Version:	0.4
Release:	1
License:	GPL v2
Group:		Development/Building
Source0:	https://github.com/draenog/slug/tarball/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	58dfd75ae54d346ddbd3e23c1a6b42b0
URL:		https://github.com/draenog/slug
BuildRequires:	python3-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
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

%install
rm -rf $RPM_BUILD_ROOT
%{__python3} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

install -d $RPM_BUILD_ROOT%{_libdir}/git-core
ln -s %{_bindir}/slug.py $RPM_BUILD_ROOT%{_libdir}/git-core/git-pld

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HOWTO Changelog
%attr(755,root,root) %{_bindir}/slug.py
%{_libdir}/git-core/git-pld
%{py3_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py3_sitescriptdir}/git_core_slug-*.egg-info
%endif
