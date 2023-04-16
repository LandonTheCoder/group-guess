Name:           group-guess
Version:        1.3.1
Release:        1%{?dist}
Summary:        A Family Feud clone
BuildArch:	noarch

License:        MIT
URL:            https://github.com/LandonTheCoder/%{name}/
Source0:        https://github.com/LandonTheCoder/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  python3
BuildRequires:	python3-setuptools
BuildRequires:	python3-rpm-macros
Requires:       python3
Requires:	gtk3
# Check what PyGObject for Python 3 is.
Requires:	python3-gobject
Requires:	gobject-introspection
Requires:	librsvg2
Requires:	glib2

%description


%prep
%setup -q


%build
#%%configure
#make %{?_smp_mflags}
%py3_build


%install
%py3_install
mkdir -vp %{buildroot}/%{_pkgdocdir}/examples
cp -vt %{buildroot}/%{_pkgdocdir}/examples %{buildroot}/%{python3_sitelib}/group_guess/example.json %{buildroot}/%{python3_sitelib}/group_guess/example.py
rm -r %{buildroot}/%{python3_sitelib}/Group_Guess-%{version}-py%{python3_version}.egg-info

%files
%license LICENSE
%dir %{python3_sitelib}/group_guess
%dir %{python3_sitelib}/group_guess/__pycache__/
%{python3_sitelib}/group_guess/__pycache__/*.pyc
%dir %{python3_sitelib}/group_guess/assets
%{python3_sitelib}/group_guess/*.py
%{python3_sitelib}/group_guess/example.json
%{python3_sitelib}/group_guess/assets/*.svg
%{_bindir}/gg-gamesave
%dir %{_pkgdocdir}/examples
%{_pkgdocdir}/examples/example.*
%doc README.md
%doc SAVE-FORMAT.md

%doc


%changelog
* Sun 16 Apr 2023 LandonTheCoder <100165458+LandonTheCoder@users.noreply.github.com> - 1.3.1-1
 - (Attempt to) Introduce Arch PKGBUILD
 - Corrections for RPM packaging
 - Fix alignment/padding of Question label
 - Correct name of command to gg-gamesave in gg-gamesave.1 manpage
 - Use correct, non-Ubuntu-specific icon name for "search" icon
* Fri Jul 5 2022 LandonTheCoder <100165458+LandonTheCoder@users.noreply.github.com> - 1.3.0-2
 - Fix date, so package will build.
* Fri Jul 5 2022 LandonTheCoder <100165458+LandonTheCoder@users.noreply.github.com> - 1.3.0-1
 - First RPM package (tested on Fedora 36) of Group Guess
 - Fixes a bug in code for asset-directory detection
