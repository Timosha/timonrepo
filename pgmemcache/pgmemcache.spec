# for f14 only
Summary:	A PostgreSQL API to interface with memcached.
Name:		pgmemcache
Version:	2.0.4
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/2672/pgmemcache_2.0.4.tar.bz2
URL:		http://pgfoundry.org/projects/pgmemcache
BuildRequires:	postgresql-devel >= 8.1
BuildRequires:  libmemcached-devel >= 0.40
Requires:	postgresql-server >= 8.1 
Requires:	libmemcached >= 0.40
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pgmemcache is a set of PostgreSQL user-defined functions that provide
an interface to memcached.

%prep
%setup -q -n %{name}

%build
make USE_PGXS=1 %{?_smp_mflags} 

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/pgsql/
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_docdir}/%{name}-%{version}
install -m 755 %{name}.so %{buildroot}%{_libdir}/pgsql/%{name}.so
install -m 755 %{name}.sql %{buildroot}%{_datadir}/%{name}

%clean
rm -rf %{buildroot}

#%post -p /sbin/ldconfig 
#%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%doc README.%{name} LICENSE COPYING NEWS
%{_datadir}/%{name}/%{name}*.sql
%{_libdir}/pgsql/%{name}.so

%changelog
* Tue Oct 5 2010 Timon <timosha@gmail.com> - 2.0.4-1
- Update to new stable 2.0.4

* Wed Apr 9 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 0.4.4-3
- Initial commit for pgsqlrpms.org repo.

* Sat Jun 17 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 0.4.4-2
- Added Requires, per bugzilla review #244536 (Thanks Ruben)
- Renamed README file, per bugzilla review #244536

* Sat Jun 16 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 0.4.4-1
- Initial RPM packaging for Fedora
