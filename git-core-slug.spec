%define 	module	git_slug
Summary:	Tools to interact with PLD git repositories
Summary(pl.UTF-8):	Narzędzia do pracy z repozytoriami gita w PLD
Name:		git-core-slug
Version:	0.13.2
Release:	3
License:	GPL v2
Group:		Development/Building
Source0:	https://github.com/draenog/slug/tarball/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a2b8365049b423fd3b332292f031ce0d
Source1:	slug_watch.init
Source2:	crontab
Source3:	slug_watch.sysconfig
Source4:	slug_watch-cron
URL:		https://github.com/draenog/slug
BuildRequires:	asciidoc
BuildRequires:	docbook-dtd45-xml
BuildRequires:	python3-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	xmlto
Requires:	git-core
Requires:	python3-modules
Suggests:	openssh-clients
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python tools to interact with PLD git repositories.

%description -l pl.UTF-8
Narzędzia w Pythonie do pracy z repozytoriami gita w PLD.

%package watch
Summary:	Daemon to update Refs repository for git-slug
Summary(pl.UTF-8):	Demon uaktualniający repozytorium Refs dla git-slug
Group:		Development/Building
Requires:	git-core-slug
Requires:	pld-gitolite
Requires:	python3-pyinotify
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description watch
Daemon to update Refs repository for git-slug. It is to be run on PLD
gitolite server.

%description watch -l pl.UTF-8
Demon uaktualniający repozytorium Refs dla git-slug. Jest przeznaczony
do uruchamiania na serwerze gitolite PLD.

%prep
%setup -qc
mv draenog-slug-*/* .

%build
%{__python3} setup.py build
%{__make} man

%install
rm -rf $RPM_BUILD_ROOT
%{__python3} setup.py install \
	--install-data=/home/services/git \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%{__make} man-install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/git-core
ln -s %{_bindir}/slug.py $RPM_BUILD_ROOT%{_libdir}/git-core/git-pld
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
%doc HOWTO Changelog
%attr(755,root,root) %{_bindir}/slug.py
%{_libdir}/git-core/git-pld
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
%dir /home/services/git
%dir /home/services/git/adc
%dir /home/services/git/adc/bin
%attr(755,git,git) /home/services/git/adc/bin/trash
%attr(755,git,git) /home/services/git/adc/bin/move
%dir /home/services/git/.gitolite/hooks/common/post-receive.python.d
/home/services/git/.gitolite/hooks/common/post-receive.python.d/slug_hook.py
%dir /home/services/git/watchdir
%dir /home/services/git/Refs
