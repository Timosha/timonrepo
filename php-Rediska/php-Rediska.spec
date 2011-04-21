%global		realname	Rediska
%global		realversion	0-5-5

Name:		php-Rediska
Summary:	PHP client for Redis
Version:        0.5.5
Release:        1%{?dist}

Source0:        http://rediska.geometria-lab.ru/download/%{realname}-%{realversion}.zip
URL:            http://rediska.geometria-lab.ru/
License:        BSD
Group:          Development/Libraries

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       php

%description
PHP client for redis with features:
 * Multiple servers support
 * Consistent hashing, crc32 or you personal algorythm for key distribution
 * Working with keys as objects
 * Use Lists, Sets, Sorted sets and Hashes as native PHP arrays
 * Transactions
 * Publish/Subscribe
 * Pipelining
 * Easy extending Rediska by adding you own commands or overwrite standart
 * Zend Framework integration
 * Symfony framework integration
 * Full documentation
 * Example application
 * PHPUnit tests

%prep
%setup -qn "%{realname} %{version}"

%build
# empty build section, nothing required

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__install} -D library/Rediska.php $RPM_BUILD_ROOT%{_datadir}/php/Rediska.php
%{__cp} -r library/Rediska $RPM_BUILD_ROOT%{_datadir}/php/


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc CHANGELOG.txt LICENSE.txt README.markdown
%doc docs
%doc tests scripts examples benchmarks
%{_datadir}/php/Rediska
%{_datadir}/php/%{realname}.php

%changelog
* Wed Mar 02 2011 Timon <timosha@gmail.com> 0.5.5-1
- Update to 0.5.5
- full changelog https://github.com/Shumkov/Rediska/commit/8de826f95b5321b0de8d0b8574cdd83c3735ac84

* Mon Nov 01 2010 Timon <timosha@gmail.com> 0.5.1-1
- Implemented ZCOUNT
- Added append and substring commands to Rediska_Key
- Added setAndExpire command to Rediska_Key
- Fixed warnings about empty namespace
- Fixed GET parameter in sort command

* Thu Sep 16 2010 Timon <timosha@gmail.com> 0.5.0-1
- first rpm release
