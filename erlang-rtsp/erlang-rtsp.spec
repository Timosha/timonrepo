#%global gitdate 20100605
%global realname rtsp

Summary:	Erlang RTSP/SDP/RTP support library
Name:		erlang-%{realname}
Version:	1.6.2
Release:	1%{?dist}
Group:		Development/Libraries
License:	GPLv3
URL:		http://github.com/erlyvideo/ertsp
# git clone http://github.com/erlyvideo/ertsp.git ertsp
# GIT_DIR=ertsp/.git git archive --format=tar --prefix=ertsp-1.6.2/ v1.6.2 | bzip2 > ertsp-1.6.2.tar.bz2
Source:		ertsp-%{version}.tar.bz2
BuildRequires:	erlang
BuildRequires:	erlang-erlmedia-devel erlang-ertp-devel
Requires:	erlang-erlmedia erlang-ertp
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
erlang-ertsp is a library, extracted from Erlyvideo. 
It handles RTSP and RTP protocols.

%package devel
Summary:	Development files for erlang-rtsp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for erlang-rtsp.

%prep
%setup -q -n ertsp-%{version}

%build
%{__make} 

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,src,include}
%{__install} -c -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%{__install} -c -m 644 ebin/*.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%{__install} -c -m 644 src/* %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/src/
%{__install} -c -m 644 include/* %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin

%files devel
%defattr(-,root,root)
%{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/src

#TODO files doc

%changelog
* Mon Sep 06 2010 Timon <timosha@gmail.com> - 1.6.2-1
- new upstream release
	
