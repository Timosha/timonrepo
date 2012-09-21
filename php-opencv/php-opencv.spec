%global ext_name   opencv
%global gitver     03f7f46

Summary:       Extension to access the OpenCV library
Name:          php-%{ext_name}
Version:       1.0
Release:       2.git%{gitver}%{?dist}
License:       PHP
Group:         Development/Languages
URL:           https://github.com/Timosha/OpenCV-for-PHP

# wget https://nodeload.github.com/Timosha/OpenCV-for-PHP/zipball/master
Source0:       Timosha-OpenCV-for-PHP-%{gitver}.zip

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel opencv-devel

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}
Requires:      opencv

# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}

%description
This extension provides a PHP implementation of the OpenCV library.

%prep
%setup -q -c 

# rename source folder
mv -n Timosha-OpenCV-for-PHP-%{gitver} nts

%{__cat} > %{ext_name}.ini << 'EOF'
; Enable %{ext_name} extension module
extension = %{ext_name}.so
EOF
sed -i 's/\r//' nts/CREDITS

%build
cd nts
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
# Install the NTS stuff
make -C nts install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ext_name}.ini %{buildroot}%{_sysconfdir}/php.d/%{ext_name}.ini

%files
%doc nts/CREDITS
%config(noreplace) %{_sysconfdir}/php.d/%{ext_name}.ini
%{php_extdir}/%{ext_name}.so

%changelog
* Fri Sep 21 2012 Timon <timosha@gmail.com> 1.0.0-2
- get source from git
- some changes from php-redis.spec
- build with 5.4

* Tue Sep 11 2012 Dmitriy Degtyaryov <degtyaryov@gmail.com> 1.0.0-1
- Initial package
