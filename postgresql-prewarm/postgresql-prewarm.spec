%global 	branch	REL9_2
Name:		postgresql-prewarm
Version:	1
Release:	1%{?dist}
Summary:	preload relation data into system buffer cache

Group:		Applications/Databases
License:	BSD
URL:		https://github.com/Timosha/pg_prewarm/
Source0:	https://github.com/Timosha/pg_prewarm/archive/REL9_2.zip

BuildRequires:	postgresql-devel >= 9.2
Requires:	postgresql-server >= 9.2

%description
preload relation data into system buffer cache

%prep
%setup -qn pg_prewarm-%{branch}

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make USE_PGXS=1 install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/pgsql/
%{_datadir}/pgsql/

%changelog
* Wed Oct 01 2014 Timon <timosha@gmail.com> - 1-1
- New package


