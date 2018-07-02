%define major 3
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Name:           pythonqt
Version:        3.2
Release:        1
Summary:        Lightweight script binding of the Qt framework to the Python language
License:        LGPLv2+
URL:            http://pythonqt.sourceforge.net
Source0:        https://downloads.sourceforge.net/pythonqt/PythonQt%{version}.zip
# Patch in the "make install" command
Patch0:         %{name}-add-install-target.diff
Patch1:         %{name}-fix-format-security.diff
BuildRequires:  qmake5
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(python3)

%package -n %{libname}
Summary:        Lightweight script binding of the Qt framework to the Python language
Group:          Development/Python

%description -n %{libname}
PythonQt is a dynamic and lightweight script binding of the Qt framework
to the Python language. It can be easily embedded into Qt applications and
makes any QObject derived object scriptable via Python without the need of
wrapper code generation.

%package -n %{devname}
Summary:        Lightweight script binding of the Qt framework to the Python language
Group:          Development/Python
Requires:       %{libname}= %{EVRD}

%description -n %{dename}
Header files and development libraries for pythonqt package. PythonQt
is a dynamic and lightweight script binding of the Qt framework
to the Python language.

%prep
%autosetup -p1
sed -r -i -e "s/(unix:PYTHON_VERSION=).*/\1%{python3_version}/g" build/python.prf

# Fix README end-of-line encoding
sed -i 's/\r//' README

%build
# Out-of-tree builds are broken, it assumes lib to be built in-tree (-Lxxx)
# /usr/bin/ld: cannot find -lPythonQt
%qmake_qt5 \
  "LIB_INSTALL=%{buildroot}%{_libdir}"                 \
  "HEADER_INSTALL=%{buildroot}%{_includedir}/PythonQt" \
  %{nil}
%make_build

%install
%make_install

%files -n %{libname}
%{_libdir}/libPythonQt-Qt5-Python*.so.%{major}*
%{_libdir}/libPythonQt_QtAll-Qt5-Python*.so.%{major}*

%files -n %{devname}
%license COPYING
%doc README
%{_includedir}/PythonQt/
%{_libdir}/libPythonQt-Qt5-Python*.so
%{_libdir}/libPythonQt_QtAll-Qt5-Python*.so
