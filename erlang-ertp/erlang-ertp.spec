#%global gitdate 20100605
%global realname ertp

Summary:	Erlang plain RTP library
Name:		erlang-ertp
Version:	0.2.1
Release:	1%{?dist}
Group:		Development/Libraries
License:	GPLv3
URL:		http://github.com/erlyvideo/ertsp
# git clone http://github.com/erlyvideo/ertp.git ertp
# GIT_DIR=ertp/.git git archive --format=tar --prefix=ertp-0.2.1/ v0.2.1 | bzip2 > ertp-0.2.1.tar.bz2
Source:		%{realname}-%{version}.tar.bz2
BuildRequires:	erlang
#BuildRequires:	erlang-erlmedia-devel
#Requires:	erlang-erlmedia
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Erlang plain RTP library

%package devel
Summary:	Development files for ertp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for erlang-ertp.


%prep
%setup -q -n %{realname}-%{version}

%build
%{__make} %{?_smp_mflags}

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
%doc README
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin

%files devel
%defattr(-,root,root)
%{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/src

%changelog
* Thu Sep 07 2010 Timon <timosha@gmail.com> - 0.2.1-1
- initial commit
	
