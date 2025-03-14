%define 	module	git_slug
Summary:	Tools to interact with PLD Linux git repositories
Summary(pl.UTF-8):	Narzędzia do pracy z repozytoriami gita w PLD Linuksa
Name:		git-core-slug
Version:	0.14
Release:	5
License:	GPL v2
Group:		Development/Building
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	94d40c83999c0ea1d085fb436beede19
Source1:	slug_watch.init
Source2:	crontab
Source3:	slug_watch.sysconfig
Source4:	slug_watch-cron
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

install -Dp %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/slug_watch
install -d $RPM_BUILD_ROOT/home/services/git/.gitolite/hooks/common
cp -rp post-receive.python.d $RPM_BUILD_ROOT/home/services/git/.gitolite/hooks/common
install -d $RPM_BUILD_ROOT/home/services/git/{watchdir,Refs}
touch $RPM_BUILD_ROOT/home/services/git/{watchdir,Refs}

install -Dp %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.d/slug_watch
install -Dp %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/slug_watch
install -Dp %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post watch
/sbin/chkconfig --add slug_watch
%service slug_watch restart

%preun watch
if [ "$1" = "0" ]; then
	%service -q slug_watch stop
	/sbin/chkconfig --del slug_watch
fi

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
