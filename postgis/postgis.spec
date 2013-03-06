%{!?javabuild:%define	javabuild 0}
%{!?utils:%define	utils 1}
%{!?gcj_support:%define	gcj_support 0}

%global majorversion 2.0

%global pg_version_minimum 9.2
%global pg_version_built  %(if [ -x %{_bindir}/pg_config ]; then %{_bindir}/pg_config --version | /bin/sed 's,^PostgreSQL *,,gi'; else echo %{pg_version_minimum}; fi)

Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:		postgis
Version:	2.0.2
Release:	2%{?dist}
License:	GPLv2+
Group:		Applications/Databases
Source0:	http://postgis.refractions.net/download/%{name}-%{version}.tar.gz
Source2:	http://www.postgis.org/download/%{name}-%{version}.pdf
Source4:	filter-requires-perl-Pg.sh
Patch0:		postgis-1.5.1-pgsql9.patch
URL:		http://postgis.refractions.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql-devel >= %{pg_version_minimum}, proj-devel, geos-devel >= 3.1.1 byacc, proj-devel, flex, sinjdoc, java, java-devel, ant
BuildRequires:	gtk2-devel, libxml2-devel, gdal-devel >= 1.9.0
Requires:	postgresql >= %{pg_version_built}, geos >= 3.1.1, proj, gdal >= 1.9.0

%description
PostGIS adds support for geographic objects to the PostgreSQL object-relational
database. In effect, PostGIS "spatially enables" the PostgreSQL server,
allowing it to be used as a backend spatial database for geographic information
systems (GIS), much like ESRI's SDE or Oracle's Spatial extension. PostGIS 
follows the OpenGIS "Simple Features Specification for SQL" and has been 
certified as compliant with the "Types and Functions" profile.

%package docs
Summary:	Extra documentation for PostGIS
Group:		Applications/Databases
%description docs
The postgis-docs package includes PDF documentation of PostGIS.

%if %javabuild
%package jdbc
Summary:	The JDBC driver for PostGIS
Group:		Applications/Databases
License:	LGPLv2+
Requires:	%{name} = %{version}-%{release}, postgresql-jdbc
BuildRequires:	ant >= 0:1.6.2, junit >= 0:3.7, postgresql-jdbc

%if %{gcj_support}
BuildRequires:		gcc-java
BuildRequires:		java-1.5.0-gcj-devel
Requires(post):		%{_bindir}/rebuild-gcj-db
Requires(postun):	%{_bindir}/rebuild-gcj-db
%endif

%description jdbc
The postgis-jdbc package provides the essential jdbc driver for PostGIS.
%endif

%if %utils
%package utils
Summary:	The utils for PostGIS
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}, perl-DBD-Pg

%description utils
The postgis-utils package provides the utilities for PostGIS.
%endif

%define __perl_requires %{SOURCE4}

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .pgsql9
# Copy .pdf file to top directory before installing.
cp -p %{SOURCE2} .

%build
%configure --with-gui
#make %{?_smp_mflags} LPATH=`pg_config --pkglibdir` shlib="%{name}.so"
make LPATH=`pg_config --pkglibdir` shlib="%{name}.so"

%if %javabuild
export BUILDXML_DIR=%{_builddir}/%{name}-%{version}/java/jdbc
JDBC_VERSION_RPM=`rpm -ql postgresql-jdbc| grep 'jdbc2.jar$'|awk -F '/' '{print $5}'`
sed 's/postgresql.jar/'${JDBC_VERSION_RPM}'/g' $BUILDXML_DIR/build.xml > $BUILDXML_DIR/build.xml.new
mv -f $BUILDXML_DIR/build.xml.new $BUILDXML_DIR/build.xml
pushd java/jdbc
ant
popd
%endif

%if %utils
 make -C utils
%endif

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -d %{buildroot}%{_libdir}/pgsql/
install -d %{buildroot}%{_bindir}/
install -d  %{buildroot}%{_datadir}/pgsql/contrib/
install -m 644 *.sql %{buildroot}%{_datadir}/pgsql/contrib/
install -m 755 loader/shp2pgsql loader/shp2pgsql-gui %{buildroot}%{_bindir}/
rm -f  %{buildroot}%{_datadir}/*.sql

if [ "%{_libdir}" = "/usr/lib64" ] ; then
	mv %{buildroot}%{_datadir}/pgsql/contrib/%{name}-%{majorversion}/postgis.sql %{buildroot}%{_datadir}/pgsql/contrib/postgis-64.sql
fi

%if %javabuild
install -d %{buildroot}%{_javadir}
install -m 755 java/jdbc/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
%if %{gcj_support}
aot-compile-rpm
%endif
strip %{buildroot}/%{_libdir}/gcj/%{name}/*.jar.so
%endif

%if %utils
install -d %{buildroot}%{_datadir}/%{name}
install -m 755 utils/*.pl %{buildroot}%{_datadir}/%{name}
%endif

%clean
rm -rf %{buildroot}

%if %javabuild
%if %gcj_support
%post -p %{_bindir}/rebuild-gcj-db
%postun -p %{_bindir}/rebuild-gcj-db
%endif
%endif

%files
%defattr(-,root,root)
%doc COPYING CREDITS NEWS TODO README.%{name} doc/html loader/README.* doc/%{name}.xml doc/ZMSgeoms.txt 
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/pgsql/postgis-*.so
%{_datadir}/pgsql/contrib/*.sql
%{_datadir}/pgsql/contrib/%{name}-%{majorversion}/*.sql
%{_datadir}/pgsql/contrib/%{name}-%{majorversion}/postgis_restore.pl
%{_datadir}/pgsql/extension/postgis-*.sql
%{_datadir}/pgsql/extension/postgis_topology*.sql
%{_datadir}/pgsql/extension/postgis.control
%{_datadir}/pgsql/extension/postgis_topology.control
%{_datadir}/postgis/svn_repo_revision.pl
%{_includedir}/liblwgeom.h
%{_libdir}/liblwgeom*
%{_libdir}/pgsql/rtpostgis-%{majorversion}.so

%if %javabuild
%files jdbc
%defattr(-,root,root)
%doc java/jdbc/COPYING_LGPL java/jdbc/README
%attr(755,root,root) %{_javadir}/%{name}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*.jar.so
%{_libdir}/gcj/%{name}/*.jar.db
%endif
%endif

%if %utils
%files utils
%defattr(755,root,root)
%doc utils/README
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/test_estimation.pl
%{_datadir}/%{name}/profile_intersects.pl
%{_datadir}/%{name}/test_joinestimation.pl
%{_datadir}/%{name}/create_undef.pl
%{_datadir}/%{name}/%{name}_proc_upgrade.pl
%{_datadir}/%{name}/%{name}_restore.pl
%{_datadir}/%{name}/read_scripts_version.pl
%{_datadir}/%{name}/test_geography_estimation.pl
%{_datadir}/%{name}/test_geography_joinestimation.pl
%endif

%files docs
%defattr(-,root,root)
%doc postgis*.pdf

%changelog
* Fri Jan 25 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.0.2-2
- Rebuilt against geos 3.3.7.
- Apply changes for PostgreSQL 9.2 and extensions.

* Wed Jan 16 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.0.2-1
- Update to 2.0.2, for various changes described at:
  http://www.postgis.org/news/20121203/

* Tue Nov 13 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 2.0.1-1
- Update to 2.0.1, so it works against PostgreSQL 9.2,
  which also fixes #872710.
- Add deps for gdal.
- Don't build JDBC portions. I have already disabled it in
  upstream packaging 8 months ago.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 4 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.3-2
- Provide postgis.jar instead of provide postgis-1.5.2.jar,
  per #714856

* Tue Oct 4 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.3-1
- Update to 1.5.3

* Tue Apr 19 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.2-1
- Update to 1.5.2

* Sun Apr 03 2011 Nils Philippsen <nils@redhat.com> - 1.5.1-3
- cope with PostgreSQL 9.0 build environment
- require pgsql version used for building

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Mar 11 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1

* Tue Jan 12 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.0-1
- Update to 1.5.0
- Trim changelog a bit.

* Wed Jan 6 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.4.1-2
- Add shp2pgsql-{cli-gui} among installed files.

* Sun Dec 20 2009 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.4.1-1
- Update to 1.4.1

* Thu Dec 03 2009 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.4.1-rc2_1.2
- Fix spec per rawhide report.

* Tue Dec 01 2009 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.4.1-rc2_1.1
- Update spec for rc2 changes.

* Mon Nov 30 2009 Devrim GUNDUZ <devrim@gunduz.org> - 1.4.1rc2-1
- Update to 1.4.1rc2

* Mon Nov 23 2009 Devrim GUNDUZ <devrim@gunduz.org> - 1.4.1rc1-1
- Update to 1.4.1rc1

* Sun Nov 22 2009 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.4.0-2
- Fix spec, per bz #536860

* Mon Jul 27 2009 Devrim GUNDUZ <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0rc1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 6 2009 Devrim GUNDUZ <devrim@gunduz.org> - 1.4.0rc1-1
- Update to 1.4.0rc1
- Fix spec for 1.4
