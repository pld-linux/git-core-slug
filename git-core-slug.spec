
%define 	module	git_slug
Summary:	Tools to interact with PLD git repositories
Name:		git-core-slug
Version:	0.1
Release:	1
License:	GPL v2
Group:		Development/Building
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	cb4fad8ff51b95077b5cbd7d5ceb3682
URL:		https://github.com/draenog/slug
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	git-core
Requires:	python-modules
Suggests:	openssh-clients
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python tools to interact with PLD git repositories.

%prep
%setup -q


%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
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
%attr(755,root,root) %{_bindir}/slug.py
%{_libdir}/git-core/git-pld
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/git_core_slug-*.egg-info
%endif
