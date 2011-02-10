# SPEC file for pg_statinfo_v2
# Copyright(C) 2010 NIPPON TELEGRAPH AND TELEPHONE CORPORATION

# Original declaration for pg_statsinfo rpmbuild #

## Set general information for pgstatsinfo.
Summary:    Performance monitoring tool for PostgreSQL
Name:       pg_statsinfo
Version:    2.0.1
Release:    2%{?dist}
License:    BSD
Group:      Applications/Databases
Source0:    http://pgfoundry.org/frs/download.php/2791/%{name}-%{version}.tar.gz
		
URL:        http://pgfoundry.org/projects/pgstatsinfo/
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)

## We use postgresql-devel package
BuildRequires:  postgresql-devel pam-devel zlib-devel openssl-devel readline-devel

%description
pg_statsinfo monitors an instance of PostgreSQL server and gather
the statistics and activities of the server as snapshots.

## pre work for build pg_statsinfo
%prep
%setup -q -n %{name}-%{version}

## Set variables for build environment
%build
USE_PGXS=1 make %{?_smp_mflags}

## Set variables for install
%install
rm -rf %{buildroot}

USE_PGXS=1 make DESTDIR=%{buildroot}

## Install each modules
#  Set install location path
install -d %{buildroot}%{_libdir}/pgsql
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/pgsql/contrib

# Install pg_statsinfo package files
install -m 755 bin/pg_statsinfo %{buildroot}%{_bindir}/pg_statsinfo
install -m 644 bin/pg_statsrepo.sql %{buildroot}%{_datadir}/pgsql/contrib/pg_statsrepo.sql
install -m 644 bin/uninstall_pg_statsrepo.sql %{buildroot}%{_datadir}/pgsql/contrib/uninstall_pg_statsrepo.sql

mkdir -p %{buildroot}%{_libdir}/pgsql/plugins
install -m 755 lib/pg_statsinfo.so %{buildroot}%{_libdir}/pgsql/plugins/pg_statsinfo.so
install -m 644 lib/pg_statsinfo.sql %{buildroot}%{_datadir}/pgsql/contrib/pg_statsinfo.sql
install -m 644 lib/uninstall_pg_statsinfo.sql %{buildroot}%{_datadir}/pgsql/contrib/uninstall_pg_statsinfo.sql

%clean
rm -rf %{buildroot}

## Set files for this packages
%files
%defattr(-,root,root)
%{_libdir}/pgsql/plugins/pg_statsinfo.so
%{_bindir}/pg_statsinfo
%{_datadir}/pgsql/contrib/pg_statsrepo.sql
%{_datadir}/pgsql/contrib/uninstall_pg_statsrepo.sql
%{_datadir}/pgsql/contrib/pg_statsinfo.sql
%{_datadir}/pgsql/contrib/uninstall_pg_statsinfo.sql

# History of pg_statsinfo-v2 RPM.
# Bellow messages are still dummy.
%changelog
* Thu Feb 10 2011 - Timon <timosh@gmail.com> 2.0.1-2
- move to $libdir/pgsql/plugins

* Wed Feb 9 2011 - Timon <timosh@gmail.com> 2.0.1-1
- Build for Fedora

* Fri Apr 2 2010 - NTT OSS Center <kasahara.tatsuhito@oss.ntt.co.jp> 2.0.0-1
- Initial cut for 2.0.0

