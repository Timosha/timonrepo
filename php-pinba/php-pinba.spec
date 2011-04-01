#%global gitdate 20100505

Name:           php-pinba
Version:        0.0.6
Release:        1%{?dist}
Summary:        PHP extension to measure particular parts of the code

Group:          Development/Languages
License:        GPLv2
URL:            http://pinba.org/
#Source0:        pinba-%{gitdate}.tar.bz2
Source:         http://pinba.org/files/pinba_extension-%{version}.tgz
Source1:        pinba.ini
# http://pinba.org/files/pinba_engine-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  php-devel >= 5.3, php-pear
BuildRequires:  protobuf-devel

Requires:       php-common >= 5.3
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

%description
This extension is needed to gather and send statistics data and also to manage 
timers. At the request time the extension records time and resource usage and 
at the request shutdown it computes the difference. After that the extension 
creates a protobuf packet and sends it to the server by UDP. 

%prep
%setup -q -n pinba_extension-%{version}

%build
phpize
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}
%{__install} -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/php.d/pinba.ini

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CREDITS README NEWS
%config(noreplace) %{_sysconfdir}/php.d/pinba.ini
%{php_extdir}/pinba.so

%changelog
* Fri Apr 1 2011 Timon <timosha@gmail.com> - 0.0.6-1
- new release

* Thu Jul 22 2010 Timon <timosha@gmail.com> - 0.0.6-0.2220100505git
- git branch

* Mon Jul 19 2010 Timon <timosha@gmail.com> - 0.0.5-2
- protobuf rebuild

* Mon Jul 12 2010 Timon <timosha@gmail.com> - 0.0.5-1
- initial commit

