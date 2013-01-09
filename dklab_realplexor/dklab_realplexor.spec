#TODO: split into dklab_realplexor-cpp and dklab_realplexor-perl

%global git     2234f5e
%global gituser Timosha
%global github  %{gituser}-dklab_realplexor

Summary:	Comet server which handles 1000000+ parallel browser connections
Name:		dklab_realplexor
Version:	1.41
Release:	0.6.git%{git}%{?dist}
Group:		Development/Libraries
License:	GPLv2
#Source0:	%{name}-%{version}.tar.bz2
Source0:        https://github.com/%{gituser}/dklab_realplexor/tarball/master/%{github}-%{git}.tar.gz
Source1:	%{name}.service

Requires:	perl-EV
Requires:       libev boost-system boost-regex boost-filesystem

# pre/post stuff needs systemd too
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

Requires(post):   chkconfig

BuildRequires: boost-devel libev-devel pkgconfig

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Comet server which handles 1000000+ parallel browser connections.

%package -n php-dklab_realplexor
Summary:	PHP bindings for Dklab Realplexor
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	php

%description -n php-dklab_realplexor
PHP bindings for Dklab Realplexor

%prep
%setup -q -n %{github}-%{git}

%build
pushd cpp/src 
g++ -std=c++11 dklab_realplexor.cpp \
	-lpthread -lcrypt -lboost_filesystem -lboost_system -lboost_regex \
	$(pkg-config --libs --cflags libev) \
        -Wno-strict-aliasing \
	-o ../../dklab_realplexor
popd

%install
%{__rm} -rf %{buildroot}
%{__install} -Dp -m 644 dklab_realplexor.conf %{buildroot}%{_sysconfdir}/%{name}.conf
%{__install} -Dp -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%{__install} -Dp -d -m 755 %{buildroot}%{_datadir}/%{name}
%{__cp} -r Connection Storage Tie Realplexor dklab_realplexor.pl %{buildroot}%{_datadir}/%{name}
%{__install} -Dp -m 644 dklab_realplexor.conf %{buildroot}%{_datadir}/%{name}/dklab_realplexor.conf
%{__install} -Dp -m 755 dklab_realplexor.pl %{buildroot}%{_datadir}/%{name}/dklab_realplexor.pl

#TODO: copy to bindir
%{__install} -Dp -m 755 dklab_realplexor %{buildroot}%{_datadir}/%{name}/dklab_realplexor

%{__install} -Dp -m 644 dklab_realplexor.html %{buildroot}%{_datadir}/%{name}/dklab_realplexor.html
%{__install} -Dp -m 644 dklab_realplexor.js %{buildroot}%{_datadir}/%{name}/dklab_realplexor.js
%{__install} -Dp -m 644 dklab_realplexor.htpasswd %{buildroot}%{_datadir}/%{name}/dklab_realplexor.htpasswd

%{__install} -Dp -d -m 755 %{buildroot}%{_datadir}/php
%{__cp} -r api/php/Dklab %{buildroot}%{_datadir}/php

#TODO
#%check 
#%{__make} test

%post
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 || :
    /bin/systemctl stop %{name}.service >/dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc dklab_realplexor.license-gpl-2.0.txt dklab_realplexor.license-additional.txt
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_datadir}/%{name}

%files -n php-dklab_realplexor
%defattr(-,root,root)
%{_datadir}/php/Dklab/Realplexor.php

%changelog
* Wed Jan 9 2013 Timon <timosha@gmail.com> - 1.41-0.6.git6e97dc5
- switch to systemd

* Tue Dec 25 2012 Timon <timosha@gmail.com> - 1.41-0.5.git6e97dc5
- fix build for gcc 4.7
- using Timosha repo
- remove ev++ patch

* Thu Jan 26 2012 Timon <timosha@gmail.com> - 1.41-0.4.git0b59237
- rebuild new version

* Thu Jan 26 2012 Timon <timosha@gmail.com> - 1.41-0.3.gitb9f4277
- default config

* Wed Jan 25 2012 Timon <timosha@gmail.com> - 1.41-0.2.gitb9f4277
- git version
- cpp version of server

* Thu Oct 10 2011 Timon <timosha@gmail.com> - 1.40-1
- new version

* Thu Oct 28 2010 Timon <timosha@gmail.com> - 1.32-2
- config noreplace

* Mon Sep 06 2010 Timon <timosha@gmail.com> - 1.32-1
- new upstream release

* Mon Aug 9 2010 Timon <timosha@gmail.com> - 1.31-2
- php-dklab_realplexor

* Thu Aug 5 2010 Timon <timosha@gmail.com> - 1.31-1
- first build for Fedora

