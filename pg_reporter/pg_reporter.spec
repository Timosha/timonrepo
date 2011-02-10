# SPEC file for pg_reporter
# Copyright(C) 2010 NIPPON TELEGRAPH AND TELEPHONE CORPORATION

# Original declaration for pg_reporter rpmbuild #

%define sname %{name}-%{version}

## Set general information for pg_reporter.
Summary:    General Reporting tool for PostgreSQL
Name:       pg_reporter
Version:    1.0.1
Release:    1%{?dist}
License:    BSD
Group:      Applications/Databases
Source0:    http://pgfoundry.org/frs/download.php/2885/%{name}-%{version}.tar.gz
URL:        http://pgfoundry.org/projects/pgstatsinfo/
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)

## We use postgresql-devel package
BuildRequires:  postgresql-devel

## Define each sub-packages summary, requires and description.
# pg_reporter
#%package
Summary: General Reporting tool
Group: Applications/Databases
Requires:  postgresql-contrib >= 8.3.0

%description
This package contains executable file, scripts and some files
for generating report file from PostgreSQL Database.

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
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter
install -d %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/css
install -d %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/files
install -d %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js
install -d %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js/excanvas
install -d %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js/graph
install -d %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/template
install -d %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/xsl


# Set each files
install -m 755 %{_builddir}/%{sname}/pg_reporter %{buildroot}%{_bindir}/pg_reporter
install -m 755 %{_builddir}/%{sname}/htdocs/.dbnames %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/.dbnames
install -m 755 %{_builddir}/%{sname}/htdocs/css/style.css %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/css/style.css
install -m 755 %{_builddir}/%{sname}/htdocs/js/common.js %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js/common.js
install -m 755 %{_builddir}/%{sname}/htdocs/js/index.js	%{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js/index.js

install -m 755 %{_builddir}/%{sname}/htdocs/js/excanvas/AUTHORS	%{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js/excanvas/AUTHORS
install -m 755 %{_builddir}/%{sname}/htdocs/js/excanvas/COPYING	%{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js/excanvas/COPYING
install -m 755 %{_builddir}/%{sname}/htdocs/js/excanvas/excanvas.compiled.js %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js/excanvas/excanvas.compiled.js
install -m 755 %{_builddir}/%{sname}/htdocs/js/excanvas/excanvas.js %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js/excanvas/excanvas.js
install -m 755 %{_builddir}/%{sname}/htdocs/js/excanvas/README %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js/excanvas/README

install -m 755 %{_builddir}/%{sname}/htdocs/js/graph/AUTHORS %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js/graph/AUTHORS
install -m 755 %{_builddir}/%{sname}/htdocs/js/graph/circle.js %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js/graph/circle.js
install -m 755 %{_builddir}/%{sname}/htdocs/js/graph/COPYING %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js/graph/COPYING
install -m 755 %{_builddir}/%{sname}/htdocs/js/graph/line.js %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js/graph/line.js
install -m 755 %{_builddir}/%{sname}/htdocs/js/graph/radar.js %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js/graph/radar.js 
install -m 755 %{_builddir}/%{sname}/htdocs/js/graph/vbar.js %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js/graph/vbar.js
install -m 755 %{_builddir}/%{sname}/htdocs/js/graph/versions.txt %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/js/graph/versions.txt

install -m 755 %{_builddir}/%{sname}/htdocs/template/details.xml %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/template/details.xml
install -m 755 %{_builddir}/%{sname}/htdocs/template/index.xml %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/template/index.xml
install -m 755 %{_builddir}/%{sname}/htdocs/template/schema.xml %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/template/schema.xml
install -m 755 %{_builddir}/%{sname}/htdocs/template/snapshot.xml %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/template/snapshot.xml
install -m 755 %{_builddir}/%{sname}/htdocs/template/statistics.xml %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/template/statistics.xml
install -m 755 %{_builddir}/%{sname}/htdocs/template/table.xml %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/template/table.xml 

install -m 755 %{_builddir}/%{sname}/htdocs/xsl/common.xsl %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/xsl/common.xsl
install -m 755 %{_builddir}/%{sname}/htdocs/xsl/dbnames.xsl %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/xsl/dbnames.xsl
install -m 755 %{_builddir}/%{sname}/htdocs/xsl/dir.xsl %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/xsl/dir.xsl
install -m 755 %{_builddir}/%{sname}/htdocs/xsl/html.xsl %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/xsl/html.xsl
install -m 755 %{_builddir}/%{sname}/htdocs/xsl/view.xsl %{buildroot}%{_datadir}/pgsql/contrib/pg_reporter/xsl/view.xsl

## Cleanup after uninstall.
# pg_reporter
%postun
rm -rf %{_datadir}/pgsql/contrib/pg_reporter

%clean
rm -rf %{buildroot}

## Set files for each packages
# pg_reporter
%files
%defattr(-,root,root)
%{_bindir}/pg_reporter
%{_datadir}/pgsql/contrib/pg_reporter/.dbnames
%{_datadir}/pgsql/contrib/pg_reporter/css/style.css
%{_datadir}/pgsql/contrib/pg_reporter/js/common.js
%{_datadir}/pgsql/contrib/pg_reporter/js/index.js
%{_datadir}/pgsql/contrib/pg_reporter/js/excanvas/AUTHORS
%{_datadir}/pgsql/contrib/pg_reporter/js/excanvas/COPYING
%{_datadir}/pgsql/contrib/pg_reporter/js/excanvas/excanvas.compiled.js
%{_datadir}/pgsql/contrib/pg_reporter/js/excanvas/excanvas.js
%{_datadir}/pgsql/contrib/pg_reporter/js/excanvas/README
%{_datadir}/pgsql/contrib/pg_reporter/js/graph/AUTHORS
%{_datadir}/pgsql/contrib/pg_reporter/js/graph/circle.js
%{_datadir}/pgsql/contrib/pg_reporter/js/graph/COPYING
%{_datadir}/pgsql/contrib/pg_reporter/js/graph/line.js
%{_datadir}/pgsql/contrib/pg_reporter/js/graph/radar.js
%{_datadir}/pgsql/contrib/pg_reporter/js/graph/vbar.js
%{_datadir}/pgsql/contrib/pg_reporter/js/graph/versions.txt
%{_datadir}/pgsql/contrib/pg_reporter/template/details.xml
%{_datadir}/pgsql/contrib/pg_reporter/template/index.xml
%{_datadir}/pgsql/contrib/pg_reporter/template/schema.xml
%{_datadir}/pgsql/contrib/pg_reporter/template/snapshot.xml
%{_datadir}/pgsql/contrib/pg_reporter/template/statistics.xml 
%{_datadir}/pgsql/contrib/pg_reporter/template/table.xml 
%{_datadir}/pgsql/contrib/pg_reporter/xsl/common.xsl
%{_datadir}/pgsql/contrib/pg_reporter/xsl/dbnames.xsl
%{_datadir}/pgsql/contrib/pg_reporter/xsl/dir.xsl
%{_datadir}/pgsql/contrib/pg_reporter/xsl/html.xsl
%{_datadir}/pgsql/contrib/pg_reporter/xsl/view.xsl
%dir %{_datadir}/pgsql/contrib/pg_reporter/files

# History of pg_reporter.
%changelog
* Wed Feb 9 2011 - Timon <timosha@gmail.com> 1.0.1-1
- Build for Fedora

* Fri Jun 11 2010 - NTT OSS Center <kasahara.tatsuhito@oss.ntt.co.jp> 1.0.0-1
- Initial cut for 1.0.0
* Fri Apr  2 2010 - NTT OSS Center <kasahara.tatsuhito@oss.ntt.co.jp> 1.0-alpha1-1
- Release alpha
