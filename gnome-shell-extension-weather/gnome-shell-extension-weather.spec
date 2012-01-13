%global git 7b9d2ed
#%global uuid weather@simon04
%global uuid weather@gnome-shell-extensions.gnome.org
%global github simon04-gnome-shell-extension-weather

Name:           gnome-shell-extension-weather
Version:        0
Release:        0.3.git%{git}%{?dist}
Summary:        A gnome-shell extension to show current weather and forecast

Group:          User Interface/Desktops
License:        GPLv3+
URL:            https://github.com/simon04/gnome-shell-extension-weather
Source0:        https://github.com/simon04/gnome-shell-extension-weather/tarball/master/%{github}-%{git}.tar.gz
BuildArch:      noarch

Requires:       gnome-shell >= 3.2.0
BuildRequires:  gnome-common intltool glib2-devel


%description
Gnome Shell Extensions that adds an applet on the panel which reveals
current weather and forecast.

%prep
%setup -q -n %{github}-%{git}

%build
./autogen.sh --prefix=%{_prefix} 
%{__make}
# Nothing to build

%install
%{__rm} -rf %{buildroot}
#%{__make} install
make DESTDIR=%{buildroot} install
%{__install} -Dp -m 0755 weather-extension-configurator.py %{buildroot}%{_bindir}/weather-extension-configurator
%find_lang %{name}

#mkdir -p %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}
#install -Dp -m 0644 src/{extension.js,metadata.json,stylesheet.css,org.gnome.shell.extensions.weather.gschema.xml} \
#  %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}/

%postun
if [ $1 -eq 0 ] ; then
	glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README.md
%{_datadir}/gnome-shell/extensions/%{uuid}/
%{_datadir}/glib-2.0/schemas/org.gnome.shell.extensions.weather.gschema.xml
%{_bindir}/weather-extension-configurator

%changelog
* Thu Dec 12 2011 Timon <timosha@gmail.com> 0-0.3.git7b9d2ed
- configurator
- Some updates from git

* Thu Dec 12 2011 Timon <timosha@gmail.com> 0-0.2.git2a8a9eb
- Some updates from git

* Thu Nov 03 2011 Timon <timosha@gmail.com> 0-0.1.git9b55721
- Initial package for Fedora
- Using spec from Fabian Affolter as a template

