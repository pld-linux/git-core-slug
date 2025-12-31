%define 	module	git_slug
Summary:	Tools to interact with PLD Linux git repositories
Summary(pl.UTF-8):	Narzędzia do pracy z repozytoriami gita w PLD Linuksa
Name:		git-core-slug
Version:	0.15
Release:	1
License:	GPL v2
Group:		Development/Building
Source0:	%{name}-%{version}.tar.xz
# Source0-md5:	6cdb2ba9c6d0270c68160ec57bc2bfae
URL:		https://git.pld-linux.org/gitweb.cgi/?p=projects/git-slug.git;a=summary
BuildRequires:	asciidoc
BuildRequires:	docbook-dtd45-xml
BuildRequires:	git-core >= 2.7.1-3
BuildRequires:	python3-modules >= 1:3.3.0
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	xmlto
Requires:	git-core
Requires:	python3-modules
Suggests:	openssh-clients
Suggests:	python3-rpm
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		gitcoredir	%(git --exec-path)

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
%setup -q

%build
%py3_build
%{__make} man

%install
rm -rf $RPM_BUILD_ROOT
%py3_install \
	--install-data=/home/services/git \

%{__make} man-install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{gitcoredir}
ln -s %{_bindir}/slug.py $RPM_BUILD_ROOT%{gitcoredir}/git-pld
echo ".so slug.py.1" > $RPM_BUILD_ROOT%{_mandir}/man1/git-pld.1

install -Dp watch/slug_watch.init $RPM_BUILD_ROOT/etc/rc.d/init.d/slug_watch
install -d $RPM_BUILD_ROOT/home/services/git/.gitolite/hooks/common
cp -rp post-receive.python.d $RPM_BUILD_ROOT/home/services/git/.gitolite/hooks/common
install -d $RPM_BUILD_ROOT/home/services/git/{watchdir,Refs}
touch $RPM_BUILD_ROOT/home/services/git/{watchdir,Refs}

install -Dp watch/crontab $RPM_BUILD_ROOT/etc/cron.d/slug_watch
install -Dp watch/slug_watch.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/slug_watch
install -Dp watch/slug_watch-cron $RPM_BUILD_ROOT%{_bindir}

install -Dp watch/slug_watch.service $RPM_BUILD_ROOT%{systemdunitdir}/slug_watch.service

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
%doc HOWTO
%attr(755,root,root) %{_bindir}/slug.py
%{gitcoredir}/git-pld
%{_mandir}/man1/git-pld.1*
%{_mandir}/man1/slug.py.1*
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/git_core_slug-*.egg-info

%files watch
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/slug_watch
%attr(755,root,root) %{_bindir}/slug_watch-cron
%attr(754,root,root) /etc/rc.d/init.d/slug_watch
%{systemdunitdir}/slug_watch.service
%config(noreplace) %verify(not md5 mtime size) /etc/cron.d/slug_watch
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/slug_watch
%{py3_sitescriptdir}/Daemon

%defattr(644,git,git,755)
%attr(755,git,git) /home/services/git/adc/bin/trash
%attr(755,git,git) /home/services/git/adc/bin/move
/home/services/git/adc/bin/copy
%dir /home/services/git/.gitolite/hooks/common/post-receive.python.d
/home/services/git/.gitolite/hooks/common/post-receive.python.d/slug_hook.py
%dir /home/services/git/watchdir
%dir /home/services/git/Refs
