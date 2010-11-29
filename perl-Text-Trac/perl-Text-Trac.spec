Name:           perl-Text-Trac
Version:        0.15
Release:        1%{?dist}
Summary:        Perl extension for formatting text with Trac Wiki Style
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Text-Trac/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MI/MIZZY/Text-Trac-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl-Module-Build
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl-Test-Base
BuildRequires:  perl-UNIVERSAL-require
BuildRequires:  perl-Class-Accessor
BuildRequires:  perl-Class-Data-Inheritable
BuildRequires:  perl-Tie-IxHash
BuildRequires:  perl-List-MoreUtils
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Test::Pod)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl-Class-Accessor
Requires:       perl-Class-Data-Inheritable

%description
Text::Trac parses text with Trac WikiFormatting and convert it to html format.

%prep
%setup -q -n Text-Trac-%{version}
find -type f -name *.pm -exec chmod -x {} \;

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT

%{__make} pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null \;

chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 03 2009 Timon <timosha@gmail.com> - 0.15-1
- bump new version
- review notes

* Fri Sep 26 2008 Timon <timosha@gmail.com> - 0.13-2
- broken deps

* Fri Sep 26 2008 Timon <timosha@gmail.com> - 0.13-1
- import Alt Linux spec http://www.sisyphus.ru/srpm/perl-Text-Trac
- version 0.13


