%define		module	git_slug
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Tools to interact with PLD Linux git repositories
Summary(pl.UTF-8):	Narzędzia do pracy z repozytoriami gita w PLD Linuksa
Name:		git-core-slug
Version:	0.20.0
Release:	1
License:	GPL v2
Group:		Development/Building
Source0:	git_core_slug-%{version}.tar.gz
# Source0-md5:	70e14ee38566d13894a4313120a1d6cd
URL:		https://git.pld-linux.org/gitweb.cgi/?p=projects/git-slug.git;a=summary
BuildRequires:	asciidoc
BuildRequires:	docbook-dtd45-xml
BuildRequires:	python3-build
BuildRequires:	python3-hatchling
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
BuildRequires:	xmlto
%if %{with tests}
BuildRequires:	python3-pytest >= 8.0
%endif
Requires:	git-core
Requires:	python3-modules >= 1:3.9
Suggests:	openssh-clients
Suggests:	python3-rpm
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python tools to interact with PLD Linux git repositories.

%description -l pl.UTF-8
Narzędzia w Pythonie do pracy z repozytoriami gita w PLD.

%package watch
Summary:	Daemon to update Refs repository for git-slug
Summary(pl.UTF-8):	Demon uaktualniający repozytorium Refs dla git-slug
Group:		Development/Building
Requires(post,preun):	/sbin/chkconfig
Requires:	git-core-slug
Requires:	pld-gitolite
Requires:	python3-pyinotify
Requires:	rc-scripts
Suggests:	crondaemon

%description watch
Daemon to update Refs repository for git-slug. It is to be run on PLD
gitolite server.

%description watch -l pl.UTF-8
Demon uaktualniający repozytorium Refs dla git-slug. Jest przeznaczony
do uruchamiania na serwerze gitolite PLD.

%prep
%setup -q -n git_core_slug-%{version}

%build
%py3_build_pyproject
%{__make} man

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests --ignore=tests/test_benchmark.py
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py3_install_pyproject

%{__make} man-install \
	DESTDIR=$RPM_BUILD_ROOT

echo ".so slug.1" > $RPM_BUILD_ROOT%{_mandir}/man1/git-pld.1

install -p server/slug_watch/slug_watch $RPM_BUILD_ROOT%{_bindir}/slug_watch
install -p server/slug_watch/slug_watch-cron $RPM_BUILD_ROOT%{_bindir}/slug_watch-cron

install -Dp server/slug_watch/slug_watch.init $RPM_BUILD_ROOT/etc/rc.d/init.d/slug_watch
install -Dp server/slug_watch/slug_watch.service $RPM_BUILD_ROOT%{systemdunitdir}/slug_watch.service
install -Dp server/slug_watch/crontab $RPM_BUILD_ROOT/etc/cron.d/slug_watch
install -Dp server/slug_watch/slug_watch.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/slug_watch

install -d $RPM_BUILD_ROOT/home/services/git/adc/bin
install -p server/adc/trash server/adc/move $RPM_BUILD_ROOT/home/services/git/adc/bin
ln -s move $RPM_BUILD_ROOT/home/services/git/adc/bin/copy

install -d $RPM_BUILD_ROOT/home/services/git/.gitolite/hooks/common/post-receive.python.d
install -p server/hooks/post-receive $RPM_BUILD_ROOT/home/services/git/.gitolite/hooks/common
install -p server/hooks/slug_hook.py $RPM_BUILD_ROOT/home/services/git/.gitolite/hooks/common/post-receive.python.d

install -d $RPM_BUILD_ROOT/home/services/git/{watchdir,Refs}

%clean
rm -rf $RPM_BUILD_ROOT

%post watch
/sbin/chkconfig --add slug_watch
%service slug_watch restart
%systemd_post slug_watch.service

%preun watch
if [ "$1" = "0" ]; then
	%service -q slug_watch stop
	/sbin/chkconfig --del slug_watch
fi
%systemd_preun slug_watch.service

%postun watch
%systemd_postun_with_restart slug_watch.service

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/git-pld
%{_mandir}/man1/git-pld.1*
%{_mandir}/man1/slug.1*
%{py3_sitescriptdir}/slug.py
%{py3_sitescriptdir}/__pycache__/slug.cpython-*.py[co]
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/git_core_slug-%{version}.dist-info

%files watch
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/slug_watch
%attr(755,root,root) %{_bindir}/slug_watch-cron
%attr(754,root,root) /etc/rc.d/init.d/slug_watch
%{systemdunitdir}/slug_watch.service
%config(noreplace) %verify(not md5 mtime size) /etc/cron.d/slug_watch
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/slug_watch
%{_mandir}/man1/slug_watch.1*

%defattr(644,git,git,755)
%attr(755,git,git) /home/services/git/adc/bin/trash
%attr(755,git,git) /home/services/git/adc/bin/move
/home/services/git/adc/bin/copy
%attr(755,git,git) /home/services/git/.gitolite/hooks/common/post-receive
%dir /home/services/git/.gitolite/hooks/common/post-receive.python.d
/home/services/git/.gitolite/hooks/common/post-receive.python.d/slug_hook.py
%dir /home/services/git/watchdir
%dir /home/services/git/Refs
