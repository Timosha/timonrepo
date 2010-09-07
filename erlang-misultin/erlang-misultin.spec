#%global gitdate 20100605
%global realname misultin

Summary:	An Erlang library for building fast lightweight HTTP(S) servers
Name:		erlang-%{realname}
Version:	0.6.1
Release:	1%{?dist}
Group:		Development/Libraries
License:	BSD
URL:		http://code.google.com/p/misultin/
Source:		http://misultin.googlecode.com/files/%{realname}-%{version}.zip	
BuildRequires:	erlang
Requires:	erlang
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Misultin (pronounced mee-sul-teen) is an Erlang library for building fast 
lightweight HTTP(S) servers, which also supports websockets. 

%package devel
Summary:	Development files for Misultin
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for Misultin

%prep
%setup -q -n %{realname}-%{version}

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
install -D -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -D -m 644 include/misultin.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/src/misultin.hrl

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.txt LICENSE.txt
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin

%files devel
%defattr(-,root,root)
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/src
%{_libdir}/erlang/lib/%{realname}-%{version}/src/misultin.hrl

%changelog
* Thu Sep 07 2010 Timon <timosha@gmail.com> - 0.6.1-1
- new upstream

* Fri Jul 23 2010 Timon <timosha@gmail.com> - 0.6-1
- let's begin



