#
# Conditional build:
%bcond_without	caja	# shares extension for Caja (MATE file manager)
#
Summary:	MATE System Tools
Summary(pl.UTF-8):	Narzędzia systemowe dla środowiska MATE
Name:		mate-system-tools
Version:	1.8.1
Release:	3
License:	GPL v2+ (programs), FDL v1.1+ (documentation)
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	7683f392868f78c5dc38f2fd7f2bfb68
URL:		http://mate-desktop.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.9
%{?with_caja:BuildRequires:	caja-devel >= 1.1.0}
BuildRequires:	dbus-devel >= 0.32
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.10.40
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gtk+2-devel >= 2:2.20.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libiw-devel
BuildRequires:	liboobs-devel >= 1.1.0
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	mate-common
BuildRequires:	mate-polkit-devel >= 0.92
BuildRequires:	pango-devel
BuildRequires:	pkgconfig >= 1:0.19
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	system-tools-backends-devel >= 2.10.1
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	dbus >= 0.32
Requires:	glib2 >= 1:2.26.0
Requires:	gtk+2 >= 2:2.20.0
Requires:	liboobs >= 1.1.0
Requires:	mate-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE System Tools are intended to simplify the tasks of configuring a
Unix system for workstations (not servers). This package is a fork of
GNOME System Tools package.

%description -l pl.UTF-8
MATE System Tools to narzędzia systemowe mające na celu uproszczenie
konfigurownia systemów uniksowych dla stacji roboczych (nie serwerów).
Ten pakiet jest odgałęzieniem pakietu GNOME System Tools.

%package devel
Summary:	Development files for MATE System Tools
Summary(pl.UTF-8):	Pliki programistyczne dla narzędzi systemowych MATE
Group:		Development/Libraries
# doesn't require base; the only file is pkg-config specific, so let's require it
Requires:	pkgconfig

%description devel
This package contains files needed for MATE System Tools related
development.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki potrzebne przy programowaniu związanym z
MATE System Tools (narzędziami systemowymi MATE).

%package -n caja-extension-shares
Summary:	Shares configuration extension for Caja (MATE file manager)
Summary(pl.UTF-8):	Rozszerzenie do konfiguracji udziałów dla zarządcy plików Caja
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	caja >= 1.1.0
Obsoletes:	mate-file-manager-extension-shares

%description -n caja-extension-shares
Shares configuration extension for Caja (MATE file manager)

%description -n caja-extension-shares -l pl.UTF-8
Rozszerzenie do konfiguracji udziałów dla zarządcy plików Caja.

%prep
%setup -q

%build
%{__libtoolize}
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_caja:--disable-caja} \
	--disable-silent-rules \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/caja/extensions-2.0/*.la

# fixup .pc file (wrong Name, unprocessed dir names)
%{__sed} -i -e '/^Name:/s/gst/mate-system-tools/' \
	-e 's,@pixmapsdir@,%{_datadir}/%{name}/pixmaps,' \
	-e 's,@scriptsdir@,%{_datadir}/%{name}/ui,' \
	mate-system-tools.pc

# mate-system-tools gettext domain, 5 separate mate dirs
%find_lang %{name} --with-mate --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache mate
%glib_compile_schemas

%postun
%update_icon_cache mate
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/mate-network-admin
%attr(755,root,root) %{_bindir}/mate-services-admin
%attr(755,root,root) %{_bindir}/mate-shares-admin
%attr(755,root,root) %{_bindir}/mate-time-admin
%attr(755,root,root) %{_bindir}/mate-users-admin
%dir %{_sysconfdir}/mate-system-tools
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mate-system-tools/user-profiles.conf
%{_datadir}/glib-2.0/schemas/org.mate.system-tools.gschema.xml
%{_datadir}/mate-system-tools
%{_desktopdir}/mate-network.desktop
%{_desktopdir}/mate-services.desktop
%{_desktopdir}/mate-shares.desktop
%{_desktopdir}/mate-time.desktop
%{_desktopdir}/mate-users.desktop
%{_iconsdir}/mate/*/apps/time-admin.*
%{_iconsdir}/mate/48x48/devices/irda.png
%{_iconsdir}/mate/48x48/devices/plip.png

%files devel
%defattr(644,root,root,755)
%{_pkgconfigdir}/mate-system-tools.pc

%if %{with caja}
%files -n caja-extension-shares
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/caja/extensions-2.0/libcaja-gst-shares.so
%endif
