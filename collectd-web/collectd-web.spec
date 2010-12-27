Summary: Contrib web interface to viewing rrd files
Name: collectd-web
Version: 4.9.1
Release: 1%{?dist}
License: GPLv2
Group: System Environment/Daemons
URL: http://collectd.org/
Source: http://collectd.org/files/collectd-%{version}.tar.bz2
Source1: collectd-httpd.conf
Source2: collection.conf

Requires:       collectd >= 4.9, collectd < 5
Requires:       collectd-rrdtool >= 4.9, collectd < 5
Requires:       perl-HTML-Parser, perl-Regexp-Common, rrdtool-perl, httpd

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
This package will allow for a simple web interface to view rrd files created by
collectd.

%prep
%setup -q -n collectd-%{version}

%build

%install

%{__install} -d -m0755 %{buildroot}/%{_datadir}/collectd/collection3/
%{__install} -d -m0755 %{buildroot}/%{_sysconfdir}/httpd/conf.d/

# Convert docs to UTF-8
find contrib/ -type f -exec %{__chmod} a-x {} \;
for f in contrib/README ChangeLog ; do
  mv $f $f.old; iconv -f iso-8859-1 -t utf-8 < $f.old > $f; rm $f.old
done


# copy web interface
cp -ad contrib/collection3/* %{buildroot}/%{_datadir}/collectd/collection3/
rm -f %{buildroot}/%{_datadir}/collectd/collection3/etc/collection.conf
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/collectd.conf
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/collection.conf
ln -s %{_sysconfdir}/collection.conf %{buildroot}/%{_datadir}/collectd/collection3/etc/collection.conf
chmod +x %{buildroot}/%{_datadir}/collectd/collection3/bin/*.cgi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{_datadir}/collectd/collection3/
%config(noreplace) %{_sysconfdir}/httpd/conf.d/collectd.conf
%config(noreplace) %{_sysconfdir}/collection.conf

%changelog
* Wed Dec 22 2010 Timon <timosha@gmail.com> 4.9.1-1
- First build
- from collectd.spec 

