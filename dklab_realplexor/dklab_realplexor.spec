Summary:	Comet server which handles 1000000+ parallel browser connections
Name:		dklab_realplexor
Version:	1.40
Release:	1%{?dist}
Group:		Development/Libraries
License:	GPLv2
URL:		http://dklab.ru/lib/dklab_realplexor/
# git clone http://github.com/DmitryKoterov/dklab_realplexor.git dklab_realplexor
# GIT_DIR=dklab_realplexor/.git git archive --format=tar --prefix=dklab_realplexor-1.32/ 1e7a3236affeeeaf42068f166540f42b0c1708b9 | bzip2 > dklab_realplexor-1.32.tar.bz2
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}.sysconfig

Requires:	perl-EV

Requires(post):		/sbin/chkconfig
Requires(preun):	/sbin/chkconfig
Requires(preun):	/sbin/service
Requires(postun):	/sbin/service

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
%setup -q -n %{name}-%{version}

#%build

%install
%{__rm} -rf %{buildroot}
#%{__make} DESTDIR=%{buildroot} install
#%{__install} -d -m 755 %{buildroot}%{sysconfig}
%{__install} -D -m 644 dklab_realplexor.conf %{buildroot}%{_sysconfdir}/%{name}.conf
%{__install} -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -D -m 755 dklab_realplexor.init %{buildroot}%{_initddir}/%{name}

%{__install} -D -d -m 755 %{buildroot}%{_datadir}/%{name}
%{__cp} -r Connection Storage Tie Realplexor dklab_realplexor.pl %{buildroot}%{_datadir}/%{name}
%{__install} -D -m 755 dklab_realplexor.pl %{buildroot}%{_datadir}/%{name}/dklab_realplexor.pl

%{__install} -D -m 644 dklab_realplexor.html %{buildroot}%{_datadir}/%{name}/dklab_realplexor.html
%{__install} -D -m 644 dklab_realplexor.js %{buildroot}%{_datadir}/%{name}/dklab_realplexor.js
%{__install} -D -m 644 dklab_realplexor.htpasswd %{buildroot}%{_datadir}/%{name}/dklab_realplexor.htpasswd

%{__install} -D -d -m 755 %{buildroot}%{_datadir}/php
%{__cp} -r api/php/Dklab %{buildroot}%{_datadir}/php


#TODO
#%check 
#%{__make} test

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
        /sbin/service %{name} stop >/dev/null 2>&1
        /sbin/chkconfig --del %{name}
fi


%postun
if [ "$1" -ge "1" ]; then
        /sbin/service %{name} condrestart >/dev/null 2>&1
fi


%files
%defattr(-,root,root)
%doc dklab_realplexor.license-gpl-2.0.txt dklab_realplexor.license-additional.txt
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_initddir}/%{name}
%{_datadir}/%{name}

%files -n php-dklab_realplexor
%defattr(-,root,root)
%{_datadir}/php/Dklab/Realplexor.php

%changelog
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

