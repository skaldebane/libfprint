Name:           libfprint-elanmoc2
Version:        1.94.9
Release:        1%{?dist}
Summary:        Toolkit for fingerprint scanner (with elanmoc2 support)

License:        LGPL-2.1-or-later
URL:            https://github.com/skaldebane/libfprint/tree/elanmoc2
Source0:        https://github.com/skaldebane/libfprint/archive/elanmoc2/libfprint-%{version}.tar.gz

# Exclude architectures where fingerprint readers don't exist
ExcludeArch:    s390 s390x

BuildRequires:  meson >= 0.56.0
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  pkgconfig(glib-2.0) >= 2.50
BuildRequires:  pkgconfig(gio-2.0) >= 2.44.0
BuildRequires:  pkgconfig(gusb) >= 0.3.0
BuildRequires:  pkgconfig(nss)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  gtk-doc
BuildRequires:  systemd
BuildRequires:  gobject-introspection-devel
BuildRequires:  python3-cairo
BuildRequires:  python3-gobject
BuildRequires:  cairo-devel
BuildRequires:  umockdev >= 0.13.2
BuildRequires:  valgrind

# We replace the system libfprint
Provides:       libfprint = %{version}-%{release}
Provides:       libfprint-2.so.2()(64bit)
Conflicts:      libfprint

# Ensure fprintd is new enough
Requires:       fprintd >= 1.94

%description
libfprint is a library designed to make it easy for application
developers to add support for consumer fingerprint readers to their
software.

This package contains a fork with the elanmoc2 driver merged, adding
support for ELAN Match-on-Chip fingerprint readers including:
- 04f3:0c00
- 04f3:0c4c
- 04f3:0c5e
- 04f3:0c7c
- 04f3:0c90

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n libfprint-elanmoc2-%{version}

%build
%meson \
    -Ddoc=false \
    -Dgtk-examples=false \
    -Dinstalled-tests=false
%meson_build

%install
%meson_install

# The elanmoc2 driver uses libgusb, so meson doesn't generate udev rules
# for USB devices. Add them manually for proper user access.
cat >> %{buildroot}%{_udevrulesdir}/70-libfprint-2.rules << 'EOF'

# ELAN MoC2 USB fingerprint readers
SUBSYSTEM=="usb", ATTR{idVendor}=="04f3", ATTR{idProduct}=="0c00", TAG+="uaccess"
SUBSYSTEM=="usb", ATTR{idVendor}=="04f3", ATTR{idProduct}=="0c4c", TAG+="uaccess"
SUBSYSTEM=="usb", ATTR{idVendor}=="04f3", ATTR{idProduct}=="0c5e", TAG+="uaccess"
SUBSYSTEM=="usb", ATTR{idVendor}=="04f3", ATTR{idProduct}=="0c7c", TAG+="uaccess"
SUBSYSTEM=="usb", ATTR{idVendor}=="04f3", ATTR{idProduct}=="0c90", TAG+="uaccess"
EOF

# We handle ldconfig via scriptlets below
%ldconfig_scriptlets

%files
%license COPYING
%doc NEWS THANKS AUTHORS README.md
%{_libdir}/libfprint-2.so.2*
%{_libdir}/girepository-1.0/*.typelib
%{_udevhwdbdir}/60-autosuspend-libfprint-2.hwdb
%{_udevrulesdir}/70-libfprint-2.rules
%{_datadir}/metainfo/*.metainfo.xml

%files devel
%doc HACKING.md
%{_includedir}/libfprint-2/
%{_libdir}/libfprint-2.so
%{_libdir}/pkgconfig/libfprint-2.pc
%{_datadir}/gir-1.0/*.gir

%changelog
* Sun Apr 26 2026 skaldebane <user@localhost> - 1.94.9-1
- Initial elanmoc2 COPR build from Depau GitLab fork
- Supports ELAN 0c00/0c4c/0c5e/0c7c/0c90 Match-on-Chip readers
