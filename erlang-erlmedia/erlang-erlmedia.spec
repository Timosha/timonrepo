%global realname erlmedia

Summary:	Formats support for erlyvideo
Name:		erlang-%{realname}
Version:	1.8.3
Release:	1%{?dist}
Group:		Development/Libraries
License:	GPLv3
URL:		http://github.com/erlyvideo/erlmedia
# git clone http://github.com/erlyvideo/erlmedia.git erlmedia
# GIT_DIR=erlmedia/.git git archive --format=tar --prefix=erlmedia-1.8.3/  81d7d2f3bf03a7ff3df5 | bzip2 > erlmedia-1.8.3.tar.bz2
Source:		erlmedia-%{version}.tar.bz2
BuildRequires:	erlang
Requires:	erlang
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Erlmedia is a format library, extracted from Erlyvideo. It doesn't and 
never will decode anything or encode, because erlang isn't suited for 
such things. Use libavcodec for it.

%package devel
Summary:	Development files for erlmedia
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for erlang erlmedia.

%prep
%setup -q -n %{realname}-%{version}

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTROOT=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING README.md doc/EPLICENSE.txt
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
#%{_libdir}/erlang/lib/%{realname}-%{version}/doc
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin

%files devel
%defattr(-,root,root)
%{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/src

%changelog
* Mon Sep 06 2010 Timon <timosha@gmail.com> - 1.8.2-1
- Initial commit

