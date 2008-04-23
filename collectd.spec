Summary: Statistics collection daemon for filling RRD files
Name: collectd
Version: 4.3.2
Release: 6
License: GPLv2
Group: System Environment/Daemons
URL: http://collectd.org/

Source: http://collectd.org/files/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: libvirt-devel, libxml2-devel
BuildRequires: rrdtool-devel
BuildRequires: lm_sensors-devel
BuildRequires: curl-devel
BuildRequires: perl-libs, perl-devel
BuildRequires: perl-ExtUtils-MakeMaker
BuildRequires: perl-ExtUtils-Embed
BuildRequires: net-snmp-devel
BuildRequires: libpcap-devel
BuildRequires: mysql-devel

Requires: rrdtool


%description
collectd is a small daemon written in C for performance.  It reads various
system  statistics  and updates  RRD files,  creating  them if necessary.
Since the daemon doesn't need to startup every time it wants to update the
files it's very fast and easy on the system. Also, the statistics are very
fine grained since the files are updated every 10 seconds.


%package apache
Summary:       Apache plugin for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}, curl
%description apache
This plugin collectd data provided by Apache's 'mod_status'.

 
%package email
Summary:       Email plugin for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}, spamassassin
%description email
This plugin collectd data provided by spamassassin.


%package mysql
Summary:       MySQL module for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}, mysql
%description mysql
MySQL querying plugin. This plugins provides data of issued commands,
called handlers and database traffic.
 

%package nginx
Summary:       Nginx plugin for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}, curl
%description nginx
This plugin gets data provided by nginx.


%package -n perl-Collectd
Summary:       Perl bindings for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}, curl
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-Collectd
This package contains Perl bindings and plugin for collectd.


%package sensors
Summary:       Libsensors module for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}, lm_sensors
%description sensors
This plugin for collectd provides querying of sensors supported by
lm_sensors.


%package snmp
Summary:        SNMP module for collectd
Group:          System Environment/Daemons
Requires:       collectd = %{version}, net-snmp
%description snmp
This plugin for collectd provides querying of net-snmp.


%package virt
Summary:       Libvirt plugin for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}, curl
%description virt
This plugin collects information from virtualized guests.


%prep
%setup -q

sed -i.orig -e 's|-Werror||g' Makefile.in */Makefile.in


%build
%configure \
    --disable-static \
    --enable-mysql \
    --enable-sensors \
    --enable-email \
    --enable-apache \
    --enable-perl \
    --enable-unixsock \
    --with-perl-bindings=INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__rm} -rf contrib/SpamAssassin
%{__make} install DESTDIR="%{buildroot}"

%{__install} -Dp -m0644 src/collectd.conf %{buildroot}%{_sysconfdir}/collectd.conf
%{__install} -Dp -m0755 contrib/fedora/init.d-collectd %{buildroot}%{_initrddir}/collectd

%{__install} -d -m0755 %{buildroot}%{_localstatedir}/lib/collectd/

# Convert docs to UTF-8
find contrib/ -type f -exec %{__chmod} a-x {} \;
for f in contrib/README ChangeLog ; do
  mv $f $f.old; iconv -f iso-8859-1 -t utf-8 < $f.old > $f; rm $f.old
done

# Remove Perl hidden .packlist files.
find %{buildroot} -name .packlist -exec rm {} \;
# Remove Perl temporary file perllocal.pod
find %{buildroot} -name perllocal.pod -exec rm {} \;

# Move the Perl examples to a separate directory.
mkdir perl-examples
find contrib -name '*.p[lm]' -exec mv {} perl-examples/ \;

# Move config contribs
mkdir -p $RPM_BUILD_ROOT/etc/collectd.d/
cp contrib/redhat/apache.conf $RPM_BUILD_ROOT/etc/collectd.d/apache.conf
cp contrib/redhat/email.conf $RPM_BUILD_ROOT/etc/collectd.d/email.conf
cp contrib/redhat/sensors.conf $RPM_BUILD_ROOT/etc/collectd.d/sensors.conf
cp contrib/redhat/mysql.conf $RPM_BUILD_ROOT/etc/collectd.d/mysql.conf
cp contrib/redhat/nginx.conf $RPM_BUILD_ROOT/etc/collectd.d/nginx.conf
cp contrib/redhat/snmp.conf $RPM_BUILD_ROOT/etc/collectd.d/snmp.conf

# *.la files shouldn't be distributed.
rm -f $RPM_BUILD_ROOT/%{_libdir}/collectd/*.la


%post
/sbin/chkconfig --add collectd


%preun
if [ $1 -eq 0 ]; then
    /sbin/service collectd stop &>/dev/null || :
    /sbin/chkconfig --del collectd
fi


%postun
/sbin/service collectd condrestart &>/dev/null || :


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, -)

%config(noreplace) %{_sysconfdir}/collectd.conf
%config(noreplace) %{_sysconfdir}/collectd.d/

%{_initrddir}/collectd
%{_bindir}/collectd-nagios
%{_sbindir}/collectd
%{_sbindir}/collectdmon
%dir %{_localstatedir}/lib/collectd/

%{_libdir}/collectd/*.so*
%{_libdir}/collectd/types.db
%exclude %{_libdir}/collectd/apache.so*
%exclude %{_libdir}/collectd/email.so*
%exclude %{_libdir}/collectd/libvirt.so*
%exclude %{_libdir}/collectd/mysql.so*
%exclude %{_libdir}/collectd/nginx.so*
%exclude %{_libdir}/collectd/perl.so*
%exclude %{_libdir}/collectd/sensors.so*
%exclude %{_libdir}/collectd/snmp.so*

%doc AUTHORS ChangeLog COPYING INSTALL README
%doc %{_mandir}/man1/collectd.1*
%doc %{_mandir}/man1/collectd-nagios.1*
%doc %{_mandir}/man1/collectdmon.1*
%doc %{_mandir}/man5/collectd.conf.5*
%doc %{_mandir}/man5/collectd-exec.5*
%doc %{_mandir}/man5/collectd-unixsock.5*
%doc %{_mandir}/man5/types.db.5*


%files apache
%doc COPYING
%{_libdir}/collectd/apache.so*
%config(noreplace) %{_sysconfdir}/collectd.d/apache.conf


%files email
%doc COPYING
%{_libdir}/collectd/email.so*
%config(noreplace) %{_sysconfdir}/collectd.d/email.conf
%doc %{_mandir}/man5/collectd-email.5*


%files mysql
%doc COPYING
%{_libdir}/collectd/mysql.so*
%config(noreplace) %{_sysconfdir}/collectd.d/mysql.conf


%files nginx
%doc COPYING
%{_libdir}/collectd/nginx.so*
%config(noreplace) %{_sysconfdir}/collectd.d/nginx.conf


%files -n perl-Collectd
%doc COPYING perl-examples/*
%{_libdir}/collectd/perl.so*
%{perl_vendorlib}/Collectd.pm
%{perl_vendorlib}/Collectd/
%doc %{_mandir}/man5/collectd-perl.5*
%doc %{_mandir}/man3/Collectd::Unixsock.3pm*

%files sensors
%doc COPYING
%{_libdir}/collectd/sensors.so*
%config(noreplace) %{_sysconfdir}/collectd.d/sensors.conf


%files snmp
%doc COPYING
%{_libdir}/collectd/snmp.so*
%config(noreplace) %{_sysconfdir}/collectd.d/snmp.conf
%doc %{_mandir}/man5/collectd-snmp.5*


%files virt
%doc COPYING
%{_libdir}/collectd/libvirt.so*


%changelog
* Thu Apr 17 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-6
- Exclude perl.so from the main package.

* Thu Apr 17 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-5
- Put the perl bindings and plugin into a separate perl-Collectd
  package.  Note AFAICT from the manpage, the plugin and Collectd::*
  perl modules must all be packaged together.

* Wed Apr 16 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-4
- Remove -devel subpackage.
- Add subpackages for apache, email, mysql, nginx, sensors,
  snmp (thanks Richard Shade).
- Add subpackages for perl, libvirt.

* Tue Apr 15 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-2
- Install Perl bindings in vendor dir not site dir.

* Tue Apr 15 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-1
- New upstream version 4.3.2.
- Create a -devel subpackage for development stuff, examples, etc.
- Use .bz2 package instead of .gz.
- Remove fix-hostname patch, now upstream.
- Don't mark collectd init script as config.
- Enable MySQL, sensors, email, apache, Perl, unixsock support.
- Don't remove example Perl scripts.
- Package types.db(5) manpage.
- Fix defattr.
- Build in koji to find the full build-requires list.

* Mon Apr 14 2008 Richard W.M. Jones <rjones@redhat.com> - 4.2.3.100.g79b0797-2
- Prepare for Fedora package review:
- Clarify license is GPLv2 (only).
- Setup should be quiet.
- Spelling mistake in original description fixed.
- Don't include NEWS in doc - it's an empty file.
- Convert some other doc files to UTF-8.
- config(noreplace) on init file.

* Thu Jan 10 2008 Chris Lalancette <clalance@redhat.com> - 4.2.3.100.g79b0797.1.ovirt
- Update to git version 79b0797
- Remove *.pm files so we don't get a bogus dependency
- Re-enable rrdtool; we will need it on the WUI side anyway

* Mon Oct 29 2007 Dag Wieers <dag@wieers.com> - 4.2.0-1 - 5946+/dag
- Updated to release 4.2.0.

* Mon Oct 29 2007 Dag Wieers <dag@wieers.com> - 3.11.5-1
- Initial package. (using DAR)
