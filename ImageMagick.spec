Summary: An X application for displaying and manipulating images.
Name: ImageMagick
Version: 5.2.7
Release: 4
Copyright: freeware
Group: Applications/Multimedia
Source: ftp://ftp.cdrom.com/pub/ImageMagick/ImageMagick-%{version}.tar.bz2
Patch0: ImageMagick-5.2.6-libpath.patch
Patch1: ImageMagick-5.2.4-lprhack.patch
Url: http://www.imagemagick.org/
Buildroot: %{_tmppath}/%{name}-%{version}-root
BuildPrereq: bzip2-devel, freetype-devel, libjpeg-devel, libpng-devel
BuildPrereq: libtiff-devel, libungif-devel, zlib-devel
Requires: bzip2, freetype, libjpeg, libpng, libtiff, libungif, zlib
BuildRequires: freetype-devel >= 2.0.1
Prefix: /usr/X11R6
%define _prefix /usr/X11R6
%define _mandir %{_prefix}/man
%define _includedir %{_prefix}/include/X11/magick

%description
ImageMagick(TM) is an image display and manipulation tool for the X 
Window System.  ImageMagick can read and write JPEG, TIFF, PNM, GIF
and Photo CD image formats.  It can resize, rotate, sharpen, color 
reduce or add special effects to an image, and when finished you can 
either save the completed work in the original format or a different 
one.  ImageMagick also includes command line programs for creating 
animated or transparent .gifs, creating composite images, creating 
thumbnail images, and more.  

ImageMagick is one of your choices if you need a program to manipulate 
and display images. If you'd also like to develop your own applications 
which use ImageMagick code or APIs, you'll need to install 
ImageMagick-devel as well.

%package devel
Summary: Static libraries and header files for ImageMagick app development.
Group: Development/Libraries
Requires: ImageMagick = %{version}

%description devel
Image-Magick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications.  ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code
or APIs, you'll need to install ImageMagick-devel as well as ImageMagick.
You don't need to install it if you just want to use ImageMagick, 
however.

%package c++
Summary: ImageMagick Magick++ library
Group: System Environment/Libraries
Requires: ImageMagick = %{version}

%description c++
This package contains the Magick++ library, a C++ binding to the ImageMagick
graphics manipulation library.

Install ImageMagick-c++ if you want to use any applications that use Magick++.

%package c++-devel
Summary: C++ bindings for the ImageMagick library
Group: Development/Libraries
Requires: ImageMagick = %{version}, ImageMagick-c++ = %{version}, ImageMagick-devel = %{version}

%description c++-devel
ImageMagick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications using the Magick++ C++ bindings.
ImageMagick is an image manipulation program.

If you want to create applications that will use Magick++ code
or APIs, you'll need to install ImageMagick-c++-devel, ImageMagick-devel and
ImageMagick.
You don't need to install it if you just want to use ImageMagick, or if you
want to develop/compile applications using the ImageMagick C interface,
however.

%prep
%setup -q
%patch0 -p1 -b .path
%patch1 -p1 -b .lpr

rm -f images/Makefile || :

%build
TARGET_PLATFORM=%{_target_platform}
%define _target_platform --target=$TARGET_PLATFORM
%ifarch alpha sparc
RPM_OPT_FLAGS=""
%endif

%ifarch ia64
CFLAGS="-g -D_GNU_SOURCE $RPM_OPT_FLAGS"; export CFLAGS
%else
CFLAGS="-g $RPM_OPT_FLAGS"; export CFLAGS
%endif
mv configure.in configure.in.dontuse # HACK: Don't run libtoolize in %%configure
%configure --prefix=/usr/X11R6 --enable-shared --with-perl --with-x --with-threads --with-magick_plus_plus --without-wmf
mv configure.in.dontuse configure.in
make
make -C Magick++

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%makeinstall PREFIX=$RPM_BUILD_ROOT/usr
%makeinstall -C Magick++ PREFIX=$RPM_BUILD_ROOT/usr

for bin in $RPM_BUILD_ROOT%{_bindir}/*-*-*-* $RPM_BUILD_ROOT%{_mandir}/man*/*-*-*-* ; do
	mv ${bin} `echo ${bin} | sed 's@[^-/]*-[^-/]*-[^-/]*-@@g'`
done
install -m755 utilities/.libs/* $RPM_BUILD_ROOT%{_bindir}/

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%postun c++ -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc www images
%doc README.txt ImageMagick.html
%attr(755,root,root) %{_libdir}/libMagick.so.*
%{_bindir}/*
/usr/lib/perl*/site_perl/*/*/auto/Image
/usr/lib/perl*/site_perl/*/*/Image
%{_mandir}/*/*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_libdir}/libMagick.a
%{_libdir}/libMagick.la
%{_libdir}/libMagick.so
%{_includedir}

%files c++
%defattr(-,root,root)
%{_libdir}/libMagick++.so.*

%files c++-devel
%defattr(-,root,root)
%{_includedir}/Magick++
%{_includedir}/Magick++.h
%{_libdir}/libMagick++.a
%{_libdir}/libMagick++.la
%{_libdir}/libMagick++.so

%changelog
* Sun Apr 29 2001 Bill Nottingham <notting@redhat.com>
- rebuild for C++ exception handling on ia64
- fix build (need -D_GNU_SOURCE at least on ia64...)
- explicitly disable libwmf support

* Mon Jan 08 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- remove patch for s390, it is not necessary

* Mon Jan  1 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.2.7

* Wed Dec 27 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.2.6

* Mon Dec 18 2000 Than Ngo <than@redhat.com>
- ported to s390

* Mon Sep 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.2.4
- Fix up and package the C++ bindings in the new c++/c++-devel packages.

* Wed Aug  2 2000 Matt Wilson <msw@redhat.com>
- rebuild against new libpng

* Wed Jul 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- include images with docs (#10312)

* Thu Jul 13 2000 Matt Wilson <msw@redhat.com>
- don't build with -ggdb, use -g instead.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul  3 2000 Florian La Roche <laroche@redhat.com>
- update to 5.2.2 beta

* Mon Jul  3 2000 Florian La Roche <laroche@redhat.com>
- update to 5.2.1, redone patches as they failed

* Fri Jun 30 2000 Matt Wilson <msw@redhat.com>
- remove hacks to move perl man pages
- don't include the perl*/man stuff, these files go in /usr/share/man now.

* Thu Jun 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable optimization on Alpha and Sparc

* Wed Jun 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 5.2.0
- update URL
- remove redundant CXXFLAGS=$RPM_OPT_FLAGS

* Thu Jun  1 2000 Matt Wilson <msw@redhat.com>
- bootstrap rebuilt to nuke broken libbz2 deps
- add Prefix: tag such that the FHS macros work properly

* Wed May 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- now compiles with bzip2 1.0
- changed buildroot to include version

* Fri May  5 2000 Bill Nottingham <notting@redhat.com>
- fix compilation with new perl

* Sat Mar 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.1.1

* Thu Feb  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Rebuild to get compressed man pages

* Thu Nov 18 1999 Michael K. Johnson <johnsonm@redhat.com>
- ugly hack to print with lpr instead of lp

* Mon Aug 30 1999 Bill Nottingham <notting@redhat.com>
- update to 4.2.9

* Tue Aug 17 1999 Bill Nottingham <notting@redhat.com>
- update to 4.2.8

* Fri Apr 09 1999 Cristian Gafton <gafton@redhat.com>
- include the perl man pages as well

* Tue Apr 06 1999 Michael K. Johnson <johnsonm@redhat.com>
- remove --enable-16bit because it damages interoperability

* Mon Apr  5 1999 Bill Nottingham <notting@redhat.com>
- update to 4.2.2
- change ChangeLog to refer to actual dates. 
- strip binaries

* Thu Apr  1 1999 Bill Nottingham <notting@redhat.com>
- add more files. Oops.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Wed Mar 10 1999 Bill Nottingham <notting@redhat.com>
- version 4.2.1

* Tue Jan 19 1999 Michael K. Johnson <johnsonm@redhat.com>
- changed group

* Tue Jan 19 1999 Cristian Gafton <gafton@redhat.com>
- hacks to make it work with the new perl
- version 4.1.0 (actually installs the sonames as 4.0.10... doh!)
- make sure the libraries have the x bit on

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 21 1998 Cristian Gafton <gafton@redhat.com>
- updated to 4.0.5

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- updated to 4.0.4
- added BuildRoot

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from 3.8.3 to 3.9.1
- removed PNG patch (appears to be fixed)

* Wed Oct 15 1997 Erik Troan <ewt@redhat.com>
- build against new libpng

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Mar 20 1997 Michael Fulbright <msf@redhat.com>
- updated to version 3.8.3.
- updated source and url tags.
