Summary:	Simple server for running CGI applications over FastCGI
Name:		fcgiwrap
Version:	1.0.3
Release:	1%{?dist}
License:	BSD
Group:		Applications/Internet
URL:		http://nginx.localdomain.pl/wiki/FcgiWrap
# git clone http://github.com/gnosek/fcgiwrap.git
# GIT_DIR=fcgiwrap/.git git archive --format=tar --prefix=fcgiwrap-1.0.3/ 1.0.3 | bzip2 > fcgiwrap-1.0.3.tar.bz2
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	fcgi-devel

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
#%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%{__install} -D -m 0755 fcgiwrap %{buildroot}%{_bindir}/fcgiwrap

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.rst
%{_bindir}/fcgiwrap

%changelog
* Thu Sep 2 2010 Timon <timosha@gmail.com> - 1.0.3-1
- Initial RPM packaging

