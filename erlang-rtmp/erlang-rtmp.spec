#%global gitdate 20100605
%global realname rtmp

Summary:	Erlang RTMP library
Name:		erlang-%{realname}
Version:	1.7.7
Release:	1%{?dist}
Group:		Development/Libraries
License:	GPLv3
URL:		http://erlyvideo.org/rtmp/
# git clone http://github.com/erlyvideo/erlang-rtmp.git erlang_rtmp
# GIT_DIR=erlang_rtmp/.git git archive --format=tar --prefix=erlang_rtmp-1.7.7/ v1.7.7 | bzip2 > erlang_rtmp-1.7.7.tar.bz2
Source:		erlang_%{realname}-%{version}.tar.bz2
BuildRequires:	erlang
#BuildRequires:	erlang-erlmedia-devel erlang-ertp-devel
#Requires:	erlang-erlmedia erlang-ertp
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
RTMP stands for Real Time Messaging Protocol. It is a proprietary 
protocol from beloved Adobe, supported by Flash Player from one 
side and by Adobe Flash Media Server from other side. All other 
implementations use non-strictly implemented reverse engineered 
ideas about RTMP.

%package devel
Summary:	Development files for erlang-rtmp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for erlang-rtmp.

%prep
%setup -q -n erlang_%{realname}-%{version}

%build
%{__make} 

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{ebin,src,include}
%{__install} -c -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%{__install} -c -m 644 ebin/*.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
%{__install} -c -m 644 src/* %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/src/
%{__install} -c -m 644 include/* %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/include/
#TODO: rtmp_bench
#TODO: doc


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.md COPYING
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin

%files devel
%defattr(-,root,root)
%{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/src

#TODO files doc

%changelog
* Tue Sep 07 2010 Timon <timosha@gmail.com> - 1.7.7-1
- initial commit
	
