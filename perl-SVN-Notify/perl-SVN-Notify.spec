Name:           perl-SVN-Notify
Version:        2.80
Release:        1%{?dist}
Summary:        Perl module for Subversion activity notification
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/SVN-Notify/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DW/DWHEELER/SVN-Notify-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl-Module-Build
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
#BuildRequires:  perl(Net::SMTP)
#BuildRequires:  perl(Net::SMTP_auth)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
#Requires:       perl(Text::Trac)

%description 
SVN::Notify Perl module may be used for sending email messages for Subversion 
repository activity. There are a number of different modes supported, 
and SVN::Notify is fully subclassable, to easily add new functionality. 
By default, a list of all the files affected by the commit will be assembled 
and listed in a single message. An additional option allows diffs 
to be calculated for the changes and either appended to the message 
or added as an attachment. The included subclass, SVN::Notify::HTML, allows 
the messages to be sent in HTML format.

%package -n svnnotify
Summary:        Subversion activity notification using SVN::Notify
Group:          Development/Tools
Requires:       perl-SVN-Notify = %{version}-%{release}

%description -n svnnotify
Little perl script which uses SVN::Notify. It can be used for sending email
messages for Subversion repositority activity.

%prep
%setup -q -n SVN-Notify-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT

%{__make} pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;

%check
%{__make} test

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files -n svnnotify
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/svnnotify
%{_mandir}/man1/svnnotify.*

%changelog
* Mon Jul 12 2010 Timon <timosha@gmail.com> - 2.80-1
- new version

* Fri Jun 19 2009 Timon <timosha@gmail.com> - 2.79-1
- new version
- spec fixes

* Thu Oct 16 2008 Timon <timosha@gmail.com> - 2.78-2
- fix dep list
- descriptions changed
- fix rpmlint errors

* Fri Sep 26 2008 Timon <timosha@gmail.com> - 2.78-1
- import Alt Linux spec http://www.sisyphus.ru/srpm/perl-SVN-Notify
- version 2.78

