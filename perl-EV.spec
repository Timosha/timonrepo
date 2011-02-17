Name:           perl-EV
Version:        4.03
Release:        1%{?dist}
Summary:        Wrapper for the libev high-performance event loop library

Group:          Development/Libraries
License:        (GPL+ or Artistic) and (BSD or GPLv2+)
URL:            http://search.cpan.org/dist/EV/
Source0:        http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/EV-%{version}.tar.gz
Patch0:         perl-EV-4.03-Don-t-ask-questions-at-build-time.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(common::sense)
BuildRequires:  gdbm-devel
BuildRequires:  libev-source == %{version}
BuildRequires:  perl(AnyEvent) => 2.6
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
This module provides an interface to libev
(<http://software.schmorp.de/pkg/libev.html>). While the included documentation
is comprehensive, one might also consult the documentation of libev itself
(<http://cvs.schmorp.de/libev/ev.html>) for more subtle details on watcher
semantics or some discussion on the available backends, or how to force a
specific backend with "LIBEV_FLAGS", or just about in any case because it has
much more detailed information.


%prep
%setup -q -n EV-%{version}

# no questins during build
%patch0 -p1

# remove all traces of the bundled libev
rm -fr libev/*

# use the sources from the system libev
mkdir -p ./libev
cp -r /usr/share/libev-source/* ./libev/


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes COPYING README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/EV.pm
%{perl_vendorarch}/EV/
%{_mandir}/man3/*.3*


%changelog
* Mon Jan 24 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 4.03-1
- Update to 4.03.
- Use the system libev instead of the bundled one.

* Sun Nov  8 2009 kwizart < kwizart at gmail.com > - 3.8-1
- Update to 3.8

* Tue Apr 28 2009 kwizart < kwizart at gmail.com > - 3.6-1
- Update to 3.6

* Mon Mar  2 2009 kwizart < kwizart at gmail.com > - 3.53-1
- Update to 3.53

* Tue Feb  3 2009 kwizart < kwizart at gmail.com > - 3.52-1
- Update to 3.52

* Tue Oct 14 2008 kwizart < kwizart at gmail.com > - 3.44-1
- Update to 3.44
- WIP conditional --with systemlibev

* Wed Jul 15 2008 kwizart < kwizart at gmail.com > - 3.431-1
- Update to 3.431
- Update License to (GPL+ or Artistic) and (BSD or GPLv2+)
- Add libev README and LICENSE

* Wed Jul  8 2008 kwizart < kwizart at gmail.com > - 3.43-1
- Update to 3.43

* Mon Jun  9 2008 kwizart < kwizart at gmail.com > - 3.42-2
- Disable filter AnyEvent

* Tue May 27 2008 kwizart < kwizart at gmail.com > - 3.42-1
- Update to 3.42

* Wed Apr 30 2008 kwizart < kwizart at gmail.com > - 3.31-1
- Initial package for Fedora

