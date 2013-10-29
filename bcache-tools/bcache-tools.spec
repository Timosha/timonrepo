%global gitdate 20131018

# blkid in util-linux v2.24 will be able to identify bcache superblocks which
# obsoletes probe-bcache. v2.24 rc is planned for F20:
# https://bugzilla.redhat.com/show_bug.cgi?id=1001120#c13
# so for F20 blkid will be used, but not for older Fedora in case someone
# builds it
#
%if 0%{?fedora} > 19
%global use_blkid 1
%else
%global use_blkid 0
%endif

Summary: Tools for Linux kernel block layer cache
Name: bcache-tools
Version: 0
Release: 0.15.%{gitdate}git%{?dist}
License: GPLv2
Group: System Environment/Base
URL: http://bcache.evilpiepirate.org/
VCS: http://evilpiepirate.org/git/bcache-tools.git
# For now I am using a prerelease version obtained by:
# git clone http://evilpiepirate.org/git/bcache-tools.git
# cd bcache-tools/
# git archive --format=tar --prefix=bcache-tools-20131018/ 89f11b135d1d57a5dbdc3548bfb9bfa0113075c4 | gzip > ../bcache-tools-20131018.tar.gz
Source0: %{name}-%{gitdate}.tar.gz
# This part is also a prerelease version obtained by https://gist.github.com/djwong/6343451:
# git clone https://gist.github.com/6343451.git
# cd 6343451/
# git archive --format=tar --prefix=bcache-status-20130909/ 10282160ab880eab0d9b8d1e1590e477f1e76da2 | gzip > ../bcache-status-20130909.tar.gz
# see also http://article.gmane.org/gmane.linux.kernel.bcache.devel/1951
Source1: bcache-status-20130909.tar.gz
# bcache status not provided as a true package, so this is a self maintained man page for it
# http://article.gmane.org/gmane.linux.kernel.bcache.devel/1946
Patch0: %{name}-status-20130826-man.patch
# Skip DM devices marked private - will be in git repo later
# https://github.com/g2p/bcache-tools/commit/15f17ed3e9a8dbe44a0e60cd981f70b7a61d6f7a
Patch1: %{name}-20131018-udev-dmfix.patch
# configure is not "Fedora compliant", do a small step in the
# right direction
Patch2: %{name}-20131018-fedconf.patch

Requires: python
%if %{use_blkid}
# This is a kind of soft dependency: because we don't include probe-bcache
# we have to make sure that libblkid is able to identify bcache. So this
# is why it requires recent libblkid.
Requires: libblkid >= 2.24
%endif
BuildRequires: libuuid-devel libblkid-devel systemd

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
%patch1 -p1 -b .dmfix
%patch2 -p1 -b .fedconfmake
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
    INSTALL="install -p" \
    UDEVLIBDIR=%{_udevlibdir} \
    MANDIR=%{_mandir}

# prevent complaints when checking for unpackaged files
%if %{use_blkid}
rm %{buildroot}%{_sbindir}/probe-bcache
rm %{buildroot}%{_mandir}/man8/probe-bcache.8
%endif
install -p  -m 755 bcache-status %{buildroot}%{_sbindir}/bcache-status

%files
%doc README COPYING
%{_udevrulesdir}/*
%{_mandir}/man8/*
%{_udevlibdir}/bcache-register
%{_sbindir}/bcache-super-show
%{_sbindir}/bcache-status
%{_sbindir}/make-bcache
%if !%{use_blkid}
%{_udevlibdir}/probe-bcache
%endif

%changelog
* Mon Oct 28 2013 Timon <timosha@gmail.com> - - 0-0.16.20131018git
- remove dracut support
- back F19 support

* Fri Oct 18 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.15.20131018git
- updated bcache-tools to latest upstream git
- bcache-register no longer needs patching
- Makefile no longer needs patching

* Wed Oct 02 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.14.20130909git
- dropped pre F20 support; no use since deps on util-linux and dracut
- (#1004693) removed execute blkid in 61-bcache.rules
- (#1004693) moved 61-bcache.rules to 69-bcache.rules
- (#1004693) now inluding /usr/lib/dracut/modules.d/90bcache/...

* Mon Sep 30 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.13.20130909git
- (#1004693) add execute blkid in 61-bcache.rules

* Fri Sep 27 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.12.20130909git
- remove obsoleted probe-bcache in F20 using use_blkid macro

* Mon Sep 09 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.11.20130909git
- updated to new bcache-status
- updated to new bcache-tools
- added libblkid-devel to BuildRequires

* Fri Sep 06 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.10.20130827git
- fixed some udev related issues (#1004693)

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
