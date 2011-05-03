Name:           lsyncd
Version:        2.0.4
Release:        1%{?dist}
Summary:        File change monitoring and synchronization daemon

Group:          Applications/Internet
License:        GPLv2+
URL:            http://code.google.com/p/lsyncd/
Source0:        http://lsyncd.googlecode.com/files/%{name}-%{version}.tar.gz
# http://code.google.com/p/lsyncd/issues/detail?id=55
Patch0:         lsyncd-2.0.4-execstack.patch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  lua-devel >= 5.1.3

%description
Lsyncd watches a local directory trees event monitor interface (inotify).
It aggregates and combines events for a few seconds and then spawns one
(or more) process(es) to synchronize the changes. By default this is
rsync.

Lsyncd is thus a light-weight live mirror solution that is comparatively
easy to install not requiring new file systems or block devices and does
not hamper local file system performance.


%prep
%setup -q
%patch0 -p1


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/lsyncd
%{_mandir}/man1/lsyncd.1*
%exclude %{_docdir}/lsyncd
%doc COPYING ChangeLog examples


%changelog
* Fri Apr 29 2011 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 2.0.4-1
- Initial packaging
