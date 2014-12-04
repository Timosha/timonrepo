Name:      libjxr
Summary:   Client library for manipulate JPEG-XR image files
Version:   1.1
Release:   1%{?dist}
License:   BSD
Group:     System Environment/Libraries
URL:       https://jxrlib.codeplex.com/
Source0:   jxrlib_1_1.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This is an open source implementation of the jpegxr image format standard.

%prep
%setup -qn jxrlib

%build
make %{_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp JxrDecApp JxrEncApp %{buildroot}%{_bindir}

%clean
%{__rm} -rf %{buildroot}

%files
%doc doc/*
%{_bindir}/Jxr*

%changelog
* Thu Dec 04 2014 Timon <timosha@gmail.com> - 1.1-3
- initial build
