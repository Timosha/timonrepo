Summary:	Simple server for running CGI applications over FastCGI
Name:		fcgiwrap
Version:	1.0.3
Release:	5%{?dist}
License:	BSD
Group:		Applications/Internet
URL:		http://nginx.localdomain.pl/wiki/FcgiWrap
# git clone http://github.com/gnosek/fcgiwrap.git
# GIT_DIR=fcgiwrap/.git git archive --format=tar --prefix=fcgiwrap-1.0.3/ 1.0.3 | bzip2 > fcgiwrap-1.0.3.tar.bz2
Source0:	%{name}-%{version}.tar.bz2
Source1:        %{name}.init
Source2:        %{name}.sysconfig
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       fcgi
Requires:       spawn-fcgi
# for usernames
Requires:       httpd 

BuildRequires:	fcgi-devel
BuildRequires:	autoconf automake

%description
fcgiwrap is a simple server for running CGI applications over FastCGI.
It hopes to provide clean CGI support to Nginx (and other web servers 
that may need it). 
Features:
 - very lightweight (84KB of private memory per instance)
 - fixes broken CR/LF in headers
 - handles environment in a sane way 
 - no configuration, so you can run several sites off the same fcgiwrap pool
 - passes CGI stderr output to fcgiwrap's stderr 
Limitations:
 - only one request at a time (but it's cheap to run a bunch of them)
 - passes the whole request to CGI before reading the reply 

%prep
%setup -q 
#-n %{name}-%{version}

%build
autoreconf -i
%configure 
%{__make} %{?_smp_mflags}

%install
%{__install} -D -m 0755 fcgiwrap %{buildroot}%{_bindir}/fcgiwrap
%{__install} -Dp -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/fcgiwrap
%{__install} -Dp -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/fcgiwrap

%preun
if [ $1 = 0 ]; then
        /sbin/service %{name} stop >/dev/null 2>&1
        /sbin/chkconfig --del %{name}
fi

%post
/sbin/chkconfig --add %{name}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.rst
%config(noreplace)%{_sysconfdir}/sysconfig/%{name}
%{_sysconfdir}/init.d/%{name}
%{_bindir}/%{name}


%changelog
* Thu Dec 16 2010 Timon <timosha@gmail.com> - 1.0.3-5
- Add init script

* Thu Sep 2 2010 Timon <timosha@gmail.com> - 1.0.3-1
- Initial RPM packaging

