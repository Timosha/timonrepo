%global beta     beta3
%global username cassandra
%global uid 	 53

%define subversion -%{beta}

Name:           apache-cassandra
Version:        0.7.0
Release:        0.2.%{beta}%{?dist}
Summary:        Cassandra is a highly scalable, eventually consistent, distributed, structured key-value store.

Group:          Development/Libraries
License:        BSD
URL:            http://cassandra.apache.org/
#Source0:        http://www.ibiblio.org/pub/mirrors/apache/%{username}/%{version}/%{name}-%{version}-src.tar.gz
#Source:		http://www.sai.msu.su/apache//cassandra/0.7.0/apache-cassandra-0.7.0-beta1-src.tar.gz
#Source:		ftp://apache.rinet.ru/pub/mirror/apache.org/dist//cassandra/0.7.0/apache-cassandra-0.7.0-beta1-src.tar.gz
Source:		http://www.eu.apache.org/dist//cassandra/%{version}/%{name}-%{version}%{subversion}-src.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: ant
BuildRequires: ant-nodeps

Requires:      java >= 1.6.0
Requires:      jpackage-utils

BuildRequires: fedora-usermgmt-devel
%{?FE_USERADD_REQ}

BuildArch:      noarch

%description
Cassandra brings together the distributed systems technologies from Dynamo
and the data model from Google's BigTable. Like Dynamo, Cassandra is
eventually consistent. Like BigTable, Cassandra provides a ColumnFamily-based
data model richer than typical key/value systems.

For more information see http://cassandra.apache.org/

%prep
%setup -q -n %{name}-%{version}%{subversion}-src

%build
ant clean jar -Drelease=true

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/%{username}/
mkdir -p %{buildroot}/usr/share/%{username}
mkdir -p %{buildroot}/usr/share/%{username}/lib
mkdir -p %{buildroot}/usr/share/%{username}/default.conf
mkdir -p %{buildroot}/etc/%{username}/default.conf
mkdir -p %{buildroot}/etc/rc.d/init.d/
mkdir -p %{buildroot}/usr/sbin
mkdir -p %{buildroot}/usr/bin
cp -p conf/* %{buildroot}/etc/%{username}/default.conf
cp -p conf/* %{buildroot}/usr/share/%{username}/default.conf
cp -p contrib/redhat/%{username} %{buildroot}/etc/rc.d/init.d/
cp -p lib/*.jar %{buildroot}/usr/share/%{username}/lib
mv bin/cassandra.in.sh %{buildroot}/usr/share/%{username}
mv bin/cassandra %{buildroot}/usr/sbin
rm bin/*.bat 
cp -p bin/* %{buildroot}/usr/bin
cp build/%{name}-%{version}%{subversion}.jar %{buildroot}/usr/share/%{username}/lib
mkdir -p %{buildroot}/var/lib/%{username}/commitlog
mkdir -p %{buildroot}/var/lib/%{username}/data
mkdir -p %{buildroot}/var/lib/%{username}/saved_caches
mkdir -p %{buildroot}/var/run/%{username}
mkdir -p %{buildroot}/var/log/%{username}

%clean
%{__rm} -rf %{buildroot}

%pre
%{__fe_groupadd} %{uid} -r %{username} &>/dev/null || :
%{__fe_useradd} %{uid} -r -s /sbin/nologin -d %{_sharedstatedir}/%{username} -M \
			-c '%{name}' -g %{username} %{username} &>/dev/null || :
%preun
if [ $1 = 0 ]; then
    /sbin/service %{username} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{username}
fi

%post
alternatives --install /etc/%{username}/conf %{username} /etc/%{username}/default.conf/ 0
/sbin/chkconfig --add %{username}
exit 0

%postun
# only delete alternative on removal, not upgrade
if [ "$1" = "0" ]; then
    alternatives --remove %{username} /etc/%{username}/default.conf/
fi
exit 0


%files
%defattr(-,root,root,0755)
%doc CHANGES.txt LICENSE.txt README.txt NEWS.txt NOTICE.txt
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/cassandra
%attr(755,root,root) /etc/rc.d/init.d/%{username}
%attr(755,%{username},%{username}) /usr/share/%{username}*
%attr(755,%{username},%{username}) %config(noreplace) %{_sysconfdir}/%{username}
%attr(755,%{username},%{username}) %config(noreplace) %{_sharedstatedir}/%{username}/*
%attr(755,%{username},%{username}) /var/log/%{username}*
%attr(755,%{username},%{username}) /var/run/%{username}*


%changelog
* Mon Nov 15 2010 Timon <timosha@gmail.com> - 0.7.0-2.beta3
- Bump new version.

* Tue Aug 03 2010 Nick Bailey <nicholas.bailey@rackpace.com> - 0.7.0-1
- Updated to make configuration easier and changed package name.

* Mon Jul 05 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.3-1
- Initial package
