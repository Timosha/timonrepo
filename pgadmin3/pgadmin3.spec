Summary:	Graphical client for PostgreSQL
Name:		pgadmin3
Version:	1.12.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
#Source:	ftp://ftp.postgresql.org/pub/pgadmin3/release/v%{version}/src/%{name}-%{version}.tar.gz
#git clone git://git.postgresql.org/git/pgadmin3.git pgadmin3
#GIT_DIR=pgadmin3/.git git archive --format=tar --prefix=pgadmin3-1.12.1/ REL-1_12_1 | bzip2 > pgadmin3-1.12.1.tar.bz2
Source0:	%{name}-%{version}.tar.bz2
URL:		http://www.pgadmin.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	wxGTK-devel postgresql-devel desktop-file-utils openssl-devel libxml2-devel libxslt-devel
BuildRequires:  autoconf automake
Requires:	wxGTK

%description
pgAdmin III is a powerful administration and development
platform for the PostgreSQL database, free for any use.
It is designed to answer the needs of all users,
from writing simple SQL queries to developing complex
databases. The graphical interface supports all PostgreSQL
features and makes administration easy.

pgAdmin III is designed to answer the needs of all users, 
from writing simple SQL queries to developing complex databases. 
The graphical interface supports all PostgreSQL features and 
makes administration easy. The application also includes a syntax 
highlighting SQL editor, a server-side code editor, an 
SQL/batch/shell job scheduling agent, support for the Slony-I 
replication engine and much more. No additional drivers are 
required to communicate with the database server.

%prep
%setup -q
bash bootstrap

%build
export LIBS="-lwx_gtk2u_core-2.8"
%configure --disable-debug --disable-dependency-tracking --with-wx-version=2.8 --with-wx=%{_prefix}
%{__make} %{?_smp_mflags} all

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

%{__cp} -f ./pkg/debian/pgadmin3.xpm %{buildroot}/%{_datadir}/%{name}/%{name}.xpm

%{__mkdir} -p %{buildroot}/%{_datadir}/applications

desktop-file-install --dir %{buildroot}%{_datadir}/applications \
%if 0%{?rhel}
	--vendor="" \
%endif
	--add-category Development pkg/%{name}.desktop

# Convert changelog, fix incorrect end-of-line encoding
#iconv -f iso-8859-1 -t utf-8 -o CHANGELOG.utf8 CHANGELOG
#sed -i 's/\r$//' CHANGELOG.utf8
#touch -c -r CHANGELOG CHANGELOG.utf8
#mv -f CHANGELOG.utf8 CHANGELOG

# Remove unwanted and double files
%{__rm} -f docs/{Docs.vcproj,builddocs.bat}
%{__rm} -f %{buildroot}%{_datadir}/%{name}/i18n/{*,.}/wxstd.mo

# Correct permissions to solve rpmlint debuginfo noise
chmod 644 pgadmin/include/images/{package,synonym}{,s}.xpm

# Move locales to their correct place
%{__mkdir} -p %{buildroot}%{_datadir}/locale
%{__mv} -f %{buildroot}%{_datadir}/%{name}/i18n/??_?? %{buildroot}%{_datadir}/locale

%find_lang %{name}

%clean
%{__rm} -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc BUGS CHANGELOG LICENSE README docs/*
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/applications/*

%changelog
* Tue Oct 5 2010 Timon <timosha@gmail.com> - 1.12.1-1
- 1.12.1 release

* Wed Sep 29 2010 Timon <timosha@gmail.com> - 1.12.1-0.3.git290910
- Some fixes

* Thu Sep 28 2010 Timon <timosha@gmail.com> - 1.12.1-0.2.git280910
- Pre 1.12.1 development version

* Wed Sep 22 2010 Timon <timosha@gmail.com> - 1.12.1-0.1
- 1.12 development version with fixed Russian translation

* Fri Sep 17 2010 Timon <timosha@gmail.com> - 1.12-1
- 1.12 release

* Wed Sep 15 2010 Timon <timosha@gmail.com> - 1.12-0.rc1
- Update to 1.12rc1

* Tue Aug 3 2010 2010 Devrim GUNDUZ <devrim@gunduz.org> 1.10.5-1
- Update to 1.10.5

* Tue Jun 15 2010 Michel Salim <salimma@fedoraproject.org> - 1.10.3-2
- Ship the hints files (bz #513039)

* Thu May 13 2010 Devrim GUNDUZ <devrim@gunduz.org> 1.10.3-1
- Update to 1.10.3

* Mon Mar 15 2010 Devrim GUNDUZ <devrim@gunduz.org> 1.10.2-1
- Update to 1.10.2

* Thu Dec 3 2009 Devrim GUNDUZ <devrim@gunduz.org> 1.10.1-1
- Update to 1.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Devrim GUNDUZ <devrim@gunduz.org> 1.10.0-1
- Update to 1.10.0
- Update licence
- Incorporate some changes from rpmfusion:
  Corrected pgadmin3 documentation path to avoid errors (#448)
  Re-added the branding directory for some users (RHBZ #473748)
  Removed useless -docs package, main package shipped it anyway
  Many spec file and package cleanups to get rpmlint very silent

* Mon Jul 14 2008 Ville Skyttä <ville.skytta at iki.fi> - 1.8.4-2
- Use $RPM_OPT_FLAGS, build with dependency tracking disabled (#229054).

* Wed Jun 4 2008 Devrim GUNDUZ <devrim@commandprompt.com> 1.8.4-1
- Update to 1.8.4

* Tue Jun 3 2008 Devrim GUNDUZ <devrim@commandprompt.com> 1.8.3-1
- Update to 1.8.3

* Fri Feb 1 2008 Devrim GUNDUZ <devrim@commandprompt.com> 1.8.2-1
- Update to 1.8.2

* Fri Jan 4 2008 Devrim GUNDUZ <devrim@commandprompt.com> 1.8.1-1
- Update to 1.8.1

* Wed Dec 05 2007 Devrim GUNDUZ <devrim@commandprompt.com> 1.8.0-2
- Rebuild for openssl bump

* Wed Nov 14 2007 Devrim GUNDUZ <devrim@commandprompt.com> 1.8.0-1
- Update to 1.8.0
- Fix requires and buildrequires
- Improve description
- Added -docs subpackage
- add 2 new configure options, per upstream
- Fix path for xpm file

* Wed Apr 04 2007 Warren Togami <wtogami@redhat.com> - 1.6.3-1
- 1.6.3

* Thu Dec 28 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.6.1-2
- A couple of minor fixes to get things building in rawhide.

* Tue Dec 05 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.6.1-1
- Update for 1.6.1. Now needs wxGTK 2.7+

* Mon Oct 09 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.3-6
- Rebuild for FC6

* Tue Aug 29 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.3-5
- Should have Developement and keeping this version one ahead for
  upgrading in FC-6

* Mon Aug 28 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.3-3
- Moved icon to Devel and updated for FC-6

* Sat Jul 30 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.3-2
- Removed gcc41 patch

* Sat Jul 29 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.3-1
- Updated to latest 
- Sorry for delay

* Wed Feb 16 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.1-2
- Applied Dennis' fixes according to Bug #181632

* Wed Feb 15 2006 Dennis Gilmore <dennis@ausil.us> - 1.4.1-1
- update to 1.4.1

* Thu Dec 8 2005 Gavin Henry <ghenry@suretecsystems.com> - 1.4.0-2
- Removed specific lib includes, not needed anymore 

* Wed Dec 7 2005 Gavin Henry <ghenry@suretecsystems.com> - 1.4.0-1
- Updated to latest release

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.0.2-5
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Oct 07 2004 Nils O. Selåsdal <NOS|at|Utel.no> - 0:1.0.2-0.fdr.3
- include LICENCE.txt BUGS.txt README.txt
- Use master location in Source
- Don't --delete-original .desktop file.
* Thu Oct 07 2004 Nils O. Selåsdal <NOS|at|Utel.no> - 0:1.0.2-0.fdr.2
- Don't own _datadir/applications/
- Fedora -> fedora for .desktop file
- Use _smp_mflags for make
* Wed Oct 06 2004 Nils O. Selåsdal <NOS|at|Utel.no> - 0:1.0.2-0.fdr.1
- Initial RPM

