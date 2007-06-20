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
# This is the PostgreSQL Global Development Group Official RPMset spec file,
# or a derivative thereof.
# Copyright 2003 Lamar Owen <lowen@pari.edu> <lamar.owen@wgcr.org>
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
# Andrew Overholt
# David Jee
# Kaj J. Niemi
# Sander Steffann
# Tom Lane
# and others in the Changelog....

# This spec file and ancilliary files are licensed in accordance with 
# The PostgreSQL license.

# In this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line:
# rpm --define 'packagename 1' .... to force the package to build.
# rpm --define 'packagename 0' .... to force the package NOT to build.
# The base package, the lib package, the devel package, and the server package always get built.

#build7x, build8, and build9 similar
%{?build7x:%define tcldevel 0}
%{?build7x:%define aconfver autoconf-2.53}
%{?build8:%define build89 1}
%{?build8:%define tcldevel 0}
%{?build9:%define build89 1}

%define beta 0
%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

%{!?aconfver:%define aconfver autoconf}

%{!?tcldevel:%define tcldevel 1}
%{!?test:%define test 1}
%{!?plpython:%define plpython 1}
%{!?pltcl:%define pltcl 1}
%{!?plperl:%define plperl 1}
%{!?python:%define python 1}
%{!?tcl:%define tcl 1}
%{!?ssl:%define ssl 1}
%{!?kerberos:%define kerberos 1}
%{!?nls:%define nls 1}
%{!?xml:%define xml 1}
%{!?pam:%define pam 1}
%{!?pgfts:%define pgfts 1}
%{!?runselftest:%define runselftest 1}

# Python major version.
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}


Summary: PostgreSQL client programs and libraries
Name: postgresql
Version: 8.2.4
Release: 2%{?dist}
License: BSD
Group: Applications/Databases
Url: http://www.postgresql.org/ 

Source0: ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
Source3: postgresql.init
Source4: Makefile.regress
Source5: pg_config.h
Source6: README.rpm-dist
Source14: postgresql.pam
Source15: postgresql-bashprofile
Source16: filter-requires-perl-Pg.sh
Source17: http://www.postgresql.org/docs/manuals/postgresql-8.2.1-US.pdf
Source18: ftp://ftp.pygresql.org/pub/distrib/PyGreSQL-3.8.1.tgz
Source19: http://pgfoundry.org/projects/pgtclng/pgtcl1.5.3.tar.gz
Source20: http://pgfoundry.org/projects/pgtclng/pgtcldocs-20060909.zip

Patch1: rpm-pgsql.patch
Patch3: postgresql-logging.patch
Patch4: postgresql-test.patch
Patch5: pgtcl-no-rpath.patch
Patch6: postgresql-perl-rpath.patch
Patch8: postgresql-prefer-ncurses.patch

BuildRequires: perl glibc-devel bison flex autoconf
Prereq: /sbin/ldconfig initscripts

%if %python || %plpython
BuildRequires: python-devel
%endif

%if %tcl || %pltcl
BuildRequires: tcl
%if %tcldevel
BuildRequires: tcl-devel
%endif
%endif

BuildRequires: readline-devel
BuildRequires: zlib-devel >= 1.0.4

%if %ssl
BuildRequires: openssl-devel
%endif

%if %kerberos
BuildRequires: krb5-devel
BuildRequires: e2fsprogs-devel
%endif

%if %nls
BuildRequires: gettext >= 0.10.35
%endif

%if %xml
BuildRequires: libxml2-devel libxslt-devel
%endif

%if %pam
BuildRequires: pam-devel
%endif

Obsoletes: postgresql-clients
Obsoletes: postgresql-perl
Obsoletes: postgresql-tk
Obsoletes: rh-postgresql

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root

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
Summary: The shared libraries required for any PostgreSQL clients
Group: Applications/Databases
Provides: libpq.so
Obsoletes: rh-postgresql-libs

%description libs
The postgresql-libs package provides the essential shared libraries for any 
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package server
Summary: The programs needed to create and run a PostgreSQL server
Group: Applications/Databases
Prereq: /usr/sbin/useradd /sbin/chkconfig 
Prereq: postgresql = %{version}-%{release} libpq.so
Obsoletes: rh-postgresql-server

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
Prereq: postgresql = %{version}-%{release}
Obsoletes: rh-postgresql-docs

%description docs
The postgresql-docs package includes some additional documentation for
PostgreSQL.  Currently, this includes the main documentation in PDF format,
the FAQ, and source files for the PostgreSQL tutorial.


%package contrib
Summary: Contributed source and binaries distributed with PostgreSQL
Group: Applications/Databases
Prereq: postgresql = %{version}-%{release}
Obsoletes: rh-postgresql-contrib

%description contrib
The postgresql-contrib package contains contributed packages that are
included in the PostgreSQL distribution.


%package devel
Summary: PostgreSQL development header files and libraries
Group: Development/Libraries
Prereq: postgresql = %{version}-%{release}
Requires: postgresql-libs = %{version}-%{release}
Obsoletes: rh-postgresql-devel

%description devel
The postgresql-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server and the ecpg Embedded C
Postgres preprocessor. You need to install this package if you want to
develop applications which will interact with a PostgreSQL server.

#------------
%if %plperl
%package plperl
Summary: The Perl procedural language for PostgreSQL
Group: Applications/Databases
PreReq: postgresql = %{version}-%{release}
PreReq: postgresql-server = %{version}-%{release}
Obsoletes: rh-postgresql-pl
Obsoletes: postgresql-pl

%description plperl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-plperl package contains the PL/Perl
procedural language for the backend.
%endif

#------------
%if %plpython
%package plpython
Summary: The Python procedural language for PostgreSQL
Group: Applications/Databases
PreReq: postgresql = %{version}-%{release}
PreReq: postgresql-server = %{version}-%{release}
Obsoletes: rh-postgresql-pl
Obsoletes: postgresql-pl

%description plpython
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-plpython package contains the PL/Python
procedural language for the backend.
%endif

#------------
%if %pltcl
%package pltcl
Summary: The Tcl procedural language for PostgreSQL
Group: Applications/Databases
PreReq: postgresql = %{version}-%{release}
PreReq: postgresql-server = %{version}-%{release}
Obsoletes: rh-postgresql-pl
Obsoletes: postgresql-pl

%description pltcl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-pltcl package contains the PL/Tcl
procedural language for the backend.
%endif

#------------
%if %tcl
%package tcl
Summary: A Tcl client library for PostgreSQL
Group: Applications/Databases
Requires: libpq.so
Requires: tcl >= 8.3
Obsoletes: rh-postgresql-tcl

%description tcl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-tcl package contains the Pgtcl client library
and its documentation.
%endif

#------------
%if %python
%package python
Summary: Development module for Python code to access a PostgreSQL DB
Group: Applications/Databases
Requires: libpq.so
Requires: python mx
Obsoletes: rh-postgresql-python

%description python
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-python package includes a module for
developers to use when writing Python code for accessing a PostgreSQL
database.
%endif

#----------
%if %test
%package test
Summary: The test suite distributed with PostgreSQL
Group: Applications/Databases
PreReq: postgresql = %{version}-%{release}
PreReq: postgresql-server = %{version}-%{release}
Obsoletes: rh-postgresql-test

%description test
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-test package includes the sources and pre-built
binaries of various tests for the PostgreSQL database management
system, including regression tests and benchmarks.
%endif

%define __perl_requires %{SOURCE16}

%prep
%setup -q 
%patch1 -p1
%patch3 -p1
%patch4 -p1
# patch5 is applied later
%patch6 -p1
%patch8 -p1

#call autoconf 2.53 or greater
%aconfver

cp -p %{SOURCE17} .

%if %python
   tar xzf %{SOURCE18}
   PYGRESQLDIR=`basename %{SOURCE18} .tgz`
   mv $PYGRESQLDIR PyGreSQL
   # Some versions of PyGreSQL.tgz contain wrong file permissions
   chmod 755 PyGreSQL/tutorial
   chmod 644 PyGreSQL/tutorial/*.py
   chmod 755 PyGreSQL/tutorial/advanced.py PyGreSQL/tutorial/basics.py
%endif

%if %tcl
   tar xzf %{SOURCE19}
   PGTCLDIR=`basename %{SOURCE19} .tar.gz`
   mv $PGTCLDIR Pgtcl
   unzip %{SOURCE20}
   PGTCLDOCDIR=`basename %{SOURCE20} .zip`
   mv $PGTCLDOCDIR Pgtcl-docs

   pushd Pgtcl
%patch5 -p1
%aconfver
   popd
%endif

%build

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS

# Strip out -ffast-math from CFLAGS....
CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`

%configure --disable-rpath \
%if %beta
	--enable-debug \
	--enable-cassert \
%endif
%if %plperl
	--with-perl \
%endif
%if %pltcl
	--with-tcl \
	--with-tclconfig=%{_libdir} \
%endif
%if %plpython
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
%if %pgfts
	--enable-thread-safety \
%endif
	--sysconfdir=/etc/sysconfig/pgsql \
	--datadir=/usr/share/pgsql \
	--with-docdir=%{_docdir}

make %{?_smp_mflags} all
make %{?_smp_mflags} -C contrib all
%if %xml
make %{?_smp_mflags} -C contrib/xml2 all
%endif

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{_libdir}/pgsql/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
make %{?_smp_mflags} -C src/tutorial NO_PGXS=1 all
rm -f src/tutorial/GNUmakefile

%if %runselftest
	pushd src/test/regress
	make all
	make MAX_CONNECTIONS=5 check
	make clean
	popd
%endif

%if %test
	pushd src/test/regress
	make RPMTESTING=1 all
	popd
%endif

%if %python
   PYTHON=/usr/bin/python
   python_version=`${PYTHON} -c "import sys; print sys.version[:3]"`
   python_prefix=`${PYTHON} -c "import sys; print sys.prefix"`
   python_includespec="-I${python_prefix}/include/python${python_version}"

   pushd PyGreSQL

   gcc $CFLAGS -fpic -shared -o _pgmodule.so ${python_includespec} -I../src/interfaces/libpq -I../src/include -L../src/interfaces/libpq -lpq pgmodule.c

   popd
%endif

%if %tcl
   pushd Pgtcl
   # pgtcl's configure only handles one include directory :-(
   ./configure --prefix=/usr \
     --libdir=%{_libdir} \
     --with-tcl=%{_libdir} \
     --with-postgres-include="../src/interfaces/libpq -I../src/include" \
     --with-postgres-lib=../src/interfaces/libpq
   # note: as of pgtcl 1.5.2, its makefile is not parallel-safe
   make all
   popd
%endif

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
make -C contrib DESTDIR=$RPM_BUILD_ROOT install
%if %xml
make -C contrib/xml2 DESTDIR=$RPM_BUILD_ROOT install
%endif

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
case `uname -i` in
  i386 | x86_64 | ppc | ppc64 | s390 | s390x)
    mv $RPM_BUILD_ROOT/usr/include/pg_config.h $RPM_BUILD_ROOT/usr/include/pg_config_`uname -i`.h
    install -m 644 %{SOURCE5} $RPM_BUILD_ROOT/usr/include/
    mv $RPM_BUILD_ROOT/usr/include/pgsql/server/pg_config.h $RPM_BUILD_ROOT/usr/include/pgsql/server/pg_config_`uname -i`.h
    install -m 644 %{SOURCE5} $RPM_BUILD_ROOT/usr/include/pgsql/server/
    ;;
  *)
    ;;
esac

install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/pgsql/tutorial
cp src/tutorial/* $RPM_BUILD_ROOT%{_libdir}/pgsql/tutorial

%if %tcl
	install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/Pgtcl
	cp Pgtcl/pkgIndex.tcl $RPM_BUILD_ROOT%{_libdir}/Pgtcl
	cp Pgtcl/libpgtcl*.so $RPM_BUILD_ROOT%{_libdir}/Pgtcl
%endif

if [ -d /etc/rc.d/init.d ]
then
	install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
	sed 's/^PGVERSION=.*$/PGVERSION=%{version}/' <%{SOURCE3} >postgresql.init
	install -m 755 postgresql.init $RPM_BUILD_ROOT/etc/rc.d/init.d/postgresql
fi

%if %pam
if [ -d /etc/pam.d ]
then
	install -d $RPM_BUILD_ROOT/etc/pam.d
	install -m 644 %{SOURCE14} $RPM_BUILD_ROOT/etc/pam.d/postgresql
fi
%endif

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 $RPM_BUILD_ROOT/var/lib/pgsql/data

# backups of data go here...
install -d -m 700 $RPM_BUILD_ROOT/var/lib/pgsql/backups

# postgres' .bash_profile
install -m 644 %{SOURCE15} $RPM_BUILD_ROOT/var/lib/pgsql/.bash_profile

# Create the multiple postmaster startup directory
install -d -m 700 $RPM_BUILD_ROOT/etc/sysconfig/pgsql


%if %test
	# tests. There are many files included here that are unnecessary,
	# but include them anyway for completeness.  We replace the original
	# Makefiles, however.
	mkdir -p $RPM_BUILD_ROOT%{_libdir}/pgsql/test
	cp -a src/test/regress $RPM_BUILD_ROOT%{_libdir}/pgsql/test
	install -m 0755 contrib/spi/refint.so $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress
	install -m 0755 contrib/spi/autoinc.so $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress
	pushd  $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress
	strip *.so
	rm -f GNUmakefile Makefile *.o
	popd
	cp %{SOURCE4} $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/Makefile
	chmod 0644 $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/Makefile
%endif

# Fix some more documentation
# gzip doc/internals.ps
cp %{SOURCE6} README.rpm-dist
mv $RPM_BUILD_ROOT%{_docdir}/pgsql/html doc
rm -rf $RPM_BUILD_ROOT%{_docdir}/pgsql

%if %python
   pushd PyGreSQL
   install -m 0755 -d $RPM_BUILD_ROOT%{python_sitearch}
   install -m 0755 _pgmodule.so $RPM_BUILD_ROOT%{python_sitearch}
   install -m 0644 pg.py $RPM_BUILD_ROOT%{python_sitearch}
   install -m 0644 pgdb.py $RPM_BUILD_ROOT%{python_sitearch}
   popd
%endif

%find_lang libpq
%find_lang initdb
%find_lang pg_config
%find_lang pg_ctl
%find_lang pg_dump
%find_lang postgres
%find_lang psql
%find_lang pg_resetxlog
%find_lang pg_controldata
%find_lang pgscripts

cat libpq.lang > libpq.lst
cat pg_config.lang > pg_config.lst
cat initdb.lang pg_ctl.lang psql.lang pg_dump.lang pgscripts.lang > main.lst
cat postgres.lang pg_resetxlog.lang pg_controldata.lang > server.lst

%post libs -p /sbin/ldconfig 
%postun libs -p /sbin/ldconfig 

%pre server
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -n -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

# If we're upgrading from rh-postgresql, we have to repeat the above actions
# after rh-postgresql-server is uninstalled, because its postun script runs
# after our pre script ...
%triggerpostun -n postgresql-server -- rh-postgresql-server
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -n -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

%post server
chkconfig --add postgresql
/sbin/ldconfig

%preun server
if [ $1 = 0 ] ; then
	/sbin/service postgresql condstop >/dev/null 2>&1
	chkconfig --del postgresql
fi

%postun server
/sbin/ldconfig 
if [ $1 -ge 1 ] ; then
	/sbin/service postgresql condrestart >/dev/null 2>&1 || :
fi
if [ $1 = 0 ] ; then
	userdel postgres >/dev/null 2>&1 || :
	groupdel postgres >/dev/null 2>&1 || : 
fi

%if %plperl
%post -p /sbin/ldconfig   plperl
%postun -p /sbin/ldconfig   plperl
%endif

%if %plpython
%post -p /sbin/ldconfig   plpython
%postun -p /sbin/ldconfig   plpython
%endif

%if %pltcl
%post -p /sbin/ldconfig   pltcl
%postun -p /sbin/ldconfig   pltcl
%endif

%if %test
%post test
chown -R postgres:postgres /usr/share/pgsql/test >/dev/null 2>&1 || :
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
%{_bindir}/pg_restore
%{_bindir}/psql
%{_bindir}/reindexdb
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
%{_mandir}/man1/reindexdb.*
%{_mandir}/man1/vacuumdb.*
%{_mandir}/man7/*
%dir %{_libdir}/pgsql

%files docs
%defattr(-,root,root)
%doc doc/src/FAQ
%doc *-US.pdf
%{_libdir}/pgsql/tutorial/

%files contrib
%defattr(-,root,root)
%{_libdir}/pgsql/_int.so
%{_libdir}/pgsql/adminpack.so
%{_libdir}/pgsql/autoinc.so
%{_libdir}/pgsql/btree_gist.so
%{_libdir}/pgsql/chkpass.so
%{_libdir}/pgsql/cube.so
%{_libdir}/pgsql/dblink.so
%{_libdir}/pgsql/earthdistance.so
%{_libdir}/pgsql/fuzzystrmatch.so
%{_libdir}/pgsql/hstore.so
%{_libdir}/pgsql/insert_username.so
%{_libdir}/pgsql/int_aggregate.so
%{_libdir}/pgsql/isn.so
%{_libdir}/pgsql/lo.so
%{_libdir}/pgsql/ltree.so
%{_libdir}/pgsql/moddatetime.so
%{_libdir}/pgsql/pg_buffercache.so
%{_libdir}/pgsql/pg_freespacemap.so
%{_libdir}/pgsql/pg_trgm.so
%{_libdir}/pgsql/pgcrypto.so
%{_libdir}/pgsql/pgrowlocks.so
%{_libdir}/pgsql/pgstattuple.so
%{_libdir}/pgsql/refint.so
%{_libdir}/pgsql/seg.so
%{_libdir}/pgsql/sslinfo.so
%{_libdir}/pgsql/tablefunc.so
%{_libdir}/pgsql/timetravel.so
%{_libdir}/pgsql/tsearch2.so
%if %xml
%{_libdir}/pgsql/pgxml.so
%endif
%{_datadir}/pgsql/contrib/
%{_bindir}/oid2name
%{_bindir}/pgbench
%{_bindir}/vacuumlo
%doc contrib/*/README.* contrib/spi/*.example

%files libs -f libpq.lang
%defattr(-,root,root)
%{_libdir}/libpq.so.*
%{_libdir}/libecpg.so.*
%{_libdir}/libpgtypes.so.*
%{_libdir}/libecpg_compat.so.*

%files server -f server.lst
%defattr(-,root,root)
/etc/rc.d/init.d/postgresql
%if %pam
%config(noreplace) /etc/pam.d/postgresql
%endif
%attr (755,root,root) %dir /etc/sysconfig/pgsql
%{_bindir}/initdb
%{_bindir}/ipcclean
%{_bindir}/pg_controldata
%{_bindir}/pg_ctl
%{_bindir}/pg_resetxlog
%{_bindir}/postgres
%{_bindir}/postmaster
%{_mandir}/man1/initdb.*
%{_mandir}/man1/ipcclean.*
%{_mandir}/man1/pg_controldata.*
%{_mandir}/man1/pg_ctl.*
%{_mandir}/man1/pg_resetxlog.*
%{_mandir}/man1/postgres.*
%{_mandir}/man1/postmaster.*
%{_datadir}/pgsql/postgres.bki
%{_datadir}/pgsql/postgres.description
%{_datadir}/pgsql/postgres.shdescription
%{_datadir}/pgsql/system_views.sql
%{_datadir}/pgsql/*.sample
%{_datadir}/pgsql/timezone/
%{_datadir}/pgsql/timezonesets/
%{_libdir}/pgsql/plpgsql.so
%dir %{_datadir}/pgsql
%attr(700,postgres,postgres) %dir /var/lib/pgsql
%attr(700,postgres,postgres) %dir /var/lib/pgsql/data
%attr(700,postgres,postgres) %dir /var/lib/pgsql/backups
%attr(644,postgres,postgres) %config(noreplace) /var/lib/pgsql/.bash_profile
%{_libdir}/pgsql/*_and_*.so
%{_datadir}/pgsql/conversion_create.sql
%{_datadir}/pgsql/information_schema.sql
%{_datadir}/pgsql/sql_features.txt

%files devel -f pg_config.lst
%defattr(-,root,root)
/usr/include/*
%{_bindir}/ecpg
%{_bindir}/pg_config
%{_libdir}/libpq.so
%{_libdir}/libecpg.so
%{_libdir}/libpq.a
%{_libdir}/libecpg.a
%{_libdir}/libecpg_compat.so
%{_libdir}/libecpg_compat.a
%{_libdir}/libpgport.a
%{_libdir}/libpgtypes.so
%{_libdir}/libpgtypes.a
%{_libdir}/pgsql/pgxs/
%{_mandir}/man1/ecpg.*
%{_mandir}/man1/pg_config.*

%if %tcl
%files tcl
%defattr(-,root,root)
%{_libdir}/Pgtcl/
%doc Pgtcl-docs/*
%endif

%if %plperl
%files plperl
%defattr(-,root,root)
%{_libdir}/pgsql/plperl.so
%endif

%if %pltcl
%files pltcl
%defattr(-,root,root)
%{_libdir}/pgsql/pltcl.so
%{_bindir}/pltcl_delmod
%{_bindir}/pltcl_listmod
%{_bindir}/pltcl_loadmod
%{_datadir}/pgsql/unknown.pltcl
%endif

%if %plpython
%files plpython
%defattr(-,root,root)
%{_libdir}/pgsql/plpython.so
%endif

%if %python
%files python
%defattr(-,root,root)
%doc PyGreSQL/docs/*.txt
%doc PyGreSQL/tutorial
%{python_sitearch}/_pgmodule.so
%{python_sitearch}/*.py
%endif

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) %{_libdir}/pgsql/test/*
%attr(-,postgres,postgres) %dir %{_libdir}/pgsql/test
%endif

%changelog
* Wed Jun 20 2007 Tom Lane <tgl@redhat.com> 8.2.4-2
- Fix oversight in postgresql-test makefile: pg_regress isn't a shell script
  anymore.  Per upstream bug 3398.

* Tue Apr 24 2007 Tom Lane <tgl@redhat.com> 8.2.4-1
- Update to PostgreSQL 8.2.4 for CVE-2007-2138, data loss bugs
Resolves: #237682

* Wed Feb 14 2007 Karsten Hopp <karsten@redhat.com> 8.2.3-2
- rebuild with tcl-8.4

* Wed Feb  7 2007 Tom Lane <tgl@redhat.com> 8.2.3-1
- Update to PostgreSQL 8.2.3 due to regression induced by security fix
Resolves: #227522

* Sun Feb  4 2007 Tom Lane <tgl@redhat.com> 8.2.2-1
- Update to PostgreSQL 8.2.2 to fix CVE-2007-0555, CVE-2007-0556
Related: #225496

* Fri Jan 12 2007 Tom Lane <tgl@redhat.com> 8.2.1-2
- Split -pl subpackage into three new packages to reduce dependencies
  and track upstream project's packaging.

* Wed Jan 10 2007 Tom Lane <tgl@redhat.com> 8.2.1-1
- Update to PostgreSQL 8.2.1
- Update to pgtcl 1.5.3
- Be sure we link to libncurses, not libtermcap which is disappearing in Fedora

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 8.2.0-2
- rebuild for python 2.5

* Mon Dec  4 2006 Tom Lane <tgl@redhat.com> 8.2.0-1
- Update to PostgreSQL 8.2.0
- Update to PyGreSQL 3.8.1
- Fix chcon arguments in test/regress/Makefile
Related: #201035
- Adjust init script to not fool /etc/rc.d/rc
Resolves: #161470
- Change init script to not do initdb automatically, but require
  manual "service postgresql initdb" for safety.  Per upstream discussions.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 8.1.4-1.1
- rebuild

* Mon May 22 2006 Tom Lane <tgl@redhat.com> 8.1.4-1
- Update to PostgreSQL 8.1.4 (includes fixes for CVE-2006-2313, CVE-2006-2314;
  see bug #192173)
- Update to PyGreSQL 3.8
- Suppress noise from chcon, per bug #187744

* Mon Mar 27 2006 Tom Lane <tgl@redhat.com> 8.1.3-2
- Remove JDBC from this build; we will package it as separate SRPM

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 8.1.3-1.1
- rebump for build order issues during double-long bump

* Mon Feb 13 2006 Tom Lane <tgl@redhat.com> 8.1.3-1
- Update to PostgreSQL 8.1.3 (fixes bug #180617, CVE-2006-0553)
- Update to jdbc driver build 405
- Modify multilib header hack to not break non-RH arches, per bug #177564

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 8.1.2-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan  9 2006 Tom Lane <tgl@redhat.com> 8.1.2-1
- Update to PostgreSQL 8.1.2
- Repair extraneous quote in pgtcl configure script ... odd that bash
  didn't use to spit up on this.

* Thu Dec 15 2005 Tom Lane <tgl@redhat.com> 8.1.1-3
- fix pg_config.h for 64-bit and ppc platforms
- update Makefile.regress (needs to --load-language=plpgsql)

* Wed Dec 14 2005 Tom Lane <tgl@redhat.com> 8.1.1-2
- oops, looks like we want uname -i not uname -m

* Wed Dec 14 2005 Tom Lane <tgl@redhat.com> 8.1.1-1
- Update to PostgreSQL 8.1.1
- Make pg_config.h architecture-independent for multilib installs;
  put the original pg_config.h into pg_config_$ARCH.h

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 12 2005 Tom Lane <tgl@redhat.com> 8.1.0-4
- Update included PDF-format manual to 8.1.

* Wed Nov  9 2005 Tom Lane <tgl@redhat.com> 8.1.0-3
- Rebuild due to openssl library update.

* Wed Nov  9 2005 Tom Lane <tgl@redhat.com> 8.1.0-2
- Rebuild due to openssl library update.

* Mon Nov  7 2005 Tom Lane <tgl@redhat.com> 8.1.0-1
- Update to PostgreSQL 8.1.0, PyGreSQL 3.7, and jdbc driver build 404
- Fix PAM config file (must have account not only auth) (bug #167040)
- Add BuildPrereq: libxslt-devel (bug #170141)
- Sync with PGDG SRPM as much as feasible

* Fri Oct 14 2005 Tomas Mraz <tmraz@redhat.com>
- use include instead of pam_stack in pam config

* Tue Oct  4 2005 Tom Lane <tgl@redhat.com> 8.0.4-2
- Add rpath to plperl.so (bug #162198)

* Tue Oct  4 2005 Tom Lane <tgl@redhat.com> 8.0.4-1
- Update to PostgreSQL 8.0.4, PyGreSQL 3.6.2, and jdbc driver build 312
- Adjust pgtcl link command to ensure it binds to correct libpq (bug #166665)
- Remove obsolete Conflicts: against other python versions (bug #166754)
- Add /etc/pam.d/postgresql (bug #167040)
- Include contrib/xml2 in build (bug #167492)

* Tue May 10 2005 Tom Lane <tgl@redhat.com> 8.0.3-1
- Update to PostgreSQL 8.0.3 (includes security and data-loss fixes; see
  bz#156727, CAN-2005-1409, CAN-2005-1410)
- Update to jdbc driver build 311
- Recreate postgres user after superseding an rh-postgresql install (bug #151911)
- Ensure postgresql server is restarted if running during an upgrade

* Thu Apr 14 2005 Florian La Roche <laroche@redhat.com> 8.0.2-2
- rebuild for postgresql-tcl

* Tue Apr 12 2005 Tom Lane <tgl@redhat.com> 8.0.2-1
- Update to PostgreSQL 8.0.2.

* Fri Mar 11 2005 Tom Lane <tgl@redhat.com> 8.0.1-5
- Remove unwanted rpath specification from pgtcl (bz#150649)

* Wed Mar  2 2005 Tom Lane <tgl@redhat.com> 8.0.1-4
- Attach Obsoletes: declarations for rh-postgresql to subpackages (bz#144435)
- Make Requires: and Prereq: package linkages specify release not only
  version, as per recent mailing list discussion.

* Tue Mar  1 2005 Tomas Mraz <tmraz@redhat.com> 8.0.1-3
- rebuild with openssl-0.9.7e

* Mon Feb 21 2005 Tom Lane <tgl@redhat.com> 8.0.1-2
- Repair improper error message in init script when PGVERSION doesn't match.
- Arrange for auto update of version embedded in init script.

* Sun Jan 30 2005 Tom Lane <tgl@redhat.com> 8.0.1-1
- Update to PostgreSQL 8.0.1.
- Add versionless symlinks to jar files (bz#145744)

* Wed Jan 19 2005 Tom Lane <tgl@redhat.com> 8.0.0-1
- Update to PostgreSQL 8.0.0, PyGreSQL 3.6.1, pgtcl 1.5.2,
  and jdbc driver build 309.
- Extensive cleanout of obsolete cruft in patch set.
- Regression tests are run during RPM build (NOTE: cannot build as root when
  this is enabled).
- Postmaster stderr goes someplace useful, not /dev/null (bz#76503, #103767)
- Make init script return a useful exit status (bz#80782)
- Move docs' tutorial directory to %%{_libdir}/pgsql/tutorial, since it
  includes .so files that surely do not belong under /usr/share.
- Remove useless .sgml files from docs RPM (bz#134450)
- Put regression tests under /usr/lib64 on 64-bit archs, since .so files
  are not architecture-independent.

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 7.4.6-5
- Rebuilt for new readline.

* Tue Jan 11 2005 Dan Walsh <dwalsh@redhat.com> 7.4.6-4
- Add restorecon to postgresql.init in order to restore database to correct
- SELinux context.

* Thu Dec 16 2004 Tom Lane <tgl@redhat.com> 7.4.6-3
- Update to PyGreSQL 3.6 (to fix bug #142711)
- Adjust a few file permissions (bug #142431)
- Assign %%{_libdir}/pgsql to base package instead of -server (bug #74003)

* Mon Nov 15 2004 Tom Lane <tgl@redhat.com> 7.4.6-2
- Rebuild so python components play with python 2.4 (bug 139160)

* Sat Oct 23 2004 Tom Lane <tgl@redhat.com> 7.4.6-1
- Update to PostgreSQL 7.4.6 (bugs 136947, 136949)
- Make init script more paranoid about mkdir step of initializing a new
  database (bugs 136947, 136949)

* Wed Oct 20 2004 Tom Lane <tgl@redhat.com> 7.4.5-4
- Remove contrib/oidjoins stuff from installed fileset; it's of no use
  to ordinary users and has a security issue (bugs 136300, 136301)
- adjust chkconfig priority (bug 128852)

* Tue Oct 05 2004 Tom Lane <tgl@redhat.com> 7.4.5-3
- Solve the stale lockfile problem (bugs 71295, 96981, 134090)
- Use runuser instead of su for SELinux (bug 134588)

* Mon Aug 30 2004 Tom Lane <tgl@redhat.com> 7.4.5-2
- Update to PyGreSQL 3.5.

* Wed Aug 24 2004 Tom Lane <tgl@redhat.com> 7.4.5-1
- Update to PostgreSQL 7.4.5.
- Update JDBC jars to driver build 215.
- Add Obsoletes: entries for rh-postgresql packages, per bug 129278.

* Sat Jul 10 2004 Tom Lane <tgl@redhat.com> 7.4.3-3
- Undo ill-considered chkconfig change that causes server to start
  immediately upon install.  Mea culpa (bug 127552).

* Sat Jul 03 2004 Tom Lane <tgl@redhat.com> 7.4.3-2
- Update JDBC jars to driver build 214.

* Wed Jun 23 2004 Tom Lane <tgl@redhat.com> 7.4.3-1
- Update to PostgreSQL 7.4.3.
- Uninstalling server RPM stops postmaster first, per bug 114846.
- Fix su commands to not assume PG user's shell is sh-like, per bug 124024.
- Fix permissions on postgresql-python doc files, per bug 124822.
- Minor postgresql.init improvements.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 10 2004 Tom Lane <tgl@redhat.com> 7.4.2-1
- Update to PostgreSQL 7.4.2; sync with community SRPM as much as possible.
- Support PGOPTS from /etc/sysconfig/pgsql, per bug 111504.
- Fix permissions on /etc/sysconfig/pgsql, per bug 115278.
- SELinux patch in init file: always su </dev/null, per bug 117901.
- Rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Tom Lane <tgl@redhat.com>
- Update to PostgreSQL 7.4.1.
- Rebuilt

* Tue Feb 24 2004 Tom Lane <tgl@redhat.com>
- Fix chown syntax in postgresql.init also.
- Rebuilt

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com>
- Use ':' instead of '.' as separator for chown.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 9 2004 Lamar Owen <lowen@pari.edu>
- 7.4.1-1PGDG
- Merge Sander Steffann's changes up to 7.4-0.5PGDG
- Proper 7.4.1 JDBC jars this time.
- Patch for no pl/python from Alvaro

* Fri Dec 05 2003 David Jee <djee@redhat.com> 7.4-5
- Rebuild for Perl 5.8.2.

* Mon Dec 01 2003 David Jee <djee@redhat.com> 7.4-4
- Add PyGreSQL patch for deprecated column pg_type.typprtlen [Bug #111263]
- Add headers patch which moves ecpg headers to /usr/include/ecpg
  [Bug #111195]

* Fri Nov 28 2003 David Jee <djee@redhat.com> 7.4-3
- uncomment buildrequires tcl-devel

* Fri Nov 28 2003 David Jee <djee@redhat.com> 7.4-2
- rebuild

* Mon Nov 24 2003 David Jee <djee@redhat.com> 7.4-1
- initial Red Hat build
- move jars to /usr/share/java
- fix rpm-multilib patch to use sysconfig

* Fri Nov 21 2003 Lamar Owen <lowen@pari.edu> <lamar.owen@wgcr.org>
- 7.4-0.1PGDG
- Development JDBC jars in addition to the 7.3 jars; will replace the
- 7.3 jars once 7.4 official jars are released.
- Changed to use the bzip2 source to save a little size.
- Removed some commented out portions of the specfile.
- Removed the 7.3.4 PDF docs.  Will replace with 7.4 PDF's once they
- are ready.

* Tue Nov 18 2003 Kaj J. Niemi <kajtzu@fi.basen.net> 7.4-0.1
- 7.4
- Fixed Patch #1 (now rpm-pgsql-7.4.patch)
- Fixed Patch #2 (now rpm-multilib-7.4.patch):
- Patch #4 is unnecessary (upstream)
- Fixed Patch #6 (now postgresql-7.4-src-tutorial.patch)
- Added Patch #8 (postgresql-7.4-com_err.patch) as com_err()
  is provided by e2fsprogs and CPPFLAGS gets lost somewhere
  inside configure (bad macro?)
- No 7.4 PDF docs available yet (Source #17)
- PyGreSQL is separated from the upstream distribution but
  we include it as usual (Source #18)
- Default to compiling libpq and ECPG as fully thread-safe

- 7.4 Origin.  See previous spec files for previous history. Adapted
- from Red Hat and PGDG's 7.3.4 RPM, directly descended from 
- postgresql-7.3.4-2 as shipped in Fedora Core 1.
