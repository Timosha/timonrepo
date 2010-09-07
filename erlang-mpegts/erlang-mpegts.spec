#%global gitdate 20100605
%global realname mpegts

Summary:	MpegTS support for Erlang
Name:		erlang-mpegts
Version:	2.3.4
Release:	1%{?dist}
Group:		Development/Libraries
License:	GPLv3
URL:		http://github.com/erlyvideo/ertsp
# git clone http://github.com/erlyvideo/mpegts.git mpegts
# GIT_DIR=mpegts/.git git archive --format=tar --prefix=mpegts-2.3.4/ v2.3.4 | bzip2 > mpegts-2.3.4.tar.bz2
Source:		%{realname}-%{version}.tar.bz2

BuildRequires:	erlang ruby
BuildRequires:	erlang-erlmedia-devel

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	erlang-erlmedia


%description
erlang-mpegts is a library, extracted from Erlyvideo. 
It handles RTSP and RTP protocols.
It requires erlmedia for unpacking RTP payload

%package devel
Summary:	Development files for erlang-mpegts
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for erlang-mpegts.


%prep
%setup -q -n %{realname}-%{version}

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,src}
%{__install} -c -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%{__install} -c -m 644 ebin/*.so %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%{__install} -c -m 644 src/* %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/src/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.md COPYING
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin

%files devel
%defattr(-,root,root)
%{_libdir}/erlang/lib/%{realname}-%{version}/src

%changelog
* Thu Sep 07 2010 Timon <timosha@gmail.com> - 2.3.4-1
- initial commit
	
