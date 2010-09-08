%global uid	52

Name:           erlyvideo
Version:        2.1.10
Release:        1%{?dist}
Summary:        Flash streaming server, written in erlang

Group:          Applications/Internet
License:        GPLv3
URL:            http://www.erlyvideo.org/
# git clone http://github.com/erlyvideo/erlyvideo.git erlyvideo
# GIT_DIR=erlyvideo/.git git archive --format=tar --prefix=erlyvideo-2.1.10/ v2.1.10 | bzip2 > erlyvideo-2.1.10.tar.bz2
Source0:        %{name}-%{version}.tar.bz2
Source1:        erlyvideo.init
Source2:	erlyvideo.sysconfig
#Source2:       ejabberd.logrotate


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       erlang 
Requires:	erlang-amf erlang-erlydtl erlang-log4erl erlang-misultin 
Requires:	erlang-erlmedia erlang-rtmp erlang-rtsp erlang-mpegts

BuildRequires:  erlang erlang-rtmp-devel erlang-erlmedia-devel
#BuildRequires:	 erlang-amf-devel erlang-ertp-devel 
#BuildRequires:	erlang-misultin-devel erlang-mpegts-devel erlang-rtmp-devel erlang-rtsp-devel
BuildRequires:  ruby

BuildRequires:	fedora-usermgmt-devel
%{?FE_USERADD_REQ}

Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service

Provides: user(%{name}) = %{uid}
Provides: group(%{name}) = %{uid}

#TODO: write desc
%description
Erlyvideo is a flash streaming server, written in erlang.

#%package doc
#Summary: Documentation for erlyvideo
#BuildArch: noarch
#Requires: %{name} = %{version}-%{release}
#Group: Documentation

#%description doc
#Documentation for erlyvideo.

%prep
%setup -q -n %{name}-%{version}

#remove ruby
#sed -i -e '1c\VERSION:=%{version}' Makefile

%build
%{__make}

%install
rm -rf %{buildroot}
#%{__make} install DESTROOT=%{buildroot}
#TODO: fix rights
#%{__mkdir} -p %{buildroot}%{_libdir}/%{name}
#%{__install} -D -d -m 755 %{buildroot}%{_libdir}/%{name}

%{__mkdir} -p %{buildroot}%{_libdir}/%{name}/{ebin,src,include}
%{__install} -m 644 ebin/* %{buildroot}%{_libdir}/%{name}/ebin
#%{__install} -m 644 src/* %{buildroot}%{_libdir}/%{name}/src
%{__install} -m 644 include/* %{buildroot}%{_libdir}/%{name}/include
#%{__install} -m 644 lib/misultin/* %{buildroot}%{_libdir}/%{name}/lib/misultin
#%{__cp} -r deps/* %{buildroot}%{_libdir}/%{name}/lib

%{__install} -D -m 755 contrib/reverse_mpegts %{buildroot}%{_bindir}/reverse_mpegts
#%{__install} -m 755 contrib/erlyctl.debian %{buildroot}%{_bindir}

## TODO: make Fedora conf's
%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
%{__install} -m 644 priv/erlyvideo.conf.debian %{buildroot}%{_sysconfdir}/%{name}/erlyvideo.conf
%{__install} -m 644 priv/log4erl.conf.debian %{buildroot}%{_sysconfdir}/%{name}/log4erl.conf
%{__install} -m 644 priv/production.config.debian %{buildroot}%{_sysconfdir}/%{name}/production.config

%{__install} -D -m 755 %{SOURCE1} %{buildroot}%{_initddir}/%{name}
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%{__install} -D -d -m 755 %{buildroot}%{_datadir}/%{name}
%{__cp} -r wwwroot %{buildroot}%{_datadir}/%{name}

%{__install} -D -d %{buildroot}%{_localstatedir}/log/%{name}
%{__install} -D -d %{buildroot}%{_localstatedir}/lib/%{name}



#mkdir -p %{buildroot}/var/log/ejabberd
#mkdir -p %{buildroot}/var/lib/ejabberd/spool

#mkdir -p %{buildroot}%{_bindir}
#ln -s consolehelper %{buildroot}%{_bindir}/ejabberdctl
#install -D -p -m 0644 %{S:9} %{buildroot}%{_sysconfdir}/pam.d/ejabberdctl
#install -D -p -m 0644 %{S:10} %{buildroot}%{_sysconfdir}/security/console.apps/ejabberdctl
#install -D -p -m 0644 %{S:11} %{buildroot}%{_sysconfdir}/pam.d/ejabberd

# install init-script
#install -D -p -m 0755 %{S:1} %{buildroot}%{_initrddir}/ejabberd

# install config for logrotate
#install -D -p -m 0644  %{S:2} %{buildroot}%{_sysconfdir}/logrotate.d/ejabberd

# install sysconfig file
#install -D -p -m 0644  %{S:3} %{buildroot}%{_sysconfdir}/sysconfig/ejabberd

# rename doc-files directory properly
#mv %{buildroot}%{_docdir}/%{name}{,-%{version}}

# Clean up false security measure
#chmod 755 %{buildroot}%{_sbindir}/ejabberdctl

%pre
%{__fe_groupadd} %{uid} -r %{name} &>/dev/null || :
%{__fe_useradd} %{uid} -r -s /sbin/nologin -d /var/lib/erlyvideo -M \
			-c 'erlyvideo' -g %{name} %{name} &>/dev/null || :

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
        /sbin/service %{name} stop >/dev/null 2>&1
        /sbin/chkconfig --del %{name}
fi


%postun
if [ "$1" -ge "1" ]; then
        /sbin/service %{name} condrestart >/dev/null 2>&1
fi


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

#%dir %{_docdir}/%{name}-%{version}
#%doc %{_docdir}/%{name}-%{version}/COPYING

#%attr(750,root,root) 
%dir %{_sysconfdir}/erlyvideo
#%attr(640,root,root) 
%config(noreplace) %{_sysconfdir}/erlyvideo/*

%{_initddir}/erlyvideo

#%config(noreplace) %{_sysconfdir}/logrotate.d/ejabberd
%config(noreplace) %{_sysconfdir}/sysconfig/erlyvideo
%{_bindir}/reverse_mpegts
#%{_sbindir}/ejabberdctl

%dir %{_libdir}/%{name}
#%dir %{_libdir}/%{name}/ebin

%{_libdir}/%{name}/ebin
#%{_libdir}/%{name}/ebin/*.beam
%{_libdir}/%{name}/include
#%{_libdir}/%{name}/lib
#%{_libdir}/%{name}/include/adhoc.hrl
#%{_libdir}/%{name}/include/ejabberd.hrl
#%{_libdir}/%{name}/include/ejabberd_commands.hrl
#%{_libdir}/%{name}/include/ejabberd_config.hrl
#%{_libdir}/%{name}/include/ejabberd_ctl.hrl
#%{_libdir}/%{name}/include/eldap/ELDAPv3.hrl
#%{_libdir}/%{name}/include/eldap/eldap.hrl
#%{_libdir}/%{name}/include/jlib.hrl

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/wwwroot

%attr(755,erlyvideo,erlyvideo) %dir /var/lib/erlyvideo
#%attr(750,ejabberd,ejabberd) %dir /var/lib/ejabberd/spool
#%attr(750,ejabberd,ejabberd) %dir /var/lock/ejabberdctl
%attr(755,erlyvideo,erlyvideo) %dir /var/log/erlyvideo

#%files doc
#%defattr(-,root,root,-)
#%doc %{_docdir}/%{name}-%{version}/*.html
#%doc %{_docdir}/%{name}-%{version}/*.png
#%doc %{_docdir}/%{name}-%{version}/*.pdf
#%doc %{_docdir}/%{name}-%{version}/*.txt

%changelog
* Wed Sep 8 2010 Timon <timosha@gmail.com> - 2.1.10-1
- fix deps
- new upstream release

* Tue Jul 27 2010 Timon <timosha@gmail.com> - 2.0.3-0.3.20100726git
- add wwwroot
- add user

* Fri Jul 26 2010 Timon <timosha@gmail.com> - 2.0.3-0.2.20100726git
- version 2.0.3
- add init and sysconfig

* Fri Jul 23 2010 Timon <timosha@gmail.com> - 2.0.2-0.1.20100723git
- First version for Fedora


