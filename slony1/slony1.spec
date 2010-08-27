%{!?docs:%define docs 0}

Summary:	A "master to multiple slaves" replication system with cascading and failover
Name:		slony1
Version:	2.0.4
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://slony.info/
# git clone http://git.postgresql.org/git/slony1-engine.git
# GIT_DIR=slony1/.git git archive --format=tar --prefix=slony1-2.0.4/ REL_2_0_4 | bzip2 > slony1-2.0.4.tar.bz2
Source0:	http://slony.info/downloads/2.0/source/%{name}-%{version}.tar.bz2
Patch1:		slony1-pgport-build-fix.patch
#Source2:	filter-requires-perl-Pg.sh
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql-devel 
BuildRequires:	postgresql-server
BuildRequires:	byacc
BuildRequires:	flex
Requires:	postgresql perl-DBD-Pg

%description
Slony-I is a "master to multiple slaves" replication 
system for PostgreSQL with cascading and failover.

The big picture for the development of Slony-I is to build
a master-slave system that includes all features and
capabilities needed to replicate large databases to a
reasonably limited number of slave systems.

Slony-I is a system for data centers and backup
sites, where the normal mode of operation is that all nodes
are available

%if %docs
%package docs
Summary:	Documentation for Slony-I
Group:		Applications/Databases
Requires:	%{name}
BuildRequires:	libjpeg, netpbm-progs, groff, docbook-style-dsssl, ghostscript
BuildRequires:	docbook-style-dsssl postgresql_autodoc docbook-utils
%description docs
The postgresql-slony1-docs package includes some 
documentation for Slony-I.
%endif

#define __perl_requires %{SOURCE2}

%prep
%setup -q -n %{name}-%{version}
# fix lpgport
%patch1 -p0

%build

## Temporary measure for 1.2.10
#%if %docs
#find doc/ -type f -exec chmod 600 {} \;
#%endif

#CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
#CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
#CPPFLAGS="${CPPFLAGS} -I%{_includedir}/et -I%{kerbdir}/include" ; export CPPFLAGS
#CFLAGS="${CFLAGS} -I%{_includedir}/et -I%{kerbdir}/include" ; export CFLAGS

#export LIBNAME=%{_lib}
#%configure --includedir %{_includedir}/pgsql --with-pgconfigdir=%{_bindir} --libdir=%{_libdir} \
#	--with-perltools=%{_bindir} --with-toolsbin=%{_bindir} \
%configure \
%if %docs
	--with-docs --with-docdir=%{_docdir}/%{name}-%{version} \
%endif
	--datadir %{_datadir}/pgsql \
	--includedir %{_includedir}/pgsql --with-pgconfigdir=%{_bindir} --libdir=%{_libdir} \
	--with-perltools=%{_bindir} --with-perlsharedir=%{_datadir}/perl5

autoconf

%{__make} %{?_smp_mflags}
%{__make} %{?_smp_mflags} -C tools

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_sysconfdir}
%{__install} -d %{buildroot}%{_datadir}/%{name}/
%{__install} -d %{buildroot}%{_libdir}/pgsql/

%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%{__install} -m 0755 src/backend/slony1_funcs.so %{buildroot}%{_libdir}/pgsql/slony1_funcs.so
%{__install} -m 0644 src/backend/*.sql %{buildroot}%{_datadir}/%{name}/
%{__install} -m 0755 tools/*.sh  %{buildroot}%{_bindir}/
%{__install} -m 0755 tools/*.pl  %{buildroot}%{_bindir}/
%{__install} -m 0644 share/slon.conf-sample %{buildroot}%{_sysconfdir}/slon.conf
#chmod 644 COPYRIGHT UPGRADING SAMPLE HISTORY-1.1 RELEASE

%{__install} -d %{buildroot}%{_initrddir}
%{__install} -m 755 redhat/slon.init %{buildroot}%{_initrddir}/slony1

%if %docs
# Temporary measure for 1.2.X
%{__rm} -f doc/implementation/.cvsignore
%{__rm} -f doc/concept/.cvsignore
%endif

pushd tools
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__rm} -rf altperl/*.pl altperl/ToDo altperl/README altperl/Makefile altperl/CVS
%{__install} -m 0644 altperl/slon_tools.conf-sample  %{buildroot}%{_sysconfdir}/slon_tools.conf
%{__install} -m 0755 altperl/* %{buildroot}%{_bindir}/
%{__install} -D -m 0644 altperl/slon-tools  %{buildroot}%{_datadir}/perl5/slon-tools.pm

%{__mkdir} -p %{buildroot}%{_datadir}/%{name}
%{__mv} %{buildroot}%{_datadir}/pgsql/*.sql %{buildroot}%{_datadir}/%{name}

%{__rm} -f %{buildroot}%{_sysconfdir}/slon_tools.conf-sample
%{__rm} -f %{buildroot}%{_bindir}/slon_tools.conf-sample
%{__rm} -f %{buildroot}%{_libdir}/slon-tools.pm
%{__rm} -f %{buildroot}%{_bindir}/slon-tools
%{__rm} -f %{buildroot}%{_bindir}/pgsql/slon-tools
%{__rm} -f %{buildroot}%{_bindir}/old-apache-rotatelogs.patch

# requires perl(log) and old perl(Pg)
%{__rm} -f %{buildroot}%{_bindir}/test_slony_replication.pl
%{__rm} -f %{buildroot}%{_bindir}/test_slony_state.pl


%clean
%{__rm} -rf %{buildroot}

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
        /sbin/service %{name} stop >/dev/null 2>&1
        /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" -ge "1" ]; then
        /sbin/service %{name} condrestart >/dev/null 2>&1
fi

%files
%defattr(-,root,root,-)
%attr(644,root,root) %doc COPYRIGHT UPGRADING HISTORY-1.1 INSTALL SAMPLE RELEASE
%{_bindir}/*
%{_libdir}/pgsql/slony1_funcs.so
%{_datadir}/%{name}/*.sql
%config(noreplace) %{_sysconfdir}/slon.conf
%{_datadir}/perl5/slon-tools.pm
%config(noreplace) %{_sysconfdir}/slon_tools.conf
%attr(755,root,root) %{_initrddir}/slony1

%if %docs
%{_mandir}/man1/*
%{_mandir}/man7/*
%endif

%if %docs
%files docs
%attr(644,root,root) %doc doc/adminguide  doc/concept  doc/howto  doc/implementation  doc/support
%endif

%changelog
* Mon Jul 12 2010 Timon <timosha@gmail.com> - 2.0.4-1
- new version
- disable doc builds

* Sat May 9 2009 Devrim Gunduz <devrim@CommandPrompt.com> 2.0.2-1
- Update to 2.0.2
- Removed patch0 -- it is no longer needed.
- Added a temp patch to get rid of sgml error.
- Re-enable doc builds

* Sat Mar 14 2009 Devrim Gunduz <devrim@CommandPrompt.com> 2.0.1-1
- Update to 2.0.1
- Create log directory,	per pgcore #77.

* Thu Jan 29 2009 Devrim Gunduz <devrim@CommandPrompt.com> 2.0.0-3
- Add docbook-utils to BR.

* Sat Dec 13 2008 Devrim Gunduz <devrim@CommandPrompt.com> 2.0.0-2
- Add a patch to fix build errors
- Temporarily update Source2, so that it will silence a dependency error.

* Tue Dec 2 2008 Devrim Gunduz <devrim@CommandPrompt.com> 2.0.0-1
- Update to 2.0.0

* Mon Sep 22 2008 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.15-3
- Add dependency for perl-DBD-Pg, paer Xavier Bergade.

* Sun Sep 21 2008 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.15-2
- Fix dependency issues caused by latest commit.

* Fri Sep 12 2008 Devrim Gunduz <devtrim@CommandPrompt.com> 1.2.15-1
- Update to 1.2.15
- Install tools written in perl, too.

* Fri May 16 2008 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.14-1
- Update to 1.2.14

* Wed Apr 2 2008 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.13-2
- Fix init script name.

* Sun Feb 10 2008 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.13-1
- Update to 1.2.13

* Mon Dec 17 2007 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.12-2
- Add flex and byacc to buildrequires, per Michael Best

* Tue Nov 13 2007 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.12-1
- Update to 1.2.12

* Wed Aug 29 2007 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.11-1
- Update to 1.2.11
- Remove the word "engine" from init script name.

* Mon Aug 6 2007 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.10-2
- Fix Source0
- Spec file cleanup (removed macro for perltools)
- Added initscripts as BR.
- Fix doc package installation path (and ownership issue)

* Wed Jun 13 2007 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.10-1
- Update to 1.2.10

* Mon Jun 11 2007 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.9-3
- Add BuildRequires for docs subpackage, per #199154 (Thanks Ruben).

* Sun Jun 3 2007 Devrim Gunduz <devrim@CommandPrompt.com> 1.2.9-2
- Some more fixes for Fedora review.
- Remove executable bits from docs.

* Thu May 17 2007 Devrim Gunduz <devrim@CommandPrompt.com>
- Install init script with rpm.
- Fix --with-pgconfigdir parameter.
- Fix rpm build problem when the system has pg_config in both under
  /usr/local/pgsql/bin and /usr/bin

* Wed Mar 22 2007 Christopher Browne <cbbrowne@ca.afilias.info>
- Added more recent release notes

* Wed Mar 7 2007 Christopher Browne <cbbrowne@ca.afilias.info>
- Added more recent release notes

* Thu Jan 4 2007 Devrim Gunduz <devrim@CommandPrompt.com>
- Add docs package (It should be added before but...)

* Wed Nov 8 2006 Devrim Gunduz <devrim@CommandPrompt.com>
- On 64-bit boxes, both 32 and 64 bit -devel packages may be installed. 
  Fix version check script
- Revert tar name patch
- Macros cannot be used in various parts of the spec file. Revert that commit
- Spec file cleanup

* Tue Oct 31 2006 Trevor Astrope <astrope@sitesell.com>
- Fixup tar name and install slon-tools as slon-tools.pm

* Mon Jul 17 2006 Devrim Gunduz <devrim@CommandPrompt.com> postgresql-slony1-engine
- Updated spec and cleaned up rpmlint errors and warnings

* Wed Dec 21 2005 Devrim Gunduz <devrim@commandprompt.com> postgresql-slony1-engine
- Added a buildrhel3 macro to fix RHEL 3 RPM builds
- Added a kerbdir macro

* Wed Dec 14 2005 Devrim Gunduz <devrim@commandprompt.com> postgresql-slony1-engine
- Fixed the spec file so that during upgrade, conf files will not be replaced, and a .rpmnew will be created.

* Thu Nov 24 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Created bindir

* Wed Oct 26 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Modify CPPFLAGS and CFLAGS to fix builds on RHEL -- Per Philip Yarra

* Tue Oct 18 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Created a new package : -docs and moved all the docs there.

* Tue Oct 18 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Fixed the problem in http://gborg.postgresql.org/pipermail/slony1-general/2005-October/003105.html

* Sat Oct 01 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Upgrade to 1.1.1

* Tue Jul 12 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Added a line to check postgresql RPM version and tag SlonyI RPM with it.
- Updated Requires files so that it checks correct PostgreSQL version
- Moved autoconf line into correct place.

* Thu Jun 08 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Added UPGRADING, HISTORY-1.1, INSTALL, SAMPLE among installed files, reflecting the change in GNUMakefile.in

* Thu Jun 02 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Apply a new %docs macro and disable building of docs by default.
- Remove slon-tools.conf-sample from bindir.
- Removed --bindir and --libdir, since they are not needed.

* Mon Apr 10 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- More fixes on RPM builds

* Thu Apr 07 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- More fixes on RPM builds

* Tue Apr 04 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Fix RPM build errors, regarding to tools/ .

* Thu Apr 02 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Added docs to installed files list.
- Added perltools, so that tools/altperl may be compiled.
- Updated the spec file

* Thu Mar 17 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Update to 1.1.0beta1
- Remove PostgreSQL source dependency

* Thu Mar 17 2005 Devrim Gunduz <devrim@PostgreSQL.org> postgresql-slony1-engine
- Fix RPM builds

* Thu Mar 18 2004 Daniel Berrange <berrange@redhat.com> postgresql-slony1-engine
- Initial RPM packaging

