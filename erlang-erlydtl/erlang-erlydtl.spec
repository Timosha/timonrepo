#%global gitdate 20100605
%global realname erlydtl

Summary:	Erlang implementation of the Django Template Language
Name:		erlang-%{realname}
Version:	0.6.0
Release:	1%{?dist}
Group:		Development/Libraries
License:	MIT
URL:		http://code.google.com/p/erlydtl/
Source:		http://erlydtl.googlecode.com/files/%{realname}-%{version}.tar.gz
BuildRequires:	erlang
Requires:	erlang
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
ErlyDTL is an Erlang implementation of the Django Template Language. 
The erlydtl module compiles Django Template source code into Erlang 
byte-code. The compiled template has a "render" function that takes 
a list of variables and returns a fully rendered document. 

%prep
%setup -q -n %{realname}-%{version}

%build
%{__make} %{?_smp_mflags}

%check
%{__make} test

%install
%{__rm} -rf %{buildroot}
install -D -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README README_I18N
%doc examples
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin


%changelog
* Fri Jul 23 2010 Timon <timosha@gmail.com> - 0.6.0-1
- let's begin
