%define compile_apidox 0
%define _mobile 0
%define _disable_ld_no_undefined 1
%define _disable_lto 1

%define major 16

%define stable %([ `echo %{version} |cut -d. -f3` -ge 70 ] && echo -n un; echo -n stable)

Summary:	Project management application
Name:		calligra-plan
#koffice has epoch 15. We need a higher epoch
Epoch:		16
Version:	3.1.0
Release:	2
Group:		Office
License:	GPLv2+ and LGPLv2+ and GFDL
Url:		https://www.calligra.org/plan/
Source0:	http://download.kde.org/%{stable}/calligra/%{version}/calligraplan-%{version}.tar.xz
Source100:	%{name}.rpmlintrc
## upstream patches
Patch0:		0020-Fix-build-with-Qt-5.11-missing-headers.patch
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5PrintSupport)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5X11Extras)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(KF5AkonadiContact)
BuildRequires:	cmake(KF5Akonadi)
BuildRequires:	cmake(KF5Archive)
BuildRequires:	cmake(KF5Activities)
BuildRequires:	cmake(KF5CalendarCore)
BuildRequires:	cmake(KF5Completion)
BuildRequires:	cmake(KF5ConfigWidgets)
BuildRequires:	cmake(KF5Config)
BuildRequires:	cmake(KF5Contacts)
BuildRequires:	cmake(KF5DBusAddons)
BuildRequires:	cmake(KF5Holidays)
BuildRequires:	cmake(KF5I18n)
BuildRequires:	cmake(KF5IconThemes)
BuildRequires:	cmake(KF5Init)
BuildRequires:	cmake(KF5ItemModels)
BuildRequires:	cmake(KF5ItemViews)
BuildRequires:	cmake(KF5JobWidgets)
BuildRequires:	cmake(KF5KHtml)
BuildRequires:	cmake(KF5KIO)
BuildRequires:	cmake(KF5Notifications)
BuildRequires:	cmake(KF5NotifyConfig)
BuildRequires:	cmake(KF5Parts)
BuildRequires:	cmake(KF5Service)
BuildRequires:	cmake(KF5TextWidgets)
BuildRequires:	cmake(KF5ThreadWeaver)
BuildRequires:	cmake(KF5WidgetsAddons)
BuildRequires:	cmake(KF5WindowSystem)
BuildRequires:	cmake(KF5XmlGui)
BuildRequires:	cmake(KF5KCMUtils)
BuildRequires:	cmake(KF5Activities)
BuildRequires:	cmake(KF5Wallet)
BuildRequires:	cmake(KGantt)
BuildRequires:	cmake(Qt5Test)
BuildRequires:	cmake(Qt5OpenGL)
%if %compile_apidox
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif

%description
Plan is a project management application.

It is intended for managing moderately large projects with multiple resources.

%files -f %{name}.lang
%{_sysconfdir}/xdg/calligraplanrc
%{_sysconfdir}/xdg/calligraplanworkrc
%{_bindir}/calligraplan
%{_bindir}/calligraplanwork
%{_libdir}/libkdeinit5_calligraplan.so
%{_libdir}/libkdeinit5_calligraplanwork.so
%{_libdir}/libkplatokernel.so*
%{_libdir}/libkplatomodels.so*
%{_libdir}/libkplatoui.so*
%{_libdir}/libplankundo2.so*
%{_libdir}/libplanmain.so*
%{_libdir}/libplanodf.so*
%{_libdir}/libplanplugin.so*
%{_libdir}/libplanprivate.so*
%{_libdir}/libplanstore.so*
%{_libdir}/libplanwidgets.so*
%{_libdir}/libplanwidgetutils.so*
%{_libdir}/libplanworkfactory.so*
%{_libdir}/qt5/plugins/calligraplan
%{_libdir}/qt5/plugins/calligraplanworkpart.so
%{_datadir}/applications/org.kde.calligraplan.desktop
%{_datadir}/applications/org.kde.calligraplanwork.desktop
%{_datadir}/calligraplan
%{_datadir}/calligraplanwork
%{_datadir}/config.kcfg/calligraplansettings.kcfg
%{_datadir}/config.kcfg/calligraplanworksettings.kcfg
%{_datadir}/icons/*/*/*/calligraplan.*
%{_datadir}/icons/*/*/*/calligraplanwork.*
%{_datadir}/icons/*/*/*/application-x-vnd.kde.kplato.png
%{_datadir}/icons/*/*/*/application-x-vnd.kde.kplato.svgz
%{_datadir}/icons/*/*/*/application-x-vnd.kde.kplato.work.*
%{_datadir}/icons/*/*/*/application-x-vnd.kde.plan.png
%{_datadir}/icons/*/*/*/application-x-vnd.kde.plan.svgz
%{_datadir}/icons/*/*/*/application-x-vnd.kde.plan.work.*
%{_datadir}/kxmlgui5/calligraplan
%{_datadir}/kxmlgui5/calligraplanwork
/usr/share/metainfo/org.kde.calligraplan.appdata.xml

%prep
%autosetup -n calligraplan-%{version} -p1

%build
%cmake_kde5 \
	-DPACKAGERS_BUILD=ON

%ninja

%if %{compile_apidox}
%ninja apidox
%endif

%install
%ninja_install -C build

%if %compile_apidox
ninja install-apidox DESTDIR=%{buildroot}/
list=`ls -d */ -1`;
echo $list;
for i in $list ; do
    cd $i;
	if grep '^include .*Doxyfile.am' Makefile.am; then
	    echo "installing apidox from $i" ;	
	    make install-apidox DESTDIR=%{buildroot}/ ; 
	fi
    cd ../;
done;
%endif

## unpackaged files
# bogus locale
rm -frv %{buildroot}%{_kde5_datadir}/locale/x-test/
# no need to package lib*.so symlinks
find  %{buildroot}%{_kde5_libdir}/  -maxdepth 1 -name lib*.so -type l -delete

%find_lang %{name} --all-name --with-html
