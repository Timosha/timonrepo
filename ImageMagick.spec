# ImageMagick has adopted a new Version.Patchlevel version numbering system...
# 5.4.0.3 is actually version 5.4.0, Patchlevel 3.
%define VER 5.4.3
%define Patchlevel 5
Summary: An X application for displaying and manipulating images.
Name: ImageMagick
%if "%{Patchlevel}" != ""
Version: %{VER}.%{Patchlevel}
%else
Version: %{VER}
%endif
Release: 1
License: freeware
Group: Applications/Multimedia
%if "%{Patchlevel}" != ""
Source: ftp://ftp.cdrom.com/pub/ImageMagick/ImageMagick-%{VER}-%{Patchlevel}.tar.bz2
%else
Source: ftp://ftp.cdrom.com/pub/ImageMagick/ImageMagick-%{version}.tar.bz2
%endif
Source1: magick_small.png
Patch1: ImageMagick-5.3.5-lprhack.patch
Patch2: ImageMagick-5.3.6-nonroot.patch
Patch3: ImageMagick-5.3.7-config.patch
Patch4: ImageMagick-5.4.0-hp2xx.patch
Patch5: ImageMagick-5.4.2-localdoc.patch
Url: http://www.imagemagick.org/
Buildroot: %{_tmppath}/%{name}-%{version}-root
BuildPrereq: bzip2-devel, freetype-devel, libjpeg-devel, libpng-devel
BuildPrereq: libtiff-devel, libungif-devel, zlib-devel, perl
Requires: bzip2, freetype, libjpeg, libpng, libtiff, libungif, zlib
BuildRequires: freetype-devel >= 2.0.1
%define _prefix /usr/X11R6
%define _mandir %{_prefix}/man
%define _includedir %{_prefix}/include/X11/magick

%description
ImageMagick(TM) is an image display and manipulation tool for the X
Window System. ImageMagick can read and write JPEG, TIFF, PNM, GIF,
and Photo CD image formats. It can resize, rotate, sharpen, color
reduce, or add special effects to an image, and when finished you can
either save the completed work in the original format or a different
one. ImageMagick also includes command line programs for creating
animated or transparent .gifs, creating composite images, creating
thumbnail images, and more.

ImageMagick is one of your choices if you need a program to manipulate
and dis play images. If you want to develop your own applications
which use ImageMagick code or APIs, you need to install
ImageMagick-devel as well.

%package devel
Summary: Static libraries and header files for ImageMagick app development.
Group: Development/Libraries
Requires: ImageMagick = %{version}-%{release}

%description devel
Image-Magick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications. ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code or
APIs, you need to install ImageMagick-devel as well as ImageMagick.
You do noy need to install it if you just want to use ImageMagick,
however.

%package perl
Summary: ImageMagick perl bindings
Group: System Environment/Libraries
Requires: ImageMagick = %{version}-%{release}, perl >= 5.6.0

%description perl
Perl bindings to ImageMagick.

Install ImageMagick-perl if you want to use any perl scripts that use
ImageMagick.

%package c++
Summary: ImageMagick Magick++ library (C++ bindings)
Group: System Environment/Libraries
Requires: ImageMagick = %{version}-%{release}

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
%setup -q -n %{name}-%{VER}
%patch1 -p1 -b .lpr
%patch2 -p1 -b .nonroot
%patch3 -p1 -b .config
%patch4 -p1 -b .hp2xx
%patch5 -p1 -b .ImageMagick
# Fix up a dependency
perl -pi -e "s,-L/home/cristy/ImageMagick/magick,-L../magick/.libs,g" PerlMagick/Makefile.PL

%build
libtoolize --force
aclocal
automake || :
autoconf || :
%configure --prefix=%{_prefix} --enable-shared \
           --with-perl --with-x \
           --with-threads --with-magick_plus_plus
make

%install
rm -rf $RPM_BUILD_ROOT

make PerlMagick/Makefile
perl -pi -e 's,^PREFIX.*,PREFIX = \$(DESTDIR)/usr,g;s,^config :: Makefile,config :: ,g;s,Makefile : ,Foo : ,g' PerlMagick/Makefile
perl -pi -e "s,-lMagick,-L../magick/.libs -lMagick,g" PerlMagick/Makefile
cat >>PerlMagick/Makefile <<EOF
Makefile:
	touch Makefile
EOF
perl -pi -e 's,^install-exec-perl:.*,install-exec-perl:,g' Makefile
rm -f PerlMagick/Makefile.*
make install DESTDIR=$RPM_BUILD_ROOT

# Generate desktop file
mkdir -p $RPM_BUILD_ROOT/usr/share/icons $RPM_BUILD_ROOT/etc/X11/applnk/Graphics
cp %{SOURCE1} $RPM_BUILD_ROOT/usr/share/icons

# Add files make install constantly forgets
install -c -m 644 coders/*.mgk $RPM_BUILD_ROOT/usr/X11R6/share/ImageMagick

cat >$RPM_BUILD_ROOT/etc/X11/applnk/Graphics/ImageMagick.desktop <<EOF
[Desktop Entry]
Name=ImageMagick
Comment=The ImageMagick picture viewer and editor
Comment[de]=Der ImageMagick-Bilderbetrachter und -editor
Exec=%{_prefix}/bin/display
Icon=magick_small.png
Terminal=0
Type=Application
EOF

find $RPM_BUILD_ROOT -name "*.bs" |xargs rm -f
find $RPM_BUILD_ROOT -name ".packlist" |xargs rm -f

# Grr... Broken makefiles!!
perlver=`perl -v |grep built |sed -e "s,.*v,,;s, .*,,"`
perlmajor=`echo $perlver |sed -e "s,\..*,,"`
if [ -d $RPM_BUILD_ROOT/usr/lib/$perlver ]; then
	mkdir -p $RPM_BUILD_ROOT/usr/lib/perl$perlmajor/site_perl/$perlver
	mv $RPM_BUILD_ROOT/usr/lib/$perlver/* $RPM_BUILD_ROOT/usr/lib/perl$perlmajor/site_perl/$perlver/
	rm -rf $RPM_BUILD_ROOT/usr/lib/$perlver
fi
if [ -d $RPM_BUILD_ROOT/usr/lib/site_perl ]; then
	for i in `find $RPM_BUILD_ROOT/usr/lib/site_perl/ -type d`; do
		mkdir -p `echo $i |sed -e "s,site_perl,perl$perlmajor/site_perl,g"` || :
	done
	for i in `find $RPM_BUILD_ROOT/usr/lib/site_perl/ -type f`; do
		mv -f `echo $i |sed -e "s,site_perl,perl$perlmajor/site_perl,g"` || :
	done
fi

cd $RPM_BUILD_ROOT/%{_bindir}
for i in %{_arch}-redhat-linux-*; do
	mv $i `echo $i |sed -e "s/^%{_arch}-redhat-linux-//"`
done
cd $RPM_BUILD_ROOT/%{_mandir}
for i in */%{_arch}-redhat-linux-*; do
	mv $i `echo $i |sed -e "s,/%{_arch}-redhat-linux-,/,"`
done


%clean
rm -rf $RPM_BUILD_ROOT

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
%{_mandir}/*/*
%{_datadir}/*
/etc/X11/applnk/Graphics/ImageMagick.desktop
/usr/share/icons/magick_small.png

%files devel
%defattr(-,root,root)
%{_libdir}/libMagick.a
%{_libdir}/libMagick.la
%{_libdir}/libMagick.so
%{_includedir}/magick

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

%files perl
%defattr(-,root,root)
/usr/lib/perl*/site_perl/*/*/auto/Image
/usr/lib/perl*/site_perl/*/*/Image

%changelog
* Fri Feb 22 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.3.5-1
- Update to 5.4.3 pl5; this fixes #58080

* Thu Jan 17 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.2.3-1
- Patchlevel 3

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jan  4 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.2.2-1
- Update to 5.4.2-2
- Fix #57923, also don't hardcode netscape as html viewer

* Wed Dec  5 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.1-1
- 5.4.1
- Link against new libstdc++

* Fri Nov  9 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.0.5-1
- 5.4.0.5
- Make the error message when trying to display an hpgl file more
  explicit (#55875)

* Mon Nov  5 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.0.3-1
- 5.4.0.3
- Fix names of man pages

* Mon Oct 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.4.0-1
- 5.4.0
- work around build system breakage causing applications to be named
  %{_arch}-redhat-linux-foo rather than foo

* Wed Sep 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.9-1
- 5.3.9

* Mon Aug 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.8-3
- Add delegates.mgk back, got lost during the update to 5.3.8 (Makefile bug)
  (#52611)

* Mon Aug 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.8-2
- Remove Magick++ includes from -devel, they're already in -c++-devel
  (#51590)

* Sun Jul 28 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.8-1
- 5.3.8 (bugfix release)

* Sat Jul 27 2001 Than Ngo <than@redhat.com> 5.3.7-3
- fix to build Perlmagic on s390 s390x

* Thu Jul 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.7-2
- Add delegates.mgk to the package (#50725)

* Tue Jul 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.7-1
- 5.3.7
- Fix build without previously installed ImageMagick-devel (#49816)
- Move perl bindings to a separate package.

* Mon Jul  9 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.6-2
- Fix build as non-root again
- Shut up rpmlint

* Tue Jul  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.6-1
- 5.3.6
- Get rid of the ia64 patch, it's no longer needed since glibc was fixed

* Sat Jun 16 2001 Than Ngo <than@redhat.com>
- update to 5.3.5
- cleanup specfile

* Sat May 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.3-2
- 5.3.3-respin, fixes #41196

* Tue May  1 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.3.3-1
- 5.3.3
- Add a desktop file for "display" (RFE#17417)

* Sun Apr 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.3.2
- work around bugs in ia64 glibc headers

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
