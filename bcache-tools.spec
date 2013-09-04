%global gitdate 20130827

Summary: Tools for Linux kernel block layer cache
Name: bcache-tools
Version: 0
Release: 0.9.%{gitdate}git%{?dist}
License: GPLv2
Group: System Environment/Base
URL: http://bcache.evilpiepirate.org/
VCS: http://evilpiepirate.org/git/bcache-tools.git
# For now I am using a prerelease version obtained by:
# git clone http://evilpiepirate.org/git/bcache-tools.git
# cd bcache-tools/
# git archive --format=tar --prefix=bcache-tools-20130827/ 8327108eeaf3e0491b17d803da164c0827aae622 | gzip > ../bcache-tools-20130827.tar.bz
Source0: %{name}-%{gitdate}.tar.bz
# This part is also a prerelease version obtained by https://gist.github.com/djwong/6343451:
# git clone https://gist.github.com/6343451.git
# cd 6343451/
# git archive --format=tar --prefix=bcache-status-20130826/ 95fe51dd30e579d5786a8cbf54ee47df0b347250 | gzip > ../bcache-status-20130826.tar.gz
# see also http://article.gmane.org/gmane.linux.kernel.bcache.devel/1951
Source1: bcache-status-20130826.tar.gz
# bcache status not provided as a true package, so this is a self maintained man page for it
# http://article.gmane.org/gmane.linux.kernel.bcache.devel/1946
Patch0: %{name}-status-20130826-man.patch
# Sent upstream: http://article.gmane.org/gmane.linux.kernel.bcache.devel/1946
Patch1: bcache-status-20130826-python.patch
# Sent upstream: http://article.gmane.org/gmane.linux.kernel.bcache.devel/1947
# This one can be left out when this is processed:
# http://article.gmane.org/gmane.linux.kernel.bcache.devel/1953
Patch2: %{name}-20130827-register.patch
# configure and make install are not "Fedora compliant", do a small step in the
# right direction
Patch3: %{name}-20130827-fedconfmake.patch

Requires: python
BuildRequires: libuuid-devel systemd

%description
Bcache is a Linux kernel block layer cache. It allows one or more fast disk
drives such as flash-based solid state drives (SSDs) to act as a cache for
one or more slower hard disk drives.
This package contains the utilities for manipulating bcache.

%global _udevlibdir %{_prefix}/lib/udev

%prep
%setup -q -n bcache-tools-%{gitdate}
tar xzf %{SOURCE1} --strip-components=1
%patch0 -p1 -b .man
%patch1 -p1 -b .python
%patch2 -p1 -b .register
%patch3 -p1 -b .fedconfmake
chmod +x configure

%build
%configure
make %{?_smp_mflags}

%install
mkdir -p \
    %{buildroot}%{_sbindir} \
    %{buildroot}%{_mandir}/man8 \
    %{buildroot}%{_udevlibdir} \
    %{buildroot}%{_udevrulesdir}

%make_install \
    SBINDIR=%{_sbindir} \
    UDEVRULESDIR=%{_udevrulesdir} \
    UDEVLIBDIR=%{_udevlibdir} \
    MANDIR=%{_mandir}

install -p  -m 755 bcache-status %{buildroot}%{_sbindir}/bcache-status

%files
%doc README COPYING
%{_udevrulesdir}/*
%{_mandir}/man8/*
%{_udevlibdir}/bcache-register
%{_sbindir}/bcache-super-show
%{_sbindir}/bcache-status
%{_sbindir}/make-bcache
%{_sbindir}/probe-bcache

%changelog
* Mon Sep 02 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.9.20130827git
- fedconfmake.spec file renamed to fedconfmake.patch
- removed libuuid as dependency
- removed trailing white-spaces in patch lines
- removed CFLAGS= from configure section
- removed (empty) check section
- replaced "make install" with make_install macro
- updated summary

* Sat Aug 31 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.8.20130827git
- updated bcache-tools to commit 8327108eeaf3e0491b17d803da164c0827aae622
- corrected URL/VCS tag
- moved towards more RPM compliancy by using configure macro
- used "make install" to do most of the work
- added (empty) check section

* Mon Aug 26 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.7.20130820git
- updated bcache-status to latest upstream gist
- removed the -rules patch

* Mon Aug 26 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.6.20130820git
- removed tar and gcc from BuildRequires
- removed defattr from files section
- added upstream references to patches in comments 

* Sun Aug 25 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.5.20130820git
- moved bcache-register to /usr/lib/udev
- suppress bcache-register error output (caused by registering device twice)
- removed man page for bcache-register
- added bcache-status
- added tar and gcc to BuildRequires
- added python to Requires

* Sat Aug 24 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.4.20130820git
- Fixed the udev rules for Fedora

* Thu Aug 22 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.3.20130820git
- Added systemd to BuildRequires

* Thu Aug 22 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.2.20130820git
- Fixed initial review feedback

* Tue Aug 20 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.1.20130820git
- Initial build
