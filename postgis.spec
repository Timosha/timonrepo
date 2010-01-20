%{!?javabuild:%define	javabuild 1}
%{!?utils:%define	utils 1}
%{!?gcj_support:%define	gcj_support 1}

Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:		postgis
Version:	1.5.0
Release:	b2_1%{?dist}
License:	GPLv2+
Group:		Applications/Databases
Source0:	http://postgis.refractions.net/download/%{name}-%{version}b2.tar.gz
Source2:	http://www.postgis.org/download/%{name}-%{version}b2.pdf
Source4:	filter-requires-perl-Pg.sh
URL:		http://postgis.refractions.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql-devel >= 8.2, proj-devel, geos-devel >= 3.1.1, byacc, proj-devel, flex, sinjdoc, java, java-devel, ant
BuildRequires:	gtk2-devel
Requires:	postgresql >= 8.2, geos >= 3.1.1, proj

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
%setup -q -n %{name}-%{version}b2
# Copy .pdf file to top directory before installing.
cp -p %{SOURCE2} .

%build
%configure --with-gui
#make %{?_smp_mflags} LPATH=`pg_config --pkglibdir` shlib="%{name}.so"
make LPATH=`pg_config --pkglibdir` shlib="%{name}.so"

%if %javabuild
export BUILDXML_DIR=%{_builddir}/%{name}-%{version}b2/java/jdbc
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
install -d  %{buildroot}%{_datadir}/pgsql/contrib/
install -m 644 *.sql %{buildroot}%{_datadir}/pgsql/contrib/
install -m 755 loader/shp2pgsql loader/shp2pgsql-gui %{buildroot}%{_bindir}/
rm -f  %{buildroot}%{_datadir}/*.sql

if [ "%{_libdir}" = "/usr/lib64" ] ; then
	mv %{buildroot}%{_datadir}/pgsql/contrib/postgis.sql %{buildroot}%{_datadir}/pgsql/contrib/postgis-64.sql
	mv %{buildroot}%{_datadir}/pgsql/contrib/postgis_upgrade_12_to_14.sql %{buildroot}%{_datadir}/pgsql/contrib/postgis_upgrade_12_to_14-64.sql
	mv %{buildroot}%{_datadir}/pgsql/contrib/postgis_upgrade_13_to_14.sql %{buildroot}%{_datadir}/pgsql/contrib/postgis_upgrade_13_to_14-64.sql
	mv %{buildroot}%{_datadir}/pgsql/contrib/postgis_upgrade_14_minor.sql %{buildroot}%{_datadir}/pgsql/contrib/postgis_upgrade_14_minor-64.sql	
fi

%if %javabuild
install -d %{buildroot}%{_javadir}
install -m 755 java/jdbc/%{name}-%{version}b2.jar %{buildroot}%{_javadir}
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
%{_datadir}/pgsql/contrib/%{name}-1.5/*.sql

%if %javabuild
%files jdbc
%defattr(-,root,root)
%doc java/jdbc/COPYING_LGPL java/jdbc/README
%attr(755,root,root) %{_javadir}/%{name}-%{version}b2.jar
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
%{_datadir}/%{name}/new_postgis_restore.pl
%{_datadir}/%{name}/read_scripts_version.pl
%{_datadir}/%{name}/test_geography_estimation.pl
%{_datadir}/%{name}/test_geography_joinestimation.pl
%endif

%files docs
%defattr(-,root,root)
%doc postgis*.pdf

%changelog
* Tue Jan 19 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.0b2-1
- Update to 1.5.0 beta2

* Tue Jan 12 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.5.0-b1-1
- Update to 1.5.0 beta1

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

* Thu Jun 18 2009 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.6-2
- Add a new subpackage: -docs, and add postgis pdf file to it.
- Own /usr/share/postgis, per bugzilla #474686

* Fri May 8 2009 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.6-1
- Update to 1.3.6

* Fri Apr 24 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 1.3.5-3
- Fix FTBFS: added BR: java-1.5.0-gcj-devel in case of gcj_support

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 16 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.5-1
- Update to 1.3.5

* Sat Nov 29 2008 Devrim GUNDUZ <devrim@gunduz.org> - 1.3.4-1
- Update to 1.3.4

* Mon Aug 11 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.3-4
- Fix #451387. Patch from Toshio.

* Thu Jun 26 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.3-3
- Rebuilt against geos 3.0.0

* Thu May 29 2008 Todd Zullinger <tmz@pobox.com> - 1.3.3-2
- fix license tags

* Sun Apr 13 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.3-1
- Update to 1.3.3

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.2-3.1
- Autorebuild for GCC 4.3

* Mon Jan 21 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 1.3.2-2.1
- Rebuilt against PostgreSQL 8.3

* Sat Jan 5 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.2-2
- Various fixes from Mark Cave-Ayland
- Removed patch2: template_gis is no longer built by default.
- Removed patch0: Building the JDBC driver using make is now deprecated
- Build JDBC driver using ant, rather than make.

* Thu Dec 6 2007 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.2-1
- Update to 1.3.2
- Updated patch2

* Wed Nov 21 2007 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.1-2
- Move postgresql-jdbc dependency to the correct place, per Rob Nagler.

* Tue Oct 16 2007 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.1-1
- Update to 1.3.1
- Updated patch2

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.2.1-3
- Rebuild for selinux ppc32 issue.

* Mon Jul 2 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.2.1-2
- Fix build problems (removed template_gis, per discussion with upstream).

* Mon Feb 19 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.2.1-1
- Update to 1.2.1
- Removed configure patch (it is in the upstream now)
- Added postgresql-jdbc as as dependency to -jdbc package, per Guillaume
- move strip to correct place, per Guillaume
- Fix long-standing post/postun problem, per Guillaume

* Wed Jan 3 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.2.0-4
- Added postgis.so among installed files, per Jon Burgess.
- Fix jdbc jar dedection problem

* Wed Dec 27 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 1.2.0-3
- Fix Requires for subpackages per bugzilla review #220743

* Mon Dec 26 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 1.2.0-2
- More spec file fixes per bugzilla review #220743

* Mon Dec 25 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 1.2.0-1
- Initial submission for Fedora Core Extras
- Spec file changes and fixes per FC Extras packaging guidelines

* Fri Jun 23 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 1.1.2-2
- Update to 1.1.2

* Tue Dec 22 2005 - Devrim GUNDUZ <devrim@commandprompt.com> 1.1.0-2
- Final fixes for 1.1.0

* Tue Dec 06 2005 - Devrim GUNDUZ <devrim@gunduz.org>
- Update to 1.1.0

* Mon Oct 03 2005 - Devrim GUNDUZ <devrim@gunduz.org>
- Make PostGIS build against pgxs so that we don't need PostgreSQL sources.
- Fixed all build errors except jdbc (so, defaulted to 0)
- Added new files under %%utils
- Removed postgis-jdbc2-makefile.patch (applied to -head)

* Tue Sep 27 2005 - Devrim GUNDUZ <devrim@gunduz.org>
- Update to 1.0.4

* Sun Apr 20 2005 - Devrim GUNDUZ <devrim@gunduz.org>
- 1.0.0 Gold

* Sun Apr 17 2005 - Devrim GUNDUZ <devrim@gunduz.org>
- Modified the spec file so that we can build JDBC2 RPMs...
- Added -utils RPM to package list.

* Fri Apr 15 2005 - Devrim GUNDUZ <devrim@gunduz.org>
- Added preun and postun scripts.

* Sat Apr 09 2005 - Devrim GUNDUZ <devrim@gunduz.org>
- Initial RPM build
- Fixed libdir so that PostgreSQL installations will not complain about it.
- Enabled --with-geos and modified the old spec.
