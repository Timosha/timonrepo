%global uid	52

Summary:	Advanced key-value store
Name:		redis
Version:	2.0.4
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://code.google.com/p/redis/

Source0:	http://redis.googlecode.com/files/redis-%{version}.tar.gz
#Source1:	redis.conf
Source2:	redis.init
Source3:	redis.logrotate
Patch1:		redis-2.0.conf.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	fedora-usermgmt-devel
%{?FE_USERADD_REQ}

Requires(post):		/sbin/chkconfig
Requires(preun):	/sbin/chkconfig
Requires(preun):	/sbin/service
Requires(postun):	/sbin/service

%description
Redis is a key-value database. It is similar to memcached but the dataset is
not volatile, and values can be strings, exactly like in memcached, but also
lists and sets with atomic operations to push/pop elements.

In order to be very fast but at the same time persistent the whole dataset is
taken in memory and from time to time and/or when a number of changes to the
dataset are performed it is written asynchronously on disk. You may lose the
last few queries that is acceptable in many applications but it is as fast
as an in memory DB (beta 6 of Redis includes initial support for master-slave
replication in order to solve this problem by redundancy).

Compression and other interesting features are a work in progress. Redis is
written in ANSI C and works in most POSIX systems like Linux, *BSD, Mac OS X,
and so on. Redis is free software released under the very liberal BSD license.

%prep
%setup -q
%patch1 -p1 -b redis.conf

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}%{_bindir}
%{__install} -Dp -m 0755 redis-server %{buildroot}%{_sbindir}/redis-server
%{__install} -Dp -m 0755 redis-benchmark %{buildroot}%{_bindir}/redis-benchmark
%{__install} -Dp -m 0755 redis-cli %{buildroot}%{_bindir}/redis-cli

%{__install} -Dp -m 0644 redis.conf %{buildroot}%{_sysconfdir}/redis.conf
%{__install} -Dp -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/init.d/redis
%{__install} -Dp -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/redis

%{__install} -p -d -m 0750 %{buildroot}%{_sharedstatedir}/redis
%{__install} -p -d -m 0755 %{buildroot}%{_localstatedir}/log/redis
%{__install} -p -d -m 0755 %{buildroot}%{_localstatedir}/run/redis

%pre
%{__fe_groupadd} %{uid} -r %{name} &>/dev/null || :
%{__fe_useradd} %{uid} -r -s /sbin/nologin -d %{_sharedstatedir}/%{name} -M \
			-c '%{name}' -g %{name} %{name} &>/dev/null || :


%preun
if [ $1 = 0 ]; then
    # make sure redis service is not running before uninstalling

    # when the preun section is run, we've got stdin attached.  If we
    # call stop() in the redis init script, it will pass stdin along to
    # the redis-cli script; this will cause redis-cli to read an extraneous
    # argument, and the redis-cli shutdown will fail due to the wrong number
    # of arguments.  So we do this little bit of magic to reconnect stdin
    # to the terminal
    term="/dev/$(ps -p$$ --no-heading | awk '{print $2}')"
    exec < $term

    /sbin/service %{name} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%post
/sbin/chkconfig --add %{name}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc doc/*.html
%doc Changelog 00-RELEASENOTES COPYING README
%{_sbindir}/redis-server
%{_bindir}/redis-benchmark
%{_bindir}/redis-cli
%{_sysconfdir}/init.d/redis
%config(noreplace) %{_sysconfdir}/redis.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/redis
%dir %attr(0750,redis,redis) %{_localstatedir}/lib/redis
%dir %attr(0755,redis,redis) %{_localstatedir}/run/redis
%dir %attr(0755,redis,redis) %{_localstatedir}/log/redis

%changelog
* Mon Nov 15 2010 Timon <timosha@gmail.com> 2.0.4-1
- new package built with tito

* Tue Oct 26 2010 Timon <timosha@gmail.com> 2.0.4-1
- new version

* Tue Oct 26 2010 Timon <timosha@gmail.com> 2.0.3-2
- fix redis.pid

* Tue Oct 26 2010 Timon <timosha@gmail.com> 2.0.3-1
- updated to 2.0.3

* Thu Sep 16 2010 Timon <timosha@gmail.com> 2.0.1-5
- fix logs
- fix data dir
- fix config

* Wed Sep 15 2010 Timon <timosha@gmail.com> 2.0.1-1
- updated to 2.0.1 
- first fedora release
- split spec to init and logrotate files
- fix dir rights

* Tue Jul 13 2010 - jay at causes dot com 2.0.0-rc2
- upped to 2.0.0-rc2

* Mon May 24 2010 - jay at causes dot com 1.3.9-2
- moved pidfile back to /var/run/redis/redis.pid, so the redis
  user can write to the pidfile.
- Factored it out into %{pid_dir} (/var/run/redis), and
  %{pid_file} (%{pid_dir}/redis.pid)


* Wed May 05 2010 - brad at causes dot com 1.3.9-1
- redis updated to version 1.3.9 (development release from GitHub)
- extract config file from spec file
- move pid file from /var/run/redis/redis.pid to just /var/run/redis.pid
- move init file to /etc/init.d/ instead of /etc/rc.d/init.d/

* Fri Sep 11 2009 - jpriebe at cbcnewmedia dot com 1.0-1
- redis updated to version 1.0 stable

* Mon Jun 01 2009 - jpriebe at cbcnewmedia dot com 0.100-1
- Massive redis changes in moving from 0.09x to 0.100
- removed log timestamp patch; this feature is now part of standard release

* Tue May 12 2009 - jpriebe at cbcnewmedia dot com 0.096-1
- A memory leak when passing more than 16 arguments to a command (including
  itself).
- A memory leak when loading compressed objects from disk is now fixed.

* Mon May 04 2009 - jpriebe at cbcnewmedia dot com 0.094-2
- Patch: applied patch to add timestamp to the log messages
- moved redis-server to /usr/sbin
- set %config(noreplace) on redis.conf to prevent config file overwrites
  on upgrade

* Fri May 01 2009 - jpriebe at cbcnewmedia dot com 0.094-1
- Bugfix: 32bit integer overflow bug; there was a problem with datasets
  consisting of more than 20,000,000 keys resulting in a lot of CPU usage
  for iterated hash table resizing.

* Wed Apr 29 2009 - jpriebe at cbcnewmedia dot com 0.093-2
- added message to init.d script to warn user that shutdown may take a while

* Wed Apr 29 2009 - jpriebe at cbcnewmedia dot com 0.093-1
- version 0.093: fixed bug in save that would cause a crash
- version 0.092: fix for bug in RANDOMKEY command

* Fri Apr 24 2009 - jpriebe at cbcnewmedia dot com 0.091-3
- change permissions on /var/log/redis and /var/run/redis to 755; this allows
  non-root users to check the service status and to read the logs

* Wed Apr 22 2009 - jpriebe at cbcnewmedia dot com 0.091-2
- cleanup of temp*rdb files in /var/lib/redis after shutdown
- better handling of pid file, especially with status

* Tue Apr 14 2009 - jpriebe at cbcnewmedia dot com 0.091-1
- Initial release.
