# build6x usage: define to 1 to build for RHL6.x.  Don't define at all for others.
%{?build6x:%define kerberos 0}
%{?build6x:%define nls 0}
%{?build6x:%define ssl 0}
#work around the undefined or defined to 1 build 6x interaction with the pam stuff
%{!?build6x:%define non6xpamdeps 1}
%{?build6x:%define non6xpamdeps 0}

%define beta 0

%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

%{!?tcl:%define tcl 1}
%{!?tkpkg:%define tkpkg 0}
%{!?jdbc:%define jdbc 1}
%{!?test:%define test 1}
%{!?python:%define python 1}
%{!?pltcl:%define pltcl 1}
%{!?plperl:%define plperl 1}
%{!?pls:%define pls 1}
%{!?ssl:%define ssl 1}
%{!?kerberos:%define kerberos 1}
%{!?nls:%define nls 1}
%{!?pam:%define pam 1}

# Python major version.
%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{expand: %%define pynextver %(python -c 'import sys;print(float(sys.version[0:3])+0.1)')}


Summary: PostgreSQL client programs and libraries.
Name: postgresql
Version: 7.3.4

# Conventions for PostgreSQL Global Development Group RPM releases:

# Official PostgreSQL Development Group RPMS have a PGDG after the release number.
# Integer releases are stable -- 0.1.x releases are Pre-releases, and x.y are
# test releases.

# Pre-releases are those that are built from CVS snapshots or pre-release
# tarballs from postgresql.org.  Official beta releases are not 
# considered pre-releases, nor are release candidates, as their beta or
# release candidate status is reflected in the version of the tarball. Pre-
# releases' versions do not change -- the pre-release tarball of 7.0.3, for
# example, has the same tarball version as the final official release of 7.0.3:
# but the tarball is different.

# Test releases are where PostgreSQL itself is not in beta, but certain parts of
# the RPM packaging (such as the spec file, the initscript, etc) are in beta.

# Pre-release RPM's should not be put up on the public ftp.postgresql.org server
# -- only test releases or full releases should be.

Release: 2
License: BSD
Group: Applications/Databases
Source0: ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.gz
Source3: postgresql.init
Source5: ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.gz.md5
Source6: README.rpm-dist
Source8: http://jdbc.postgresql.org/download/pg73jdbc1.jar
Source9: http://jdbc.postgresql.org/download/pg73jdbc2.jar
Source10: http://jdbc.postgresql.org/download/pg73jdbc3.jar
Source15: postgresql-bashprofile
Source16: filter-requires-perl-Pg.sh
Source17: postgresql-7.3.4-USpdfdocs.tar.gz
Patch1: rpm-pgsql-%{version}.patch
Patch2: rpm-multilib-%{version}.patch
Patch3: postgresql-%{version}-tighten.patch
Patch4: postgresql-ppc64.patch
Patch5: postgresql-plperl.patch
Patch6: postgresql-7.3.4-src-tutorial.patch
Patch7: postgresql-7.3.4-s390-pic.patch
Buildrequires: perl glibc-devel bison flex
Prereq: /sbin/ldconfig initscripts
%if %python
BuildPrereq: python-devel
%endif
%if %tcl
BuildPrereq: tcl
#Buildrequires: tcl-devel
%endif
%if %tkpkg
BuildPrereq: tk
%endif
BuildPrereq: readline-devel
BuildPrereq: zlib-devel >= 1.0.4
%if %ssl
BuildPrereq: openssl-devel
%endif
%if %kerberos
BuildPrereq: krb5-devel
%endif
%if %nls
BuildPrereq: gettext >= 0.10.35
%endif

%if %pam
%if %non6xpamdeps
BuildPrereq: pam-devel
%endif
%endif

Url: http://www.postgresql.org/ 
Obsoletes: postgresql-clients
Obsoletes: postgresql-perl
Obsoletes: postgresql-tk
Buildroot: %{_tmppath}/%{name}-%{version}-root

# This is the PostgreSQL Global Development Group Official RPMset spec file,
# or a derivative thereof.
# Copyright 2001 Lamar Owen <lamar@postgresql.org> <lamar.owen@wgcr.org>
# and others listed.

# Major Contributors:
# ---------------
# Lamar Owen
# Trond Eivind Glomsrd <teg@redhat.com>
# Thomas Lockhart
# Reinhard Max
# Karl DeBisschop
# Peter Eisentraut
# Joe Conway
# and others in the Changelog....

# This spec file and ancilliary files are licensed in accordance with 
# The PostgreSQL license.

# On top of this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line:
# rpm --define 'packagename 1' .... to force the package to build.
# rpm --define 'packagename 0' .... to force the package NOT to build.
# The base package, the lib package, the devel package, and the server package always get built.


%description
PostgreSQL is an advanced Object-Relational database management system
(DBMS) that supports almost all SQL constructs (including
transactions, subselects and user-defined types and functions). The
postgresql package includes the client programs and libraries that
you'll need to access a PostgreSQL DBMS server.  These PostgreSQL
client programs are programs that directly manipulate the internal
structure of PostgreSQL databases on a PostgreSQL server. These client
programs can be located on the same machine with the PostgreSQL
server, or may be on a remote machine which accesses a PostgreSQL
server over a network connection. This package contains the docs
in HTML for the whole package, as well as command-line utilities for
managing PostgreSQL databases on a PostgreSQL server. 

If you want to manipulate a PostgreSQL database on a remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql-server package.

%package libs
Summary: The shared libraries required for any PostgreSQL clients.
Group: Applications/Databases
#XXX should not be needed:
#Provides: libpq.so.3 libpq.so.3.0
Provides: libpq.so

%description libs
The postgresql-libs package provides the essential shared libraries for any 
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package server
Summary: The programs needed to create and run a PostgreSQL server.
Group: Applications/Databases
Prereq: /usr/sbin/useradd /sbin/chkconfig 
Requires: postgresql = %{version} libpq.so
Conflicts: postgresql < 7.3

%description server
The postgresql-server package includes the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.  PostgreSQL is an advanced
Object-Relational database management system (DBMS) that supports
almost all SQL constructs (including transactions, subselects and
user-defined types and functions). You should install
postgresql-server if you want to create and maintain your own
PostgreSQL databases and/or your own PostgreSQL server. You also need
to install the postgresql package.


%package docs
Summary: Extra documentation for PostgreSQL
Group: Applications/Databases
%description docs
The postgresql-docs package includes the SGML source for the documentation
as well as the documentation in PDF format and some extra documentation.
Install this package if you want to help with the PostgreSQL documentation
project, or if you want to generate printed documentation.

%package contrib
Summary: Contributed source and binaries distributed with PostgreSQL
Group: Applications/Databases
Requires: postgresql = %{version}
%description contrib
The postgresql-contrib package contains contributed packages that are
included in the PostgreSQL distribution.


%package devel
Summary: PostgreSQL development header files and libraries.
Group: Development/Libraries
Requires: postgresql-libs = %{version}

%description devel
The postgresql-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server and the ecpg Embedded C
Postgres preprocessor. You need to install this package if you want to
develop applications which will interact with a PostgreSQL server. If
you're installing postgresql-server, you need to install this
package.

#------------
%if %pls
%package pl
Summary: The PL procedural languages for PostgreSQL.
Group: Applications/Databases
Requires: postgresql = %{version}
PreReq: postgresql-server = %{version}

%description pl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-pl package contains the the PL/Perl, PL/Tcl, and PL/Python
procedural languages for the backend.  PL/Pgsql is part of the core server package.
%endif

#------------
%if %tcl
%package tcl
Summary: A Tcl client library for PostgreSQL.
Group: Applications/Databases
Requires: tcl >= 8.0

%description tcl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-tcl package contains the libpgtcl client library,
the pg-enhanced pgtclsh,and the pg-enhanced tksh, if so configured at buildtime.
%endif

#------------
%if %python
%package python
Summary: Development module for Python code to access a PostgreSQL DB.
Group: Applications/Databases
Requires: python mx
Conflicts: python < %pyver, python >= %pynextver


%description python
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-python package includes a module for
developers to use when writing Python code for accessing a PostgreSQL
database.
%endif

#----------
%if %jdbc
%package jdbc
Summary: Files needed for Java programs to access a PostgreSQL database.
Group: Applications/Databases

%description jdbc
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-jdbc package includes the .jar file needed for
Java programs to access a PostgreSQL database.
%endif

#------------
%if %test
%package test
Summary: The test suite distributed with PostgreSQL.
Group: Applications/Databases
Requires: postgresql = %{version}
PreReq: postgresql-server = %{version}

%description test
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-test package includes the sources and pre-built
binaries of various tests for the PostgreSQL database management
system, including regression tests and benchmarks.
%endif

%define __perl_requires %{SOURCE16}

%prep
%setup -q 
pushd doc
tar zxf postgres.tar.gz
popd
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
autoconf
pushd doc
tar -zcf postgres.tar.gz *.html catalogs.gif connections.gif stylesheet.css
rm -f *.html catalogs.gif connections.gif stylesheet.css
popd

cp -p %{SOURCE17} .
tar zxf %{SOURCE17}

%build

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
%if %kerberos
CPPFLAGS="${CPPFLAGS} -I%{_includedir}/et" ; export CPPFLAGS
CFLAGS="${CFLAGS} -I%{_includedir}/et" ; export CFLAGS
%endif

# Strip out -ffast-math from CFLAGS....

CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
export LIBNAME=%{_lib}
%configure --disable-rpath \
%if %beta
	--enable-debug \
	--enable-cassert \
%endif
%if %plperl
	--with-perl \
%endif
%if %tcl
	--with-tcl \
	--with-tclconfig=%{_libdir} \
%endif
%if %tkpkg
	--with-tkconfig=%{_libdir} \
%else
	--without-tk \
%endif
%if %python
	--with-python \
%endif
%if %ssl
	--with-openssl \
%endif
%if %pam
	--with-pam \
%endif
%if %kerberos
	--with-krb5 \
%endif
%if %nls
	--enable-nls \
%endif
	--sysconfdir=/etc/sysconfig/pgsql \
	--datadir=/usr/share/pgsql \
	--with-docdir=%{_docdir}

make all
make -C contrib all

%if %test
	pushd src/test
	make all
	popd
%endif

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
make -C contrib DESTDIR=$RPM_BUILD_ROOT install

# install dev headers.

make DESTDIR=$RPM_BUILD_ROOT install-all-headers

# copy over Makefile.global to the include dir....
install -m755 src/Makefile.global $RPM_BUILD_ROOT/usr/include/pgsql

%if %jdbc
	# Java/JDBC
	# The user will have to set a CLASSPATH to find it here, but not sure where else to put it...

	# JDBC jars 
	install -m 755 %{SOURCE8} $RPM_BUILD_ROOT/usr/share/pgsql
	install -m 755 %{SOURCE9} $RPM_BUILD_ROOT/usr/share/pgsql
	install -m 755 %{SOURCE10} $RPM_BUILD_ROOT/usr/share/pgsql

%endif

if [ -d /etc/rc.d/init.d ]
then
	install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
	install -m 755 %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/postgresql
fi


# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 $RPM_BUILD_ROOT/var/lib/pgsql/data

# backups of data go here...
install -d -m 700 $RPM_BUILD_ROOT/var/lib/pgsql/backups

# postgres' .bash_profile
install -m 644 %{SOURCE15} $RPM_BUILD_ROOT/var/lib/pgsql/.bash_profile

# Create the multiple postmaster startup directory
install -d -m 700 $RPM_BUILD_ROOT/etc/sysconfig/pgsql


%if %test
	# tests. There are many files included here that are unnecessary, but include
	# them anyway for completeness.
	mkdir -p $RPM_BUILD_ROOT/usr/lib/pgsql/test
	cp -a src/test/regress $RPM_BUILD_ROOT/usr/lib/pgsql/test
	install -m 0755 contrib/spi/refint.so $RPM_BUILD_ROOT/usr/lib/pgsql/test/regress
	install -m 0755 contrib/spi/autoinc.so $RPM_BUILD_ROOT/usr/lib/pgsql/test/regress
	pushd  $RPM_BUILD_ROOT/usr/lib/pgsql/test/regress/
	strip *.so
	popd
%endif

# Fix some more documentation
# gzip doc/internals.ps
cp %{SOURCE6} README.rpm-dist
mv $RPM_BUILD_ROOT%{_docdir}/postgresql/html doc
rm -rf $RPM_BUILD_ROOT%{_docdir}/postgresql
%if %tkpkg
%else
rm -rf $RPM_BUILD_ROOT%{_mandir}/man1/pgtksh.*
%endif

%find_lang libpq
%find_lang pg_dump
%find_lang postgres
%find_lang psql
%find_lang pg_resetxlog
%find_lang pg_controldata

cat libpq.lang > libpq.lst
cat psql.lang pg_dump.lang > main.lst
cat postgres.lang pg_resetxlog.lang pg_controldata.lang > server.lst

%post libs -p /sbin/ldconfig 
%postun libs -p /sbin/ldconfig 

%pre server
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -n -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :
touch /var/log/pgsql
chown postgres.postgres /var/log/pgsql
chmod 0700 /var/log/pgsql

%post server
chkconfig --add postgresql
/sbin/ldconfig

%preun server
if [ $1 = 0 ] ; then
	chkconfig --del postgresql
fi

%postun server
/sbin/ldconfig 
if [ $1 -ge 1 ]; then
  /sbin/service postgresql condrestart >/dev/null 2>&1
fi
if [ $1 = 0 ] ; then
	userdel postgres >/dev/null 2>&1 || :
	groupdel postgres >/dev/null 2>&1 || : 
fi

%if %tcl
%post -p /sbin/ldconfig   tcl
%postun -p /sbin/ldconfig   tcl
%endif

%if %pls
%post -p /sbin/ldconfig   pl
%postun -p /sbin/ldconfig   pl
%endif

%if %test
%post test
chown -R postgres.postgres /usr/share/pgsql/test >/dev/null 2>&1 || :
%endif

%clean
rm -rf $RPM_BUILD_ROOT

# FILES section.

%files -f main.lst
%defattr(-,root,root)
%doc doc/FAQ doc/KNOWN_BUGS doc/MISSING_FEATURES doc/README* 
%doc COPYRIGHT README HISTORY doc/bug.template
%doc README.rpm-dist
%doc doc/html
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createlang
%{_bindir}/createuser
%{_bindir}/dropdb
%{_bindir}/droplang
%{_bindir}/dropuser
%{_bindir}/pg_dump
%{_bindir}/pg_dumpall
%{_bindir}/pg_encoding
%{_bindir}/pg_id
%{_bindir}/pg_restore
%{_bindir}/psql
%{_bindir}/vacuumdb
%{_mandir}/man1/clusterdb.*
%{_mandir}/man1/createdb.*
%{_mandir}/man1/createlang.*
%{_mandir}/man1/createuser.*
%{_mandir}/man1/dropdb.*
%{_mandir}/man1/droplang.*
%{_mandir}/man1/dropuser.*
%{_mandir}/man1/pg_dump.*
%{_mandir}/man1/pg_dumpall.*
%{_mandir}/man1/pg_restore.*
%{_mandir}/man1/psql.*
%{_mandir}/man1/vacuumdb.*
%{_mandir}/man7/*

%files docs
%defattr(-,root,root)
%doc doc/src/*
%doc *-US.pdf
%doc src/tutorial

%files contrib
%defattr(-,root,root)
%{_libdir}/pgsql/_int.so
%{_libdir}/pgsql/array_iterator.so
%{_libdir}/pgsql/autoinc.so
%{_libdir}/pgsql/btree_gist.so
%{_libdir}/pgsql/chkpass.so
%{_libdir}/pgsql/cube.so
%{_libdir}/pgsql/dblink.so
%{_libdir}/pgsql/dbsize.so
%{_libdir}/pgsql/earthdistance.so
%{_libdir}/pgsql/fti.so
%{_libdir}/pgsql/fuzzystrmatch.so
%{_libdir}/pgsql/insert_username.so
%{_libdir}/pgsql/int_aggregate.so
%{_libdir}/pgsql/isbn_issn.so
%{_libdir}/pgsql/lo.so
%{_libdir}/pgsql/ltree.so
%{_libdir}/pgsql/misc_utils.so
%{_libdir}/pgsql/moddatetime.so
%{_libdir}/pgsql/noup.so
%{_libdir}/pgsql/pending.so
%{_libdir}/pgsql/pgcrypto.so
%{_libdir}/pgsql/pgstattuple.so
%{_libdir}/pgsql/refint.so
%{_libdir}/pgsql/rserv.so
%{_libdir}/pgsql/rtree_gist.so
%{_libdir}/pgsql/seg.so
%{_libdir}/pgsql/string_io.so
%{_libdir}/pgsql/tablefunc.so
%{_libdir}/pgsql/timetravel.so
%{_libdir}/pgsql/tsearch.so
%{_libdir}/pgsql/user_locks.so
%{_datadir}/pgsql/contrib/
%{_bindir}/dbf2pg
%{_bindir}/findoidjoins
%{_bindir}/make_oidjoins_check
%{_bindir}/fti.pl
%{_bindir}/oid2name
%{_bindir}/pg_dumplo
%{_bindir}/pg_logger
%{_bindir}/pgbench
%{_bindir}/RservTest
%{_bindir}/MasterInit
%{_bindir}/MasterAddTable
%{_bindir}/Replicate
%{_bindir}/MasterSync
%{_bindir}/CleanLog
%{_bindir}/SlaveInit
%{_bindir}/SlaveAddTable
%{_bindir}/GetSyncID
%{_bindir}/PrepareSnapshot
%{_bindir}/ApplySnapshot
%{_bindir}/InitRservTest
%{_bindir}/vacuumlo
%doc contrib/*/README.* contrib/spi/*.example

%files libs -f libpq.lang
%defattr(-,root,root)
%{_libdir}/libpq.so.*
%{_libdir}/libecpg.so.*

%files server -f server.lst
%defattr(-,root,root)
/etc/rc.d/init.d/postgresql
%dir /etc/sysconfig/pgsql
%{_bindir}/initdb
%{_bindir}/initlocation
%{_bindir}/ipcclean
%{_bindir}/pg_controldata
%{_bindir}/pg_ctl
%{_bindir}/pg_resetxlog
%{_bindir}/postgres
%{_bindir}/postmaster
%{_mandir}/man1/initdb.*
%{_mandir}/man1/initlocation.*
%{_mandir}/man1/ipcclean.*
%{_mandir}/man1/pg_controldata.*
%{_mandir}/man1/pg_ctl.*
%{_mandir}/man1/pg_resetxlog.*
%{_mandir}/man1/postgres.*
%{_mandir}/man1/postmaster.*
%{_datadir}/pgsql/postgres.bki
%{_datadir}/pgsql/postgres.description
%{_datadir}/pgsql/*.sample
%{_libdir}/pgsql/plpgsql.so
%dir %{_libdir}/pgsql
%dir %{_datadir}/pgsql
%attr(700,postgres,postgres) %dir /var/lib/pgsql
%attr(700,postgres,postgres) %dir /var/lib/pgsql/data
%attr(700,postgres,postgres) %dir /var/lib/pgsql/backups
%attr(644,postgres,postgres) %config(noreplace) /var/lib/pgsql/.bash_profile
%{_libdir}/pgsql/*_and_*.so
%{_datadir}/pgsql/conversion_create.sql

%files devel
%defattr(-,root,root)
/usr/include/*
%{_bindir}/ecpg
%{_bindir}/pg_config
%{_libdir}/libpq.so
%{_libdir}/libecpg.so
%{_libdir}/libpq.a
%{_libdir}/libecpg.a
%if %tcl
%{_libdir}/libpgtcl.a
%endif
%{_mandir}/man1/ecpg.*
%{_mandir}/man1/pg_config.*

%if %tcl
%files tcl
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/libpgtcl.so.*
# libpgtcl.so is not in devel because Tcl scripts may load it by that name.
%{_libdir}/libpgtcl.so
%{_bindir}/pgtclsh
%{_mandir}/man1/pgtclsh.*
%if %tkpkg
%{_bindir}/pgtksh
%{_mandir}/man1/pgtksh.*
%endif
%endif

%if %pls
%files pl
%defattr(-,root,root)
%if %plperl
%{_libdir}/pgsql/plperl.so
%endif
%if %pltcl
%{_libdir}/pgsql/pltcl.so
%{_bindir}/pltcl_delmod
%{_bindir}/pltcl_listmod
%{_bindir}/pltcl_loadmod
%{_datadir}/pgsql/unknown.pltcl
%endif
%{_libdir}/pgsql/plpython.so
%endif

%if %python
%files python
%defattr(-,root,root)
%doc src/interfaces/python/README src/interfaces/python/tutorial
%{_libdir}/python%{pyver}/site-packages/_pgmodule.so
%{_libdir}/python%{pyver}/site-packages/*.py
%endif

%if %jdbc
%files jdbc
%defattr(-,root,root)
%{_datadir}/pgsql/pg73jdbc1.jar
%{_datadir}/pgsql/pg73jdbc2.jar
%{_datadir}/pgsql/pg73jdbc3.jar
%endif

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) /usr/lib/pgsql/test/*
%attr(-,postgres,postgres) %dir /usr/lib/pgsql/test
%endif

%changelog
* Thu Sep 04 2003 David Jee <djee@redhat.com> 7.3.4-2
- fix src-tutorial patch handling to include all files in the
  original postgres.tar.gz (*.html catalogs.gif connections.gif
  stylesheet.css)

* Thu Jul 31 2003 David Jee <djee@redhat.com> 7.3.4-1
- initial 7.3.4 build

* Wed Jul 30 2003 Andrew Overholt <overholt@redhat.com> 7.3.3-10
- fix basename call in postgresql.init (courtesy E. Jay Berkenbilt)
- fix x86_64 issues with /usr/lib64 and regression tests
- backout previous lib64 change

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 7.3.3-9
- rebuild for updated krb5 1.3, which moves headers and libs to /usr
- use -fPIC instead of -fpic on s390x to allow the plpython bits to link

* Wed Jul 16 2003 Olga Rodimina <rodimina@redhat.com> 7.3.3-8
- fix tutorial location
- modify tutorial patch to be 7.3.3-specific

* Mon Jul 14 2003 Chip Turner <cturner@redhat.com>
- rebuild for new perl 5.8.1

* Fri Jul 11 2003 Olga Rodimina <rodimina@redhat.com> 7.3.3-6
- add src/tutorial to -docs package [Bug #54711]
- add postgresql-src-tutorial.patch [Bug #54711]
- postgresql-src-tutorial.patch builds src/tutorial before
  installing and corrects entry specifying path to tutorial in 
  tutorial-sql.html

* Mon Jul 07 2003 Kim Ho <kho@redhat.com> 7.3.3-5
- add patch to use rpath when creating plperl [Bug #83000]
- add Buildrequires: tcl-devel for libpgtcl --overholt

* Fri Jun 13 2003 Andrew Overholt <overholt@redhat.com> 7.3.3-4
- add PDF docs to -docs package [Bug #91941]

* Wed Jun 04 2003 Andrew Overholt <overholt@redhat.com> 7.3.3-3
- remove PGOPTS from init script [Bug #91943]
- fix system startup 'S90postgresql' issue [Bug #91943]

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 26 2003 Andrew Overholt <overholt@redhat.com> 7.3.3-1
- initial 7.3.3 build

* Thu May 22 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- remove libpq.so.2*

* Wed Apr 16 2003 Andrew Overholt <overholt@redhat.com> 7.3.2-4
- Obsolete postgresql-perl and postgresql-tk [Bugzilla #79814]

* Mon Feb 17 2003 Elliot Lee <sopwith@redhat.com> 7.3.2-4
- Add ppc64 patch

* Fri Feb 14 2003 Andrew Overholt <overholt@redhat.com> 7.3.2-3
- Remove pltcl.so from postgresql-tcl and plpython.so from postgresql-server.
  [Bugzilla #83906]

* Wed Feb 12 2003 Andrew Overholt <overholt@redhat.com> 7.3.2-2
- Fix typo in pg_hba.conf tighten patch.  [Bugzilla #81366]

* Wed Feb 5 2003 Andrew Overholt <overholt@redhat.com> 7.3.2-1
- Initial 7.3.1 build.
- Add bison and flex to BuildRequires line.  [Bugzilla #83553]

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan 09 2003 Elliot Lee <sopwith@redhat.com> 7.3.1-5
- Rebuild for newer libssl
- Add patch4 (isblank.patch) to make it all build

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 7.3.1-4
- use internal dep generator.    

* Fri Jan 3 2003 Andrew Overholt <overholt@redhat.com> 7.3.1-3
- Remove spurious PreReq line

* Fri Jan 3 2003 Andrew Overholt <overholt@redhat.com> 7.3.1-2
- Rebuild with new 7.3.1 tarball
- Remove obsoletes postgresql-perl line (should have been postgresql-plperl)
  as we did not have that package previously

* Wed Dec 18 2002 Andrew Overholt <overholt@redhat.com> 7.3.1-1
- Initial 7.3.1 build.

* Tue Dec 17 2002 Nalin Dahyabhai <nalin@redhat.com> 7.3-6
- Make postgresql-pl obsolete postgresql-perl, not postgresql-plperl

* Fri Dec 13 2002 Andrew Overholt <overholt@redhat.com>
- Remove perl(Pg) dependency
- Bash profile PGDATA fix
- Updated initscript to new community version

* Tue Dec 10 2002 Andrew Overholt <overholt@redhat.com>
- Upgrade to 7.3 community spec file.
- Add patch to use with multilib.
- Change explicit path names to use RPM macros (multilib).
- Add security patch.

* Thu Dec 05 2002 Lamar Owen <lamar.owen@ramifordistat.net>
- 7.3-2PGDG
- Fix typo in initscript.  Argh!!

* Wed Dec 04 2002 Lamar Owen <lamar.owen@ramifordistat.net>
- 7.3-0.5PGDG
- Jerk out all perl client stuff and kludgage
- Rename plperl subpackage to a pl subpackage containing all but PL/Pgsql PL's
- Eliminate locale and multibyte explicit enables -- they are both defaults now
- Eliminate pgaccess code; it's not a part of the main tarball anymore
- Eliminate ODBC stuff -- it's also separate now.  Use unixODBC instead.
- Eliminated separate tk client package -- rolled the tk client into the tcl client.
- Moved pltcl into the pl subpackage.
- Added plpython to the pl subpackage.
- /etc/sysconfig/pgsql is sysconfdir for multiple postmaster startup.


* Mon Dec 02 2002 Lamar Owen <lamar.owen@ramifordistat.net>
- 7.3-0.1PGDG (not released)
- Integrate 7.3 jar's courtesy Joe Conway
- Integrate multi-postmaster initscript courtesy Karl DeBisschop
- Some renames and restructures.
- Stripped out the last dregs of the postgresql-dump migration script.
- Conflicts with less than 7.3.
