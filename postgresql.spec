# build6x usage: define to 1 to build for RHL6.x.  Don't define at all for others.
%{?build6x:%define kerberos 0}
%{?build6x:%define nls 0}
%{?build6x:%define ssl 0}
#work around the undefined or defined to 1 build 6x interaction with the pam stuff
%{!?build6x:%define non6xpamdeps 1}
%{?build6x:%define non6xpamdeps 0}

%define beta 0

%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}
%{!?perl:%define perl 1}
%{!?tcl:%define tcl 1}
%{!?tkpkg:%define tkpkg 1}
%{!?odbc:%define odbc 1}
%{!?jdbc:%define jdbc 1}
%{!?test:%define test 1}
%{!?python:%define python 1}
%{!?pltcl:%define pltcl 1}
%{?forceplperl:%define plperl %{expand:forceplperl}}
%{!?forceplperl:%define forceplperl 0}
%{!?plperl:%define plperl 0}
%{!?ssl:%define ssl 1}
%{!?kerberos:%define kerberos 1}
%{!?nls:%define nls 1}
%{!?pam:%define pam 1}

# Utility feature defines.
%{!?enable_mb:%define enable_mb 1}
%{!?pgaccess:%define pgaccess 1}

# Python major version.
%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{expand: %%define pynextver %(python -c 'import sys;print(float(sys.version[0:3])+0.1)')}


Summary: PostgreSQL client programs and libraries.
Name: postgresql
Version: 7.2.3

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

Release: 5.80
License: BSD
Group: Applications/Databases
Source0: ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.gz
Source2: redhat-style-files.lst
Source3: postgresql.init
Source4: suse-style-files.lst
Source5: ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.gz.md5
Source6: README.rpm-dist
Source7: migration-scripts.tar.gz
Source8: http://jdbc.postgresql.org/download/jdbc7.2dev-1.1.jar
Source9: http://jdbc.postgresql.org/download/jdbc7.2dev-1.2.jar
Source10: http://jdbc.postgresql.org/download/jdbc7.1-1.1.jar
Source11: http://jdbc.postgresql.org/download/jdbc7.1-1.2.jar
Source12: postgresql-dump.1.gz
Source14: rh-pgdump.sh
Source15: postgresql-bashprofile
Patch1: rpm-pgsql-%{version}.patch
Patch2: postgresql-%{version}-geo_ops.patch
Patch3: postgresql-%{version}-tighten.patch
Buildrequires: perl glibc-devel
Prereq: /sbin/ldconfig initscripts
%if %python
BuildPrereq: python-devel
%endif
%if %perl
BuildPrereq: perl
%endif
%if %tcl
BuildPrereq: tcl
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
Buildroot: %{_tmppath}/%{name}-%{version}-root
# Obsolete the packages we are not building...
%if ! %{plperl}
Obsoletes: postgresql-plperl
%endif
%if ! %{tcl}
Obsoletes: postgresql-tcl
%endif
%if ! %{tkpkg}
Obsoletes: postgresql-tk
%endif
%if ! %{odbc}
Obsoletes: postgresql-odbc
%endif
%if ! %{perl}
Obsoletes: postgresql-perl
%endif
%if ! %{python}
Obsoletes: postgresql-python
%endif
%if ! %{jdbc}
Obsoletes: postgresql-jdbc
%endif
%if ! %{test}
Obsoletes: postgresql-test
%endif



# This is the PostgreSQL Global Development Group Official RPMset spec file,
# or a derivative thereof.
# Copyright 2001 Lamar Owen <lamar@postgresql.org> <lamar.owen@wgcr.org>
# and others listed.

# Major Contributors:
# ---------------
# Lamar Owen
# Trond Eivind Glomsrød <teg@redhat.com>
# Thomas Lockhart
# Reinhard Max
# Karl DeBisschop
# Peter Eisentraut
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
Provides: libpq.so.2 libpq.so.2.0 libpq.so

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
Conflicts: postgresql-server <= 7.1.3

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
as well as the documentation in other formats, and some extra documentation.
Install this package if you want to help with the PostgreSQL documentation
project, or if you want to generate printed documentation.

%package contrib
Summary: Contributed source and binaries distributed with PostgreSQL
Group: Applications/Databases
Requires: postgresql = %{version} postgresql-perl postgresql-tcl tk
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
%if %plperl
%package plperl
Summary: The PL/Perl procedural language for PostgreSQL.
Group: Applications/Databases
Requires: perl, postgresql = %{version}

%description plperl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-plperl package contains the the PL/Perl
procedural language for the backend.
%endif

#------------
%if %tcl
%package tcl
Summary: A Tcl client library, and the PL/Tcl procedural language for PostgreSQL.
Group: Applications/Databases
Requires: tcl >= 8.0

%description tcl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-tcl package contains the libpgtcl client library,
the pg-enhanced pgtclsh, and the PL/Tcl procedural language for the backend.
%endif

#------------
%if %tkpkg
%package tk
Summary: Tk shell and tk-based GUI for PostgreSQL.
Group: Applications/Databases
Requires: tcl >= 8.0, tk >= 8.0

%description tk
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-tk package contains the pgaccess
program. Pgaccess is a graphical front end, written in Tcl/Tk, for the
psql and related PostgreSQL client programs.
%endif

#------------
%if %odbc
%package odbc
Summary: The ODBC driver needed for accessing a PostgreSQL DB using ODBC.
Group: Applications/Databases

%description odbc
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-odbc package includes the ODBC (Open DataBase
Connectivity) driver and sample configuration files needed for
applications to access a PostgreSQL database using ODBC.
%endif

#------------
%if %perl
%package perl
Summary: Development module needed for Perl code to access a PostgreSQL DB.
Group: Applications/Databases
Requires: perl >= 5.004-4

%description perl
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-perl package includes a module for developers
to use when writing Perl code for accessing a PostgreSQL database.
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

%description test
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-test package includes the sources and pre-built
binaries of various tests for the PostgreSQL database management
system, including regression tests and benchmarks.
%endif

%prep
%setup -q 

%patch1 -p1
%patch2 -p1
%patch3 -p1


%build

# Get file lists....
#tar xzf %{SOURCE4}
# Moved out of tarball.
cp %{SOURCE2} %{SOURCE4} .

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS

# Strip out -ffast-math from CFLAGS....

CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`

./configure --enable-locale  --with-CXX --prefix=/usr --disable-rpath\
%if %beta
	--enable-debug \
	--enable-cassert \
%endif
%if %perl
	--with-perl \
%endif
%if %enable_mb
	--enable-multibyte \
%endif
%if %tcl
	--with-tcl \
%endif
%if %tkpkg
%else
	--without-tk \
%endif
%if %odbc
	--with-odbc \
%endif
	--enable-syslog\
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
	--with-krb5=/usr/kerberos \
%endif
%if %nls
	--enable-nls \
%endif
	--sysconfdir=/etc/pgsql \
	--mandir=%{_mandir} \
	--docdir=%{_docdir} \
	--includedir=%{_includedir} \
	--datadir=/usr/share/pgsql

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

%if %perl
	make DESTDIR=$RPM_BUILD_ROOT -C src/interfaces/perl5 -f Makefile install

	# Get rid of the packing list generated by the perl Makefile, and build my own...
	find $RPM_BUILD_ROOT/usr/lib/perl5 -name .packlist -exec rm -f {} \;
	find $RPM_BUILD_ROOT/usr/lib/perl5 -type f -print | \
		sed -e "s|$RPM_BUILD_ROOT/|/|g"  | \
		sed -e "s|.*/man/.*|&\*|" > perlfiles.list
	find $RPM_BUILD_ROOT/usr/lib/perl5 -type d -name Pg -print | \
		sed -e "s|$RPM_BUILD_ROOT/|%dir /|g" >> perlfiles.list
	
	# check and fixup Pg manpage location....
	if [ ! -e $RPM_BUILD_ROOT%{_mandir}/man3/Pg.* ]
	then
		mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3
		cp src/interfaces/perl5/blib/man3/Pg.3pm $RPM_BUILD_ROOT%{_mandir}/man3
	fi
	
	pushd src/interfaces
	mkdir -p $RPM_BUILD_ROOT/usr/share/pgsql/perl5
	cp -a perl5/test.pl $RPM_BUILD_ROOT/usr/share/pgsql/perl5
	popd
	# remove perllocal.pod and Pg.bs from the file list - only occurs with 5.6

	perl -pi -e "s/^.*perllocal.pod$//" perlfiles.list
	perl -pi -e "s/^.*Pg.bs$//" perlfiles.list
	mkdir -p $RPM_BUILD_ROOT/usr/lib/perl5/site_perl/%{_arch}-linux/auto/Pg

%endif


# man pages....
# the postgresql-dump manpage.....
pushd $RPM_BUILD_ROOT%{_mandir}
cp %{SOURCE12} man1
popd

# install the dump script

install -m755 %SOURCE14 $RPM_BUILD_ROOT/usr/bin/

# install dev headers.

make DESTDIR=$RPM_BUILD_ROOT install-all-headers

# copy over Makefile.global to the include dir....
install -m755 src/Makefile.global $RPM_BUILD_ROOT/usr/include/pgsql

%if %pgaccess
	# pgaccess installation
	pushd src/bin
	install -m 755 pgaccess/pgaccess $RPM_BUILD_ROOT/usr/bin
	mkdir -p $RPM_BUILD_ROOT/usr/share/pgsql/pgaccess
	install -m 644 pgaccess/main.tcl $RPM_BUILD_ROOT/usr/share/pgsql/pgaccess
	tar cf - pgaccess/lib pgaccess/images | tar xf - -C $RPM_BUILD_ROOT/usr/share/pgsql
	cp -a pgaccess/doc/html   ../../doc/pgaccess
	cp    pgaccess/demo/*.sql ../../doc/pgaccess
	popd
%endif

%if %jdbc
	# Java/JDBC
	# The user will have to set a CLASSPATH to find it here, but not sure where else to put it...

	# JDBC jars 
	install -m 755 %{SOURCE8} $RPM_BUILD_ROOT/usr/share/pgsql
	install -m 755 %{SOURCE9} $RPM_BUILD_ROOT/usr/share/pgsql
	install -m 755 %{SOURCE10} $RPM_BUILD_ROOT/usr/share/pgsql
	install -m 755 %{SOURCE11} $RPM_BUILD_ROOT/usr/share/pgsql

%endif

# The initscripts....
# Redhat-style....
if [ -d /etc/rc.d/init.d ]
then
	install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
	install -m 755 %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/postgresql
	mv redhat-style-files.lst files.lst
fi

# SuSE-style....
# NOTE: SuSE stuff not yet fully implemented -- this is likely to not work yet.
# Putting SuSE-style stuff here
if [ -d /sbin/init.d ]
then
	# install the SuSE stuff...
	mv suse-style-files.lst files.lst
fi


# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 $RPM_BUILD_ROOT/var/lib/pgsql/data

# backups of data go here...
install -d -m 700 $RPM_BUILD_ROOT/var/lib/pgsql/backups

# postgres' .bash_profile
install -m 644 %{SOURCE15} $RPM_BUILD_ROOT/var/lib/pgsql/.bash_profile

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

# Upgrade scripts.
pushd $RPM_BUILD_ROOT
tar xzf %{SOURCE7}
popd

# logrotate script removed until future release
#logrotate script source (which needs WORK)
#mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
#cp %{SOURCE8} $RPM_BUILD_ROOT/etc/logrotate.d/postgres
#chmod 0644 $RPM_BUILD_ROOT/etc/logrotate.d/postgres

# Fix some more documentation
# gzip doc/internals.ps
cp %{SOURCE6} README.rpm-dist
mv $RPM_BUILD_ROOT%{_docdir}/postgresql/html doc

# Symlink libpq.so.2.0 to libpq.so.2 for backwards compatibility, until 
# -soname patches are the norm.
pushd $RPM_BUILD_ROOT/usr/lib
ln -s libpq.so.2 libpq.so.2.0
popd


%find_lang libpq
%find_lang pg_dump
%find_lang postgres
%find_lang psql

cat psql.lang pg_dump.lang > main.lst
cat postgres.lang files.lst > server.lst

%pre
# Need to make backups of some executables if an upgrade
# They will be needed to do a dump of the old version's database.
# All output redirected to /dev/null.

if [ $1 -gt 1 ]
then
   mkdir -p /usr/lib/pgsql/backup > /dev/null
   pushd /usr/bin > /dev/null
   cp -fp postmaster postgres pg_dump pg_dumpall psql /usr/share/pgsql/backup > /dev/null 2>&1  || :
   popd > /dev/null
   pushd /usr/lib > /dev/null
   cp -fp libpq.* /usr/share/pgsql/backup > /dev/null 2>&1 || :
   popd > /dev/null
fi

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

%if %odbc
%post -p /sbin/ldconfig  odbc
%postun -p /sbin/ldconfig  odbc
%endif

%if %tcl
%post -p /sbin/ldconfig   tcl
%postun -p /sbin/ldconfig   tcl
%endif

%if %plperl
%post -p /sbin/ldconfig   plperl
%postun -p /sbin/ldconfig   plperl
%endif

%if %test
%post test
chown -R postgres.postgres /usr/share/pgsql/test >/dev/null 2>&1 || :
%endif

%clean
rm -rf $RPM_BUILD_ROOT
rm -f perlfiles.list

# Ok, we are dynamically generating some filelists.  These are by default
# under the BUILD/postgresql-x.y.z tree.

# Note that macros such as config are available in those lists.
# The lists differentiate between RedHat, SuSE, and others.

%files -f main.lst
%defattr(-,root,root)
%doc doc/FAQ doc/KNOWN_BUGS doc/MISSING_FEATURES doc/README* 
%doc COPYRIGHT README HISTORY doc/bug.template
%doc README.rpm-dist
%doc doc/html
/usr/bin/createdb
/usr/bin/createlang
/usr/bin/createuser
/usr/bin/dropdb
/usr/bin/droplang
/usr/bin/dropuser
/usr/bin/pg_dump
/usr/bin/pg_dumpall
/usr/bin/pg_encoding
/usr/bin/pg_id
/usr/bin/pg_restore
/usr/bin/psql
/usr/bin/vacuumdb
%{_mandir}/man1/createdb.1*
%{_mandir}/man1/createlang.1*
%{_mandir}/man1/createuser.1*
%{_mandir}/man1/dropdb.1*
%{_mandir}/man1/droplang.1*
%{_mandir}/man1/dropuser.1*
%{_mandir}/man1/pg_dump.1*
%{_mandir}/man1/pg_dumpall.1*
%{_mandir}/man1/psql.1*
%{_mandir}/man1/vacuumdb.1*
%{_mandir}/man7/*

%files docs
%defattr(-,root,root)
%doc doc/src/*

%files contrib
%defattr(-,root,root)
/usr/lib/pgsql/_int.so
/usr/lib/pgsql/array_iterator.so
/usr/lib/pgsql/autoinc.so
/usr/lib/pgsql/btree_gist.so
/usr/lib/pgsql/chkpass.so
/usr/lib/pgsql/cube.so
/usr/lib/pgsql/dblink.so
/usr/lib/pgsql/earthdistance.so
/usr/lib/pgsql/fti.so
/usr/lib/pgsql/fuzzystrmatch.so
/usr/lib/pgsql/insert_username.so
/usr/lib/pgsql/isbn_issn.so
/usr/lib/pgsql/lo.so
/usr/lib/pgsql/misc_utils.so
/usr/lib/pgsql/moddatetime.so
/usr/lib/pgsql/noup.so
/usr/lib/pgsql/pgcrypto.so
/usr/lib/pgsql/refint.so
/usr/lib/pgsql/rserv.so
/usr/lib/pgsql/rtree_gist.so
/usr/lib/pgsql/seg.so
/usr/lib/pgsql/string_io.so
/usr/lib/pgsql/timetravel.so
/usr/lib/pgsql/user_locks.so
/usr/share/pgsql/contrib/
/usr/bin/dbf2pg
/usr/bin/findoidjoins
/usr/bin/make_oidjoins_check
/usr/bin/fti.pl
/usr/bin/oid2name
/usr/bin/pg_controldata
/usr/bin/pg_dumplo
/usr/bin/pg_logger
/usr/bin/pg_resetxlog
/usr/bin/pgbench
/usr/bin/RservTest
/usr/bin/MasterInit
/usr/bin/MasterAddTable
/usr/bin/Replicate
/usr/bin/MasterSync
/usr/bin/CleanLog
/usr/bin/SlaveInit
/usr/bin/SlaveAddTable
/usr/bin/GetSyncID
/usr/bin/PrepareSnapshot
/usr/bin/ApplySnapshot
/usr/bin/InitRservTest
/usr/bin/vacuumlo
%doc contrib/*/README.* contrib/spi/*.example

%files libs -f libpq.lang
%defattr(-,root,root)
/usr/lib/libpq.so.*
/usr/lib/libecpg.so.*
/usr/lib/libpq++.so.*
/usr/lib/libpgeasy.so.*

%files server -f server.lst
%defattr(-,root,root)
/usr/bin/initdb
/usr/bin/initlocation
/usr/bin/ipcclean
/usr/bin/pg_ctl
/usr/bin/pg_passwd
/usr/bin/postgres
/usr/bin/postgresql-dump
/usr/bin/postmaster
/usr/bin/rh-pgdump.sh
%{_mandir}/man1/initdb.1*
%{_mandir}/man1/initlocation.1*
%{_mandir}/man1/ipcclean.1*
%{_mandir}/man1/pg_ctl.1*
%{_mandir}/man1/pg_passwd.1*
%{_mandir}/man1/postgres.1*
%{_mandir}/man1/postmaster.1*
%{_mandir}/man1/postgresql-dump.1*
/usr/share/pgsql/postgres.bki
/usr/share/pgsql/postgres.description
/usr/share/pgsql/*.sample
/usr/lib/pgsql/plpgsql.so
%dir /usr/lib/pgsql
%dir /usr/share/pgsql
%attr(700,postgres,postgres) %dir /usr/share/pgsql/backup
/usr/share/pgsql/backup/pg_dumpall_new
%attr(700,postgres,postgres) %dir /var/lib/pgsql
%attr(700,postgres,postgres) %dir /var/lib/pgsql/data
%attr(700,postgres,postgres) %dir /var/lib/pgsql/backups
%attr(644,postgres,postgres) %config(noreplace) /var/lib/pgsql/.bash_profile

%files devel
%defattr(-,root,root)
/usr/include/*
/usr/bin/ecpg
/usr/bin/pg_config
/usr/lib/libpq.so
/usr/lib/libecpg.so
/usr/lib/libpq++.so
/usr/lib/libpgeasy.so
/usr/lib/libpq.a
/usr/lib/libecpg.a
/usr/lib/libpq++.a
/usr/lib/libpgeasy.a
%if %tcl
/usr/lib/libpgtcl.a
%endif
%{_mandir}/man1/ecpg.1*
%{_mandir}/man1/pg_config.1*

%if %tcl
%files tcl
%defattr(-,root,root)
%attr(755,root,root) /usr/lib/libpgtcl.so.*
# libpgtcl.so is not in devel because Tcl scripts may load it by that name.
/usr/lib/libpgtcl.so
/usr/bin/pgtclsh
%{_mandir}/man1/pgtclsh.1*
/usr/lib/pgsql/pltcl.so
%endif

%if %tkpkg
%files tk
%defattr(-,root,root)
/usr/bin/pgtksh
%{_mandir}/man1/pgtksh.1*
%endif

%if %pgaccess
%doc doc/pgaccess/*
/usr/share/pgsql/pgaccess
/usr/bin/pgaccess
%{_mandir}/man1/pgaccess.1*
%endif

%if %odbc
%files odbc
%defattr(-,root,root)
%attr(755,root,root) /usr/lib/libpsqlodbc.so*
/usr/share/pgsql/odbc.sql
%endif

%if %perl
%files -f perlfiles.list perl
%defattr (-,root,root)
%dir /usr/lib/perl5/site_perl/%{_arch}-linux/auto
/usr/share/pgsql/perl5
%{_mandir}/man3/Pg.*
%endif

%if %plperl
%files plperl
%defattr(-,root,root)
/usr/lib/pgsql/plperl.so
%endif

%if %python
%files python
%defattr(-,root,root)
%doc src/interfaces/python/README src/interfaces/python/tutorial
/usr/lib/python%{pyver}/site-packages/_pgmodule.so
/usr/lib/python%{pyver}/site-packages/*.py
%endif

%if %jdbc
%files jdbc
%defattr(-,root,root)
/usr/share/pgsql/jdbc7.1-1.1.jar
/usr/share/pgsql/jdbc7.1-1.2.jar
/usr/share/pgsql/jdbc7.2dev-1.1.jar
/usr/share/pgsql/jdbc7.2dev-1.2.jar
%endif

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) /usr/lib/pgsql/test/*
%attr(-,postgres,postgres) %dir /usr/lib/pgsql/test
%endif

%changelog
* Wed Dec 20 2002 Andrew Overholt <overholt@redhat.com>
- 7.2.3-4.(73,80) - add buffer overrun patch for geo_ops
- 7.2.3-5.(73,80) - add pg_hba.conf tightening patch

* Thu Dec 19 2002 Andrew Overholt <overholt@redhat.com>
- 7.2.3-3.(73,80) - correct init script success/failure messages.

* Tue Dec 17 2002 Andrew Overholt <overholt@redhat.com>
- 7.2.3-1 - initial Red Hat build.
- 7.2.3-2.(73,80) - distribution-specific release tags to avoid upgrading
  issues.

* Wed Oct 02 2002 Lamar Owen <lamar.owen@ramifordistat.net>
- 7.2.3-1PGDG

* Mon Aug 26 2002 Lamar Owen <lamar.owen@ramifordistat.net>
- 7.2.2-1PGDG
- Applied PeterE's contrib patch -- contrib is now completely restructured.
- server conflicts with less than 7.2, as a warning to the upcoming
-- yank of the broken partial upgrade.

* Thu Aug 22 2002 Lamar Owen <lamar.owen@ramifordistat.net>
- 7.2.2 security fix.
- deprecate postgresql-dump system.
- 7.2.2-0.1PGDG PRERELEASE!

* Fri Apr 12 2002 Lamar Owen <lamar.owen@ramifordistat.net>
- Correct tcl conditionals -- especially for the devel package.
- Corrected BuildPrereq conditionals.
- Added a build6x conditional -- define it to build for RHL 6.x
- Integrate a few of Trond's fixes from RawHide.
- Pulled file-lists out of tarball for better maintainability.
- Updated README.rpm-dist.
- 6.x build can't buildprereq pam-devel, as 6.x has no pam-devel.

* Tue Apr 09 2002 Lamar Owen <lamar.owen@ramifordistat.net>
- Integrate DP's patch and stuff.

* Fri Apr 05 2002 David B. Peterson <dave@toppledwagon.com>
- hacked for 7.2.1 (made rpm-pgsql-7.2.1.patch from rpm-pgsql-7.2.patch)
- changed gettext version to 0.10.35 (from 0.10.36, for RH62)
- added BuildPrereq for tk

* Wed Apr  3 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.2.1-3
- make postgresql-server and postgresql depend on postgresql-libs
- store backups of old binaries in /usr/lib/pgsql/backup instead of /usr/share

* Thu Mar 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.2-6
- Move the libpgtcl.so symlink into the tcl subpackage from -devel
- Enable pam support
- Include the odbc plugin, not just the symlink to it

* Tue Feb 04 2002 Lamar Owen <lamar.owen@wgcr.org>
- 7.2 final.
- 7.2-1PGDG RPM release.
- Integrate NLS build per Peter E.
- Clean up a few things; undef beta for final build.
- Newer JDBC -- point to correct website and 7.2 dev.
- postgresql.init changes.
- NLS build does funky %defattr things; redhat-style-files.lst changed
-- for execute permission on /etc/rc.d/init.d/postgresql

* Sun Jan 27 2002 Lamar Owen <lamar.owen@wgcr.org>
- 7.2rc2-0.1PGDG

* Thu Nov 29 2001 Lamar Owen <lamar.owen@wgcr.org>
- 7.2b3-0.3PGDG
- beta conditionals for debugging, assertion checking, and no strip.

* Tue Nov 27 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Improve python version handling

* Fri Nov 23 2001 Lamar Owen <lamar.owen@wgcr.org>
- 7.2b3-0.2PGDG
- second beta3 tarball.

* Thu Nov 22 2001 Lamar Owen <lamar.owen@wgcr.org>
- 7.2b3-0.1PGDG
- Beta3
- Docs changes --man pages back, internals.ps gone.
- manl (letter 'ell') is now 'man7'.

* Mon Nov 19 2001 Lamar Owen <lamar.owen@wgcr.org>
- 7.2b2-0.1PGDG
- --disable-rpath configure option.

* Fri Oct 26 2001 Lamar Owen <lamar.owen@wgcr.org>
- Actual PGDG 7.2b1.

* Mon Oct 01 2001 Lamar Owen <lamar.owen@wgcr.org>
- 7.2alpha-0.1PGDG
- Merged some changes from Peter Eisentraut for7.2.
- Cleaned up some legacy junk.
- Prepare for 7.2 beta cycle.















