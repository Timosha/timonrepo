%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

%global pecl_name memcached
#global gitver    1736623

Summary:      Extension to work with the Memcached caching daemon
Name:         php-pecl-memcached
Version:      2.0.0
%if 0%{?gitver:1}
Release:      0.1.git%{gitver}%{?dist}
Source:       php-memcached-dev-php-memcached-v2.0.0b2-14-g%{gitver}.tar.gz
%else
Release:      1%{?dist}
Source:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
%endif
# memcached is PHP, FastLZ is MIT
License:      PHP and MIT
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}

# 5.2.10 required to HAVE_JSON enabled
BuildRequires: php-devel >= 5.2.10
BuildRequires: php-pear
BuildRequires: php-pecl-igbinary-devel
BuildRequires: libmemcached-devel
BuildRequires: zlib-devel
BuildRequires: cyrus-sasl-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:     php-common%{?_isa} >= 5.2.10
Requires:     php-pecl-igbinary%{?_isa}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}

Provides:     php-pecl(%{pecl_name}) = %{version}-%{release}
Provides:     php-pecl(%{pecl_name})%{?_isa} = %{version}-%{release}


# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$


%description
This extension uses libmemcached library to provide API for communicating
with memcached servers.

memcached is a high-performance, distributed memory object caching system,
generic in nature, but intended for use in speeding up dynamic web 
applications by alleviating database load.

It also provides a session handler (memcached). 


%prep 
%setup -c -q

%if 0%{?gitver:1}
mv php-memcached-dev-php-memcached-%{gitver}/package.xml .
mv php-memcached-dev-php-memcached-%{gitver} %{pecl_name}-%{version}
%endif

# https://bugs.php.net/61261
sed -i -e '/PHP_MEMCACHED_VERSION/s/2.0.0-dev/%{version}/' %{pecl_name}-%{version}/php_memcached.h

# Chech version as upstream often forget to update this
extver=$(sed -n '/#define PHP_MEMCACHED_VERSION/{s/.* "//;s/".*$//;p}' %{pecl_name}-%{version}/php_memcached.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream HTTP version is now ${extver}, expecting %{version}.
   : Update the pdover macro and rebuild.
   exit 1
fi

cp %{pecl_name}-%{version}/fastlz/LICENSE LICENSE-FastLZ

cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; ----- Options to use the memcached session handler

;  Use memcache as a session handler
;session.save_handler=memcached
;  Defines a comma separated list of server urls to use for session storage
;session.save_path="localhost:11211"
EOF


%build
cd %{pecl_name}-%{version}
phpize
%configure --enable-memcached-igbinary \
           --enable-memcached-json
make %{?_smp_mflags}


%install
make install -C %{pecl_name}-%{version} INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{pecl_name}.ini %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
cd %{pecl_name}-%{version}
# only check if build extension can be loaded
ln -s %{php_extdir}/json.so modules/
ln -s %{php_extdir}/igbinary.so modules/
%{_bindir}/php -n -q \
    -d extension_dir=modules \
    -d extension=json.so \
    -d extension=igbinary.so \
    -d extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


%files
%doc %{pecl_name}-%{version}/{CREDITS,LICENSE,README.markdown,ChangeLog}
%doc LICENSE-FastLZ
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Sat Mar 03 2012  Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-0.1.1736623
- update to git snapshot (post 2.0.0b2) for php 5.4 build

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Sep 17 2011  Remi Collet <remi@fedoraproject.org> - 1.0.2-7
- rebuild against libmemcached 0.52
- adapted filter
- clean spec

* Thu Jun 02 2011  Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-6
- rebuild against libmemcached 0.49

* Thu Mar 17 2011  Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-5
- rebuilt with igbinary support
- add arch specific provides/requires

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 23 2010  Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-3
- add filter_provides to avoid private-shared-object-provides memcached.so

* Fri Oct 01 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-2
- rebuild against libmemcached 0.44 with SASL support

* Tue May 04 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-1
- update to 1.0.2 for libmemcached 0.40

* Sat Mar 13 2010 Remi Collet <fedora@famillecollet.com> - 1.0.1-1
- update to 1.0.1 for libmemcached 0.38

* Sun Feb 07 2010 Remi Collet <fedora@famillecollet.com> - 1.0.0-3.1
- bump release

* Sat Feb 06 2010 Remi Collet <fedora@famillecollet.com> - 1.0.0-3
- rebuilt against new libmemcached
- add minimal %%check

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <fedora@famillecollet.com> - 1.0.0-1
- Update to 1.0.0 (First stable release)

* Sat Jun 27 2009 Remi Collet <fedora@famillecollet.com> - 0.2.0-1
- Update to 0.2.0 + Patch for HAVE_JSON constant

* Sun Apr 29 2009 Remi Collet <fedora@famillecollet.com> - 0.1.5-1
- Initial RPM

