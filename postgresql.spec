Summary: PostgreSQL client programs and libraries.
Name: postgresql
Version: 7.0.2
Release: 18.2
License: BSD
Group: Applications/Databases
Source0: ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.gz
Source1: http://jdbc.postgresql.org/download/jdbc6.5-1.1.jar
Source2: http://jdbc.postgresql.org/download/jdbc6.5-1.2.jar
Source3: postgresql.init-%{version}
Source6: README.rpm.postgresql-%{version}
Source5: ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.gz.md5
Source7: pg-migration-scripts-%{version}.tar.gz
Source8: logrotate.postgresql-%{version}
Source9: pg_options-%{version}
Source10: http://www.retep.org.uk/postgres/jdbc7.0-1.1.jar
Source11: http://www.retep.org.uk/postgres/jdbc7.0-1.2.jar
Source12: postgresql-dump.1.gz
Source14: rh-pgdump.sh
Patch0: postgresql-%{version}-alpha.patch.gz
Patch1: rpm-pgsql-%{version}.patch
Patch2: postgresql-%{version}-security.patch
Requires: perl
Prereq: /sbin/chkconfig /sbin/ldconfig /usr/sbin/useradd /lib/cpp initscripts
BuildPrereq: python-devel perl tcl
Url: http://www.postgresql.org/ 
Obsoletes: postgresql-clients postgresql-test
Buildroot: %{_tmppath}/%{name}-%{version}-root
ExcludeArch: ia64

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
server over a network connection. This package contains the client
libraries for C and C++, as well as command-line utilities for
managing PostgreSQL databases on a PostgreSQL server. 

If you want to manipulate a PostgreSQL database on a remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql-server package.

%package server
Summary: The programs needed to create and run a PostgreSQL server.
Group: Applications/Databases
Prereq: /usr/sbin/useradd
Requires: postgresql = %{version}

%description server
The postgresql-server package includes the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.  PostgreSQL is an advanced
Object-Relational database management system (DBMS) that supports
almost all SQL constructs (including transactions, subselects and
user-defined types and functions). You should install
postgresql-server if you want to create and maintain your own
PostgreSQL databases and/or your own PostgreSQL server. You also need
to install the postgresql and postgresql-devel packages.

%package devel
Summary: PostgreSQL development header files and libraries.
Group: Development/Libraries
Requires: postgresql = %{version}

%description devel
The postgresql-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server and the ecpg Embedded C
Postgres preprocessor. You need to install this package if you want to
develop applications which will interact with a PostgreSQL server. If
you're installing postgresql-server, you need to install this
package.

%package tcl
Summary: A Tcl client library, and the PL/Tcl procedural language for PostgreSQL.
Group: Applications/Databases
Requires: tcl >= 8.0, postgresql = %{version}

%description tcl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-tcl package contains the libpgtcl client library,
the pg-enchanced pgtclsh, and the PL/Tcl procedural language for the backend.

%package tk
Summary: Tk shell and tk-based GUI for PostgreSQL.
Group: Applications/Databases
Requires: tcl >= 8.0, tk >= 8.0, postgresql = %{version}

%description tk
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-tk package contains the pgaccess
program. Pgaccess is a graphical front end, written in Tcl/Tk, for the
psql and related PostgreSQL client programs.


%package odbc
Summary: The ODBC driver needed for accessing a PostgreSQL DB using ODBC.
Group: Applications/Databases
Requires: postgresql = %{version}

%description odbc
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-odbc package includes the ODBC (Open DataBase
Connectivity) driver and sample configuration files needed for
applications to access a PostgreSQL database using ODBC.

%package perl
Summary: Development module needed for Perl code to access a PostgreSQL DB.
Group: Applications/Databases
Requires: perl >= 5.004-4, postgresql = %{version}

%description perl
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-perl package includes a module for developers
to use when writing Perl code for accessing a PostgreSQL database.

%package python
Summary: Development module for Python code to access a PostgreSQL DB.
Group: Applications/Databases
Requires: python >= 1.5, postgresql = %{version}

%description python
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-python package includes a module for
developers to use when writing Python code for accessing a PostgreSQL
database.

%package jdbc
Summary: Files needed for Java programs to access a PostgreSQL database.
Group: Applications/Databases
Requires: postgresql = %{version}

%description jdbc
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-jdbc package includes the .jar file needed for
Java programs to access a PostgreSQL database.

#package test
#Summary: The test suite distributed with PostgreSQL.
#Group: Applications/Databases
#Requires: postgresql = %{version}

#description test
#PostgreSQL is an advanced Object-Relational database management
#system. The postgresql-test package includes the sources and pre-built
#binaries of various tests for the PostgreSQL database management
#system, including regression tests and benchmarks.

%prep
%setup -q 

# The alpha patches are not trivial, so wrap in ifarch-endif block
#
%ifarch alpha
%patch0 -p1
%endif

%patch1 -p1
%patch2 -p1

%build
pushd src
# XXX libtoolize dinna work
# WHAT is 'libtoolize???' LRO
# a program distributed with the libtool package

#cp /usr/share/libtool/config.* .
CFLAGS="$RPM_OPT_FLAGS"
%ifarch alpha
	./configure --enable-hba --enable-locale --prefix=/usr\
	--with-perl --enable-multibyte\
	--with-tcl --with-tk --with-x \
	--with-odbc --with-java \
	--with-python --with-template=linux_alpha
%else

./configure --enable-hba --enable-locale  --prefix=/usr\
	--with-perl --enable-multibyte \
	--with-tcl --with-tk --with-x \
	--with-odbc --with-java \
	--with-python
%endif

make COPT="$RPM_OPT_FLAGS" all

pushd interfaces/python
cp /usr/lib/python1.5/config/Makefile.pre.in .
echo *shared* > Setup
echo _pg pgmodule.c -I../../include -I../libpq -L../libpq -lpq -lcrypt >> Setup
make -f Makefile.pre.in boot
make
popd
popd

make all PGDOCS=unpacked -C doc

pushd src/test
make all
popd

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{include/pgsql,lib,bin}
mkdir -p $RPM_BUILD_ROOT%{_mandir}
mkdir -p $RPM_BUILD_ROOT/usr/lib/perl5/site_perl/%{_arch}-linux/auto/Pg
make POSTGRESDIR=$RPM_BUILD_ROOT/usr PREFIX=$RPM_BUILD_ROOT/usr -C src install
#make POSTGRESDIR=$RPM_BUILD_ROOT/usr PREFIX=$RPM_BUILD_ROOT/usr -C src/man install
make POSTGRESDIR=$RPM_BUILD_ROOT/usr PREFIX=$RPM_BUILD_ROOT/usr -C src/interfaces/perl5 install

# Get rid of the packing list generated by the perl Makefile, and build my own...
find $RPM_BUILD_ROOT/usr/lib/perl5 -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT/usr/lib/perl5 -type f -print | \
	sed -e "s|$RPM_BUILD_ROOT/|/|g"  | \
	sed -e "s|.*/man/.*|&\*|" > perlfiles.list
find $RPM_BUILD_ROOT/usr/lib/perl5 -type d -name Pg -print | \
	sed -e "s|$RPM_BUILD_ROOT/|%dir /|g" >> perlfiles.list
make -C doc
#make -C doc man
# Newer man pages from Thomas Lockhart
pushd $RPM_BUILD_ROOT%{_mandir}
tar xzf $RPM_BUILD_DIR/postgresql-%{version}/doc/man.tar.gz

# the postgresql-dump manpage.....
cp %{SOURCE12} man1
popd

# install the dump script

install -m755 %SOURCE14 $RPM_BUILD_ROOT/usr/bin/

# Move all includes beneath /usr/include/pgsql.
pushd $RPM_BUILD_ROOT/usr/include
rm -rf pgsql/*
for f in *.h access commands executor iodbc lib libpq libpq++ port utils ; do
     mv $f pgsql
done
popd

# copy over the includes needed for SPI development.
pushd src/include
/lib/cpp -M -I. -I../backend executor/spi.h |xargs -n 1|grep \\W|grep -v ^/|grep -v spi.o |grep -v spi.h | sort |cpio -pdu $RPM_BUILD_ROOT/usr/include/pgsql
# thank you, cpio....

#fixup directory permissions for SPI stuff...
pushd $RPM_BUILD_ROOT/usr/include/pgsql
chmod 755 access catalog executor lib nodes parser rewrite storage tcop utils
popd

popd

# Move all templates/examples beneath /usr/lib/pgsql
pushd $RPM_BUILD_ROOT/usr/lib
  mkdir -p pgsql
  mv *.source *.sample *.description pgsql
popd

# Get interface-specific tests and examples, and stuff under /usr/lib/pgsql
pushd src/interfaces
mkdir -p $RPM_BUILD_ROOT/usr/lib/pgsql/perl5
cp -a perl5/test.pl perl5/eg $RPM_BUILD_ROOT/usr/lib/pgsql/perl5
mkdir -p $RPM_BUILD_ROOT/usr/lib/pgsql/python
cp -a python/tutorial $RPM_BUILD_ROOT/usr/lib/pgsql/python
popd

# Get example odbcinst.ini and put in /usr/lib/pgsql
mv $RPM_BUILD_ROOT/usr/odbcinst.ini $RPM_BUILD_ROOT/usr/lib/pgsql

# pgaccess installation
pushd src/bin
install -m 755 pgaccess/pgaccess $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/lib/pgsql/pgaccess
install -m 644 pgaccess/main.tcl $RPM_BUILD_ROOT/usr/lib/pgsql/pgaccess
tar cf - pgaccess/lib pgaccess/images | tar xf - -C $RPM_BUILD_ROOT/usr/lib/pgsql
cp -a pgaccess/doc/html   ../../doc/pgaccess
cp    pgaccess/demo/*.sql ../../doc/pgaccess
popd

# Python
pushd src/interfaces/python
# Makefile.pre.in doesn't yet support .py files anyway, so we stick to a manual installation
  mkdir -p $RPM_BUILD_ROOT/usr/lib/python1.5/site-packages
  install -m 755 _pgmodule.so *.py $RPM_BUILD_ROOT/usr/lib/python1.5/site-packages/
popd

# Java/JDBC
# We know that JDK1.2 is pre-beta at this time, so install the JDK1.1-compatible driver
# as well as the JDK1.2 compatible driver.
# The user will have to set a CLASSPATH to find it here, but not sure where else to put it...
# Install 6.5 JDBC jars for now.
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/usr/lib/pgsql
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/usr/lib/pgsql
# Install 7.0 JDBC jars -- in addition to, not replacing 6.5 stuff yet.
install -m 755 %{SOURCE10} $RPM_BUILD_ROOT/usr/lib/pgsql
install -m 755 %{SOURCE11} $RPM_BUILD_ROOT/usr/lib/pgsql

chmod 644 $RPM_BUILD_ROOT%{_mandir}/*/*
chmod +x $RPM_BUILD_ROOT/usr/lib/lib*.so.*
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 755 %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/postgresql

# Move the PL's to the right place
mv $RPM_BUILD_ROOT/usr/lib/pl*.so $RPM_BUILD_ROOT/usr/lib/pgsql

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 $RPM_BUILD_ROOT/var/lib/pgsql/data

# Initial pg_options
install -m 700 %{SOURCE9} $RPM_BUILD_ROOT/var/lib/pgsql/data/pg_options

# backups of data go here...
install -d -m 700 $RPM_BUILD_ROOT/var/lib/pgsql/backups


# tests. There are many files included here that are unnecessary, but include
# them anyway for completeness.

#cp -a src/test $RPM_BUILD_ROOT/usr/lib/pgsql
#install -m 0755 src/config.guess $RPM_BUILD_ROOT/usr/lib/pgsql
#install -m 0755 contrib/spi/refint.so $RPM_BUILD_ROOT/usr/lib/pgsql/test/regress
#install -m 0755 contrib/spi/autoinc.so $RPM_BUILD_ROOT/usr/lib/pgsql/test/regress

# Upgrade scripts.
pushd $RPM_BUILD_ROOT
tar xzf %{SOURCE7}
popd

#logrotate script source (which needs WORK)
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
cp %{SOURCE8} $RPM_BUILD_ROOT/etc/logrotate.d/postgres
chmod 0700 $RPM_BUILD_ROOT/etc/logrotate.d/postgres


# Fix some more documentation
# no need for the OS2 client
rm -rf contrib/os2client
gzip doc/internals.ps
cp %{SOURCE6} README.rpm

# remove the binaries from contrib

rm -f `find contrib -name "*.so"`
rm -f contrib/spi/preprocessor/step1.e

# Fix a dangling symlink
mkdir -p $RPM_BUILD_ROOT/usr/include/pgsql/port
cp src/include/port/linux.h $RPM_BUILD_ROOT/usr/include/pgsql/port/
ln -sf port/linux.h $RPM_BUILD_ROOT/usr/include/pgsql/os.h

# remove perllocal.pod from the file list - only occurs with 5.6

perl -pi -e "s/^.*perllocal.pod$//" perlfiles.list

%pre
# Need to make backups of some executables if an upgrade
# They will be needed to do a dump of the old version's database.
# All output redirected to /dev/null.

if [ $1 -gt 1 ]
then
   mkdir -p /usr/lib/pgsql/backup > /dev/null
   pushd /usr/bin > /dev/null
   cp -fp postmaster postgres pg_dump pg_dumpall psql /usr/lib/pgsql/backup > /dev/null 2>&1  || :
   popd > /dev/null
   pushd /usr/lib > /dev/null
   cp -fp libpq.* /usr/lib/pgsql/backup > /dev/null 2>&1 || :
   popd > /dev/null
fi

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%pre server
useradd -M -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :
touch /var/log/postgresql
chown postgres.postgres /var/log/postgresql
chmod 0700 /var/log/postgresql

%post -p /sbin/ldconfig  server

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
fi

%post -p /sbin/ldconfig  odbc
%postun -p /sbin/ldconfig  odbc

%post -p /sbin/ldconfig   tcl
%postun -p /sbin/ldconfig   tcl

%clean
rm -rf $RPM_BUILD_ROOT
rm -f perlfiles.list

%files
%defattr(-,root,root)
%doc doc/FAQ doc/FAQ_Linux doc/README* 
%doc COPYRIGHT README HISTORY doc/bug.template doc/FAQ_Linux
%doc contrib doc/unpacked/* 
%doc README.rpm
/usr/lib/libpq.so.*
/usr/lib/libecpg.so.*
/usr/lib/libpq++.so.*
/usr/lib/libpgeasy.so.*
/usr/bin/createdb
/usr/bin/createlang
/usr/bin/createuser
/usr/bin/dropdb
/usr/bin/droplang
/usr/bin/dropuser
/usr/bin/pg_dump
/usr/bin/pg_dumpall
/usr/bin/pg_id
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
%{_mandir}/manl/*

%files server
%defattr(-,root,root)
%config /etc/rc.d/init.d/postgresql
/etc/logrotate.d/postgres
/usr/bin/initdb
/usr/bin/initlocation
/usr/bin/ipcclean
/usr/bin/pg_ctl
/usr/bin/pg_encoding
/usr/bin/pg_passwd
/usr/bin/pg_upgrade
/usr/bin/pg_version
/usr/bin/postgres
/usr/bin/postgresql-dump
/usr/bin/postmaster
/usr/bin/rh-pgdump.sh

%{_mandir}/man1/initdb.1*
%{_mandir}/man1/initlocation.1*
%{_mandir}/man1/ipcclean.1*
%{_mandir}/man1/pg_ctl.1*
%{_mandir}/man1/pgadmin.1*
%{_mandir}/man1/pg_passwd.1*
%{_mandir}/man1/postgres.1*
%{_mandir}/man1/postmaster.1*
%{_mandir}/man1/pg_upgrade.1*
%{_mandir}/man1/vacuumdb.1*
%{_mandir}/man1/postgresql-dump.1*
/usr/lib/pgsql/global1.bki.source
/usr/lib/pgsql/global1.description
/usr/lib/pgsql/local1_template1.bki.source
/usr/lib/pgsql/local1_template1.description
/usr/lib/pgsql/*.sample
/usr/lib/pgsql/plpgsql.so
%attr(700,postgres,postgres) %dir /usr/lib/pgsql/backup
/usr/lib/pgsql/backup/pg_dumpall_new
%attr(700,postgres,postgres) %dir /var/lib/pgsql/data
%attr(700,postgres,postgres) /var/lib/pgsql/data/pg_options
%attr(700,postgres,postgres) %dir /var/lib/pgsql/backups

%files devel
%defattr(-,root,root)
/usr/include/pgsql
/usr/bin/ecpg
/usr/lib/lib*.a
/usr/lib/libpq.so
/usr/lib/libecpg.so
/usr/lib/libpq++.so
/usr/lib/libpgeasy.so
%{_mandir}/man1/ecpg.1*

%files tcl
%defattr(-,root,root)
%attr(755,root,root) /usr/lib/libpgtcl.so*
/usr/bin/pgtclsh
%{_mandir}/man1/pgtclsh.1*
/usr/lib/pgsql/pltcl.so

%files tk
%defattr(-,root,root)
%doc doc/pgaccess/*
/usr/lib/pgsql/pgaccess
/usr/bin/pgaccess
/usr/bin/pgtksh
%{_mandir}/man1/pgaccess.1*
%{_mandir}/man1/pgtksh.1*

%files odbc
%defattr(-,root,root)
%attr(755,root,root) /usr/lib/libpsqlodbc.so*
/usr/lib/pgsql/odbcinst.ini

%files -f perlfiles.list perl
%defattr (-,root,root)
%dir /usr/lib/perl5/site_perl/%{_arch}-linux/auto
/usr/lib/pgsql/perl5
%{_mandir}/man3/Pg.*

%files python
%defattr(-,root,root)
/usr/lib/python1.5/site-packages/_pgmodule.so
/usr/lib/python1.5/site-packages/*.py
/usr/lib/pgsql/python

%files jdbc
%defattr(-,root,root)
/usr/lib/pgsql/jdbc6.5-1.1.jar
/usr/lib/pgsql/jdbc6.5-1.2.jar
/usr/lib/pgsql/jdbc7.0-1.1.jar
/usr/lib/pgsql/jdbc7.0-1.2.jar

#files test
#defattr(-,postgres,postgres)
#attr(755,postgres,postgres)/usr/lib/pgsql/config.guess
#/usr/lib/pgsql/test/*

%changelog
* Tue Jan 7 2003 Andrew Overholt <overholt@redhat.com> [7.0.2-18.2]
- addition to security backpatch

* Tue Jan 7 2003 Andrew Overholt <overholt@redhat.com> [7.0.2-18]
- add security backpatch from more recent versions (~#74505)

* Thu Aug 24 2000 Trond Eivind Glomsrød <teg@redhat.com>
- the old dump script didn't work - added rh-pgdump.sh
  to handle this. Point docs at it, and tell how it is to be used. 

* Mon Aug 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix the initscript so it points you at the 7.0.2 directory
  in /usr/share/doc, not 7.0  (#16163). Also, remove statement
  it was built on a 6.2 system.
- prereq /lib/cpp and initscripts
- fix backups of existing files (#16706)
- fix conditional restart

* Sat Aug 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix README.rpm to it points at /usr/share/doc, not /usr/doc 
  (part of #16416)

* Wed Aug 16 2000 Trond Eivind Glomsrød <teg@redhat.com>
- don't build test package anymore, it's broken. These
  tests should be run by pgsql developers and not
  by db-developers, so it's not a big loss (#16165).
  Obsolete it in the main package, so it doesn't get left over

* Mon Aug 14 2000 Trond Eivind Glomsrød <teg@redhat.com>
- reference docs in /usr/share/doc, not /usr/doc (#16163)
- add python-devel, perl and tcl as build prereqs
- use /dev/null as STDIN for su commands in initscripts,
  to avoid error messages from not being able to read from 
  tty

* Sat Aug 05 2000 Bill Nottingham <notting@redhat.com>
- condrestart fixes

* Mon Jul 31 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove all plperl references, to avoid confusing post install scripts
- cleanups

* Mon Jul 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove the symlink from libpq.so.2.0 to libpq.so.2.1
- remove some binaries from docs
- fix dangling symlink os.h
- use /sbin/service

* Thu Jul 13 2000 Trond Eivind Glomsrød <teg@redhat.com>
- don't strip manually
- fixes to init script so they look more like the rest 
  (#13749, from giulioo@pobox.com)
- use /etc/rc.d/init.d again (sigh)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jul 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- "Prereq:", not "Requires:" for /etc/init.d

* Thu Jul 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- require /etc/init.d

* Wed Jun 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove perl kludge as perl 5.6 is now fixed
- include the man page for the perl module
- fix the init script and spec file to handle conditional
  restart
- move the init file to /etc/init.d
- use License instead of Copyright

* Mon Jun 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Tue Jun 13 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%defattr on postgresql-perl
- use %%{_tmppath}
- Don't use release number in patch 
- Don't build on ia64 yet

* Mon Jun 12 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0.2-2
- Corrected misreporting of version.
- Corrected for non-root build clean script.

* Mon Jun 05 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0.2 
- Postgresql-dump manpage to man1, and to separate source file to facilitate
-- _mandir macro expansion correctness.
- NOTE: The PostScript documentation is no longer being included in the
-- PostgreSQL tarball.  If demand is such, I will pull together a
-- postgresql-ps-docs subpackage or pull in the PostScript docs into the
-- main package.
- RPM patchset has release number, now, to prevent patchfile confusion :-(.


* Sat Jun 03 2000 Lamar Owen <lamar.owen@wgcr.org>
- Incorporate most of Trond's changes (reenabled the alpha
-- patches, as it was a packaging error on my part).
- Trimmed changelog history to Version 7.0beta1 on. To see the
-- previous changelog, grab the 6.5.3 RPM from RedHat 6.2 and pull the spec.
- Rev to 7.0.1 (which incorporates the syslog patch, which has
-- been removed from rpm-pgsql-7.0.1-1.patch)

* Fri May 26 2000 Trond Eivind Glomsrød <teg@redhat.com>
- disable the alpha patch, as it doesn't apply cleanly
- removed distribution, packager, vendor
- renamed spec file
- don't build pl-perl
- use %%{_mandir}
- now includes vacuumdb.1*

* Thu May 25 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0-3
- Incorporated Tatsuo's syslog segmentation patches
- Incorporated some of Trond's changes (see below)
-- Fixed some Perl 5.6 oddness in Rawhide
- Incorporated some of Karl's changes (see below)
-- PL/Perl should now work.
- Fixed missing /usr/bin/pg_passwd.

* Mon May 22 2000 Karl DeBisschop <kdebisschop@infoplease.com>
- 7.0-2.1
- make plperl module (works for linux i386, your guess for other platforms)
- use "make COPT=" because postgreSQL configusre script ignores CFLAGS

* Sat May 20 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0-2
- pg_options default values changed.
- SPI headers (again!) fixed in a permanent manner  -- hopefully!
- Alpha patches!

* Wed May 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- changed bug in including man pages

* Tue May 16 2000 Trond Eivind Glomsrød <teg@redhat.com>
- changed buildroot, removed packager, vendor, distribution
-- [Left all but buildroot as-is for PostgreSQL.org RPMS. LRO]
- don't strip in package [strip in PostgreSQL.org RPMS]
- fix perl weirdnesses (man page in bad location, remove 
  perllocal.pod from file list)

* Mon May 15 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0 final -1
- Man pages restructured
- Changed README.rpm notices about BETA
- incorporated minor changes from testing
- still no 7.0 final alpha patches -- for -2 or -3, I guess.
- 7.0 JDBC jars!

* Sat May 06 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0RC5-0.5
- UserID of 26 to conform to RedHat Standard, instead of 40.  This only
-- is for new installs -- upgrades will use what was already there.
- Waiting on built jar's of JDBC.  If none are forthcoming by release,
-- I'm going to have to bite the bullet and install the jdk....

* Mon May 01 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0RC2-0.5
- Fixed /usr/src/redhat/BUILD path to $RPM_BUILD_DIR for portability
-- and so that RPM's can be built by non-root.
- Minor update to README.rpm

* Tue Apr 18 2000 Lamar Owen <lamar.owen@wgcr.org>
- 0.6
- Fixed patchset: wasn't patching pgaccess or -i in postmaster.opts.default
- minor update to README.rpm

* Mon Apr 17 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0RC1-0.5 (release candidate 1.)
- Fixed SPI header directories' permisssions.
- Removed packaging of Alpha patches until Ryan releases RC1-tested set.

* Mon Apr 10 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0beta5-0.1 (released instead of the release candidate)

* Sat Apr 08 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0beta4-0.2 (pre-release-candidate CVS checkout)
- Alpha patches!
- pg_options.sample

* Fri Mar 24 2000 Lamar Owen <lamar.owen@wgcr.org>
- 7.0beta3-0.1

* Mon Feb 28 2000 Lamar Owen <lamar.owen@wgcr.org>
- Release 0.3
- Fixed stderr redir problem in init script
- Init script now uses pg_ctl to start postmaster
- Packaged inital pg_options for good logging
- built with timestamped logging.

* Tue Feb 22 2000 Lamar Owen <lamar.owen@wgcr.org>
- Initial 7.0beta1 build
- Moved PGDATA to /var/lib/pgsql/data
- First stab at logging and logrotate functionality -- test carefully!
- -tcl subpackage split -- tcl client and pltcl lang separated from
-- the Tk stuff.  PgAccess and the tk client are now in the -tk subpackage.
- No patches for Alpha as yet.

