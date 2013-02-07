%global debug 0

Name:		pgbouncer
Version:	1.5.4
Release:	1%{?dist}
Summary:	Lightweight connection pooler for PostgreSQL
Group:		Applications/Databases
License:	MIT and BSD
URL:		http://pgfoundry.org/projects/pgbouncer/
Source0:	http://ftp.postgresql.org/pub/projects/pgFoundry/%{name}/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}.service
Source2:	%{name}.tmpfiles.d

Patch0:		%{name}.ini.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libevent-devel >= 2.0
BuildRequires:  systemd-units

# pre/post stuff needs systemd too
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

Requires(post): chkconfig

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

%{__make} %{?_smp_mflags} V=1

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
install -p -d %{buildroot}%{_sysconfdir}/%{name}/
install -p -m 644 etc/pgbouncer.ini %{buildroot}%{_sysconfdir}/%{name}
install -p -m 700 etc/mkauth.py %{buildroot}%{_sysconfdir}/%{name}/

install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}

mkdir -p %{buildroot}%{_prefix}/lib/tmpfiles.d
install -m 0644 %{SOURCE2} %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf

install -d -m 755 %{buildroot}%{_localstatedir}/log/%{name}

install -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

# Remove duplicated files
%{__rm} -f %{buildroot}%{_docdir}/%{name}/*

%post
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%pre
groupadd -r pgbouncer >/dev/null 2>&1 || :
useradd -m -g pgbouncer -r -s /bin/bash \
        -c "PgBouncer Server" pgbouncer >/dev/null 2>&1 || :
#touch /var/log/pgbouncer.log
#chown pgbouncer:pgbouncer /var/log/pgbouncer.log
#chmod 0700 /var/log/pgbouncer.log

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 || :
    /bin/systemctl stop %{name}.service >/dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README NEWS COPYRIGHT AUTHORS doc/README.html doc/config.html doc/faq.html doc/todo.html doc/usage.html
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.ini
%{_unitdir}/%{name}.service
%{_mandir}/man1/%{name}.*
%{_mandir}/man5/%{name}.*
%{_sysconfdir}/%{name}/mkauth.py*
%attr(755,pgbouncer,pgbouncer) %dir %{_localstatedir}/run/%{name}
%attr(755,pgbouncer,pgbouncer) %dir %{_localstatedir}/log/%{name}
%{_prefix}/lib/tmpfiles.d/%{name}.conf


%changelog
* Thu Feb 7 2013 Timon <timosha@gmail.com> - 1.5.4-1
- pgbouncer 1.5.4
- systemd fixes
- pgbouncer user

* Wed Aug 8 2012 Timon <timosha@gmail.com> - 1.5.2-3
- remove pgbouncer user
- systemd

* Thu Jun 21 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.2-2
- Fix useradd line.

* Tue Jun 5 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.2-1
- Update to 1.5.2, per changes described at:
  http://pgfoundry.org/forum/forum.php?forum_id=1885

* Tue Apr 24 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1, for the changes described here:
  http://pgfoundry.org/frs/shownotes.php?release_id=1936

* Sun Apr 08 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5-2
- Fix shell of pgbouncer user, to avoid startup errors.

* Fri Apr 6 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5-1
- Update to 1.5, for the changes described here:
  http://pgfoundry.org/frs/shownotes.php?release_id=1920
- Trim changelog

* Fri Aug 12 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.4.2-1
- Update to 1.4.2, for the changes described here:
  http://pgfoundry.org/frs/shownotes.php?release_id=1863

* Mon Sep 13 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.3.4-1
- Update to 1.3.4, for the changes described here:
  http://pgfoundry.org/frs/shownotes.php?prelease_id=1698
* Fri Aug 06 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.3.3-2
- Sleep 2 seconds before getting pid during start(), like we do in PostgreSQL
  init script, to avoid false positive startup errors.

* Tue May 11 2010 Devrim GUNDUZ <devrim@gunduz.org> - 1.3.3-1
- Update to 1.3.3, per pgrpms.org #25, for the fixes described at:
  http://pgfoundry.org/frs/shownotes.php?release_id=1645

* Tue Mar 16 2010 Devrim GUNDUZ <devrim@gunduz.org> - 1.3.2-1
- Fix some issues in init script. Fixes pgrpms.org #9.

