Summary:	MATE text editor
Name:		mate-text-editor
Version:	1.6.2
Release:	1
License:	GPL v2
Group:		X11/Applications/Editors
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	518869ea16bafd951dac0ab3947c99af
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	enchant-devel
BuildRequires:	gettext-devel
BuildRequires:	mate-doc-utils
BuildRequires:	gtk+-devel
BuildRequires:	gtk-doc
BuildRequires:	gtksourceview2-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkg-config
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	rarian
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
Pluma is a small but powerful text editor for GTK+ and/or MATE. It
includes such features as split-screen mode, a plugin API, which
allows gedit to be extended to support many features while remaining
small at its core, multiple document editing and many more functions.

%package devel
Summary:	gedit header files
Group:		X11/Development/Libraries
# don't require base

%description devel
gedit header files

%package apidocs
Summary:	gedit API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
gedit API documentation.

%prep
%setup -q

# kill mate common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'			\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__libtoolize}
%{__gtkdocize}
%{__intltoolize}
mate-doc-prepare --copy
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-python		\
	--disable-schemas-compile	\
	--disable-scrollkeeper		\
	--disable-silent-rules		\
	--with-html-dir=%{_gtkdocdir}
	#--with-omf-dir=%{_omf_dest_dir}/%{name}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/pluma/*/*.la
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/pluma.convert
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,crh,en@shaw,la}

%find_lang mate-text-editor --with-mate --with-omf --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post
%update_desktop_database
%update_gsettings_cache

%postun
%scrollkeeper_update_postun
%update_desktop_database
%update_gsettings_cache

%files -f mate-text-editor.lang
%defattr(644,root,root,755)
%doc README ChangeLog AUTHORS

# dirs
%dir %{_libdir}/pluma
%dir %{_libdir}/pluma/plugins
%dir %{_libdir}/pluma/plugin-loaders

%attr(755,root,root) %{_bindir}/mate-text-editor
%attr(755,root,root) %{_bindir}/pluma
%attr(755,root,root) %{_libdir}/pluma/plugins/*.so
%attr(755,root,root) %{_libdir}/pluma/plugin-loaders/libcloader.so
%{_libdir}/pluma/plugins/*.pluma-plugin

%{_datadir}/pluma
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml

%{_desktopdir}/pluma.desktop
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/pluma
%{_pkgconfigdir}/pluma.pc

%if 0
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/pluma
%endif

