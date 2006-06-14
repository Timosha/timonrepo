%define section		devel
%define upstreamver	8.1-407
%define gcj_support	1

Summary:	JDBC driver for PostgreSQL
Name:		postgresql-jdbc
Version:	8.1.407
Release:	1jpp
Epoch:		0
License:	BSD
Group:		Applications/Databases
URL:		http://jdbc.postgresql.org/

Source0:	http://jdbc.postgresql.org/download/%{name}-%{upstreamver}.src.tar.gz
Patch1:		postgresql-jdbc-unspec-string.patch

%if %{gcj_support}
%else
BuildArch:	noarch
%endif
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  ant >= 0:1.6.2
BuildRequires:  ant-junit >= 0:1.6.2
BuildRequires:  junit >= 0:3.7
BuildRequires:	findutils gettext
%if %{gcj_support}
BuildRequires:	gcc-java
Requires(post): java-1.4.2-gcj-compat
Requires(postun): java-1.4.2-gcj-compat
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-root

Obsoletes: rh-postgresql-jdbc

%description
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-jdbc package includes the .jar files needed for
Java programs to access a PostgreSQL database.

%prep
%setup -c -q
mv -f %{name}-%{upstreamver}.src/* .
rm -f %{name}-%{upstreamver}.src/.cvsignore
rmdir %{name}-%{upstreamver}.src

# remove any binary libs
find -name "*.jar" -or -name "*.class" | xargs rm -f

%patch1 -p1

%build
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=
sh update-translations.sh
ant

%install
rm -rf ${RPM_BUILD_ROOT}

install -d $RPM_BUILD_ROOT%{_javadir}
# Per jpp conventions, jars have version-numbered names and we add
# versionless symlinks.
install -m 644 jars/postgresql.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

pushd $RPM_BUILD_ROOT%{_javadir}
ln -s %{name}-%{version}.jar %{name}.jar
# Also, for backwards compatibility with our old postgresql-jdbc packages,
# add these symlinks.  (Probably only the jdbc3 symlink really makes sense?)
ln -s postgresql-jdbc.jar postgresql-jdbc2.jar
ln -s postgresql-jdbc.jar postgresql-jdbc2ee.jar
ln -s postgresql-jdbc.jar postgresql-jdbc3.jar
popd

%if %{gcj_support}
aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}

%post
/usr/bin/rebuild-gcj-db

%postun
/usr/bin/rebuild-gcj-db

%endif

%files
%defattr(-,root,root)
%doc LICENSE README doc/* example
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*.jar.so
%{_libdir}/gcj/%{name}/*.jar.db
%endif

%changelog
* Wed Jun 14 2006 Tom Lane <tgl@redhat.com> 8.1.407-1jpp
- Update to build 8.1-407

* Mon Mar 27 2006 Tom Lane <tgl@redhat.com> 8.1.405-2jpp
- Back-patch upstream fix to support unspecified-type strings.

* Thu Feb 16 2006 Tom Lane <tgl@redhat.com> 8.1.405-1jpp
- Split postgresql-jdbc into its own SRPM (at last).
- Build it from source.  Add support for gcj compilation.
