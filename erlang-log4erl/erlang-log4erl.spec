#%global gitdate 20100605
%global realname log4erl

Summary:	A logger for erlang in the spirit of Log4J
Name:		erlang-%{realname}
Version:	0.9.0
Release:	3%{?dist}
Group:		Development/Libraries
License:	MPL
URL:		http://code.google.com/p/log4erl/
Source:		http://log4erl.googlecode.com/files/%{realname}-%{version}.tar.gz
BuildRequires:	erlang
Requires:	erlang
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
A logger for erlang in the spirit of Log4J. Features:
- multiple logs
- Currently, only size-based log rotation of files for file appender
- Support default logger if no logger specified
- 5 predifined log levels (debug, info, warn, error, fatal)
- A log handler for error_logger
- Support for user-specified log levels
- Support for a log formatter (similar to Layouts in Log4J)
- Support for console log
- Support for smtp formatter
- Support for XML logs
- Support for syslog 
- Support for changing format and level of appender during run-time

%package devel
Summary:	Development files for log4erl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for log4erl

%prep
%setup -q -n %{realname}-%{version}

%build
%{__make}

%install
%{__rm} -rf %{buildroot}
install -D -m 644 ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -m 644 ebin/*.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -D -m 644 include/log4erl.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/src/log4erl.hrl

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.txt LICENSE.txt CONFIGURATION.txt CHANGELOG.txt TODO.txt
%doc API.txt Appenders_API.txt
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin

%files devel
%defattr(-,root,root)
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/src
%{_libdir}/erlang/lib/%{realname}-%{version}/src/log4erl.hrl

%changelog
* Mon Sep 06 2010 Timon <timosha@gmail.com> - 0.9.0-3
- Licence fix

* Fri Jul 23 2010 Timon <timosha@gmail.com> - 0.9.0-2
- let's begin



