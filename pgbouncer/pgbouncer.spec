%define debug 0

Name:		pgbouncer
Version:	1.4
Release:	2%{?dist}
Summary:	Lightweight connection pooler for PostgreSQL
Group:		Applications/Databases
License:	MIT and BSD
URL:		http://pgfoundry.org/projects/pgbouncer/
Source0:	http://pgfoundry.org/frs/download.php/2912/%{name}-%{version}.tgz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-ini.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libevent-devel >= 1.3b
Requires:	initscripts

Requires(post):	chkconfig
Requires(preun):	chkconfig, initscripts
Requires(postun):	initscripts

%description
pgbouncer is a lightweight connection pooler for PostgreSQL.
pgbouncer uses libevent for low-level socket handling.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0

%build
sed -i.fedora \
 -e 's|-fomit-frame-pointer||' \
 -e '/BININSTALL/s|-s||' \
 configure

%configure \
%if %debug
	--enable-debug \
	--enable-cassert \
%endif
--datadir=%{_datadir} 

make %{?_smp_mflags} V=1

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -p -d %{buildroot}%{_sysconfdir}/
install -p -d %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 644 etc/pgbouncer.ini %{buildroot}%{_sysconfdir}/
rm -f %{buildroot}%{_docdir}/%{name}/pgbouncer.ini
install -p -d %{buildroot}%{_initrddir}
install -p -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%post
chkconfig --add pgbouncer

%preun
if [ $1 = 0 ] ; then
	/sbin/service pgbouncer condstop >/dev/null 2>&1
	chkconfig --del pgbouncer
fi

%postun
if [ "$1" -ge "1" ] ; then
	/sbin/service pgbouncer condrestart >/dev/null 2>&1 || :
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README NEWS AUTHORS
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}.ini
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_mandir}/man1/%{name}.*
%{_mandir}/man5/%{name}.*

%changelog
* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 15 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.4-1
- Update to 1.4

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May 10 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.3.3-1
- Update to 1.3.3, per changes described in:
- http://pgfoundry.org/frs/shownotes.php?release_id=1645

* Tue Mar 16 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.3.2-1
- Update to 1.3.2, per changes described in:
- http://pgfoundry.org/frs/shownotes.php?release_id=1605

* Sat Dec 05 2009 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.3.1-2
- Fix init script, per report from Scott Bowers:
  http://lists.pgfoundry.org/pipermail/pgbouncer-general/2009-December/000477.html

* Tue Dec 1 2009 - Devrim GUNDUZ <devrim@gunduz.org> 1.3.1-1
- Update to 1.3.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 1.2.3-3
- More fixes, per Fedora review.

* Fri Aug 29 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 1.2.3-2
- More fixes, per Fedora review.

* Fri Aug 8 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 1.2.3-1
- Update to 1.2.3
- Final fixes for Fedora review

* Sun Mar 23 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 1.1.2-3
- Mark sysconfig file as config file, per Guillaume Smet.

* Fri Mar 7 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 1.1.2-2
- Add a patch for pgbouncer.ini to satisfy Red Hat defaults and security.
  Per Darcy Buskermolen.
- Fix chkconfig line
- Add sysconfig file
- Refactor init script

* Sat Mar 1 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 1.1.2-1
- Update to 1.1.2
- Various spec file improvements, per bz review #244593 .

* Fri Oct 26 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.1.1-1
- Update to 1.1.1

* Tue Oct 9 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.1-1
- Update to 1.1

* Tue Sep 25 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.0.8-2
- Added init script from Darcy.

* Tue Sep 18 2007 - Darcy Buskermolen <darcyb@commandprompt.com> 1.0.8-1
- Update to pgBouncer 1.0.8
- Add libevent to requires

* Sat Jun 18 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.0.7-2
- Prepare for Fedora review
- Change spec file name

* Thu May 03 2007 David Fetter <david@fetter.org> 1.0.7-1
- Initial build 