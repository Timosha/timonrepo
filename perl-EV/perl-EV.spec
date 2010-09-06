
Name:           perl-EV
Version:        3.9
Release:        1%{?dist}
Summary:        Perl interface to libev
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/EV/
Source0:        http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/EV-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl-Module-Build
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(common::sense)
#BuildRequires:  libev-devel=%{version}

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
#Requires:       libev=%{version}

%description 
EV - perl interface to libev, a high performance full-featured event loop

%prep
%setup -q -n EV-%{version}

%build
PERL_MM_USE_DEFAULT=1 %{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT

%{__make} pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;

%check
%{__make} test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README COPYING
%{perl_vendorarch}/*
%{_mandir}/man3/*

%changelog
* Thu Aug 5 2010 Timon <timosha@gmail.com> - 3.9-1
- first build for Fedora

