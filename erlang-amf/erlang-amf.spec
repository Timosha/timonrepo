%global realname amf

Summary:	Erlang Action Message Format Library
Name:		erlang-%{realname}
Version:	1.0.1
Release:	1%{?dist}
Group:		Development/Libraries
License:	GPLv2
URL:		http://github.com/erlyvideo/erlang-amf
# git clone http://github.com/erlyvideo/erlang-amf.git erlang_amf
# GIT_DIR=erlang_amf/.git git archive --format=tar --prefix=erlang_amf-1.0.1/ 98217e3b53b2cc0f32b8 | bzip2 > erlang_amf-1.0.1.tar.bz2
Source:		erlang_amf-%{version}.tar.bz2
BuildRequires:	erlang
Requires:	erlang
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Action Message Format (AMF) is a compact binary format that is used to
serialize ActionScript object graphs. Once serialized an AMF encoded object
graph may be used to persist and retrieve the public state of an application
across sessions or allow two endpoints to communicate through the exchange
of strongly typed data.

%package devel
Summary:	Development files for Erlang-AMF
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for Erlang-AMF interface.

%prep
%setup -q -n erlang_amf-%{version}

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

#TODO: remove amf0_tests.beam amf3_tests.beam
#%{__install} -D -m 644 src/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
#%{__install} -m 644 src/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING README ChangeLog AUTHORS
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%{_libdir}/erlang/lib/%{realname}-%{version}/doc
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin



%files devel
%defattr(-,root,root)
%{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/src


%changelog
* Mon Sep 06 2010 Timon <timosha@gmail.com> - 1.0.1-1
- latest upstream version

* Fri Jul 23 2010 Timon <timosha@gmail.com> - 1.0.1-0.1.20100605git
- let's begin



