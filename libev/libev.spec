%global source_dir  %{_datadir}/%{name}-source
%global inst_srcdir %{buildroot}/%{source_dir}

Name:		libev
Version:	4.03
Release:	2%{?dist}
Summary:	High-performance event loop/event model with lots of features

Group:		System Environment/Libraries
License:	BSD or GPLv2+
URL:		http://software.schmorp.de/pkg/libev.html
Source0:	http://dist.schmorp.de/libev/Attic/%{name}-%{version}.tar.gz
Source1:	%{name}.pc.in
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	automake libtool

%description
Libev is modeled (very loosely) after libevent and the Event Perl
module, but is faster, scales better and is more correct, and also more
featureful. And also smaller.

%package 	devel
Summary:	High-performance event loop/event model with lots of features
Group:		System Environment/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description 	devel
Libev is modeled (very loosely) after libevent and the Event Perl
module, but is faster, scales better and is more correct, and also more
featureful. And also smaller. Development libraries.


%package	source
Summary:	High-performance event loop/event model with lots of features
Group:		System Environment/Libraries
BuildArch:	noarch

%description	source
This package contains the source code for libev.

Libev is modeled (very loosely) after libevent and the Event Perl
module, but is faster, scales better and is more correct, and also more
featureful. And also smaller. Development libraries.

%prep
%setup -q

# Add pkgconfig support
cp -p %{SOURCE1} .
sed -i.pkgconfig -e 's|Makefile|Makefile libev.pc|' configure.ac configure
sed -i.pkgconfig -e 's|lib_LTLIBRARIES|pkgconfigdir = $(libdir)/pkgconfig\n\npkgconfig_DATA = libev.pc\n\nlib_LTLIBRARIES|' Makefile.am Makefile.in
aclocal
automake


%build
%configure --disable-static --with-pic --includedir=%{_includedir}/%{name}
make %{?_smp_mflags}


%check
make check


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}.la

# Make the source package
mkdir -p %{inst_srcdir}

find . -type f | grep -E '.*\.(c|h|am|ac|inc|m4|h.in|pc.in|man.pre|pl|txt)$' | xargs tar cf - | (cd %{inst_srcdir} && tar xf -)
install -p -m 0644 Changes ev.pod LICENSE README %{inst_srcdir}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{_libdir}/%{name}.so.4
%{_libdir}/%{name}.so.4.0.0
%{_mandir}/man?/*


%files devel
%defattr(-,root,root,-)
%{_libdir}/%{name}.so
%{_includedir}/libev/
%{_libdir}/pkgconfig/%{name}.pc


%files source
%defattr(-,root,root,-)
%{source_dir}


%changelog
* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb  5 2011 Michal Nowak <mnowak@redhat.com> - 4.03-1
- 4.03; RHBZ#674022
- add a -source subpackage (Mathieu Bridon); RHBZ#672153

* Mon Jan 10 2011 Michal Nowak <mnowak@redhat.com> - 4.01-1
- 4.01
- fix grammar in %%description

* Sat Jan  2 2010 Michal Nowak <mnowak@redhat.com> - 3.90-1
- 3.9

* Fri Aug 10 2009 Michal Nowak <mnowak@redhat.com> - 3.80-1
- 3.8
- always use the most recent automake
- BuildRequires now libtool

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.70-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Michal Nowak <mnowak@redhat.com> - 3.70-2
- spec file change, which prevented uploading most recent tarball
  so the RPM was "3.70" but tarball was from 3.60

* Fri Jul 17 2009 Michal Nowak <mnowak@redhat.com> - 3.70-1
- v3.7
- list libev soname explicitly

* Mon Jun 29 2009 Michal Nowak <mnowak@redhat.com> - 3.60-1
- previous version was called "3.6" but this is broken update
  path wrt version "3.53" -- thus bumping to "3.60"

* Thu Apr 30 2009 Michal Nowak <mnowak@redhat.com> - 3.6-1
- 3.60
- fixed few mixed-use-of-spaces-and-tabs warnings in spec file

* Thu Mar 19 2009 Michal Nowak <mnowak@redhat.com> - 3.53-1
- 3.53

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 07 2009 Michal Nowak <mnowak@redhat.com> - 3.52-1
- 3.52

* Wed Dec 24 2008 Michal Nowak <mnowak@redhat.com> - 3.51-1
- 3.51

* Thu Nov 20 2008 Michal Nowak <mnowak@redhat.com> - 3.49-1
- version bump: 3.49

* Sun Nov  9 2008 Michal Nowak <mnowak@redhat.com> - 3.48-1
- version bump: 3.48

* Mon Oct  6 2008 kwizart <kwizart at gmail.com> - 3.44-1
- bump to 3.44

* Tue Sep  2 2008 kwizart <kwizart at gmail.com> - 3.43-4
- Fix pkgconfig support

* Mon Aug 12 2008 Michal Nowak <mnowak@redhat.com> - 3.43-2
- removed libev.a
- installing with "-p"
- event.h is removed intentionaly, because is there only for 
  backward compatibility with libevent

* Mon Aug 04 2008 Michal Nowak <mnowak@redhat.com> - 3.43-1
- initial package

