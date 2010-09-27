%global php_extdir %(php-config --extension-dir 2>/dev/null || echo "undefined")

Summary:       An extension for communicating with Redis database
Name:          php-redis
Version:       2.0.2
Release:       2%{?dist}
License:       BSD
Group:         Development/Languages
URL:           http://github.com/owlient/phpredis
# git clone http://github.com/owlient/phpredis.git phpredis
# GIT_DIR=phpredis/.git git archive --format=tar --prefix=phpredis-2.0.2/ 2.0.2 | bzip2 > phpredis-2.0.2.tar.bz2
Source0:       phpredis-2.0.2.tar.bz2
Source1:       phpredis.ini
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel >= 5.1.0
Obsoletes:     php-phpredis

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}

%description
This extension provides an API for communicating with Redis database, 
a persistent key-value database with built-in net interface written in 
ANSI-C for Posix systems.

%prep
%setup -q -n phpredis-%{version}

%build
phpize
%configure --with-php-config=%{_bindir}/php-config
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install INSTALL_ROOT=$RPM_BUILD_ROOT

%{__install} -D -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/redis.ini

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%doc README.markdown CREDITS
%config(noreplace) %{_sysconfdir}/php.d/redis.ini
%{php_extdir}/redis.so

%changelog
* Mon Sep 27 2010 Timon <timosha@gmail.com> 2.0.2-2
- rename to php-redis

* Fri Sep 24 2010 Timon <timosha@gmail.com> 2.0.2-1
- First release for Fedora

