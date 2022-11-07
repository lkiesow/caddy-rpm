%define debug_package %{nil}

%define  uid   caddy
%define  gid   caddy

Name:          caddy
Summary:       Fast and extensible multi-platform HTTP/1-2-3 web server with automatic HTTPS
Version:       2.6.2
Release:       1%{?dist}
License:       ASL 2.0

Source0:       https://github.com/caddyserver/caddy/releases/download/v%{version}/caddy_%{version}_linux_amd64.tar.gz
Source1:       https://raw.githubusercontent.com/caddyserver/dist/v%{version}/init/caddy.service
Source2:       https://raw.githubusercontent.com/caddyserver/dist/v%{version}/init/caddy-api.service
Source3:       https://raw.githubusercontent.com/lkiesow/caddy-rpm/main/Caddyfile
URL:           https://caddyserver.com

BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd


%description
Caddy simplifies your infrastructure. It takes care of TLS certificate
renewals, OCSP stapling, static file serving, reverse proxying, Kubernetes
ingress, and more.

Its modular architecture means you can do more with a single, static binary
that compiles for any platform.

Caddy runs great in containers because it has no dependencies—not even libc.
Run Caddy practically anywhere.


%prep
%setup -q -c %{name}-%{version}

%build

%install
rm -rf %{buildroot}

install -p -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}/
install -p -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}/

# install binary
install -p -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

# install unit file2
install -p -D -m 0644 \
   %{SOURCE1} \
   %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0644 \
   %{SOURCE2} \
   %{buildroot}%{_unitdir}/%{name}-api.service

# install configuration
install -p -D -m 0644 \
   %{SOURCE3} \
   %{buildroot}%{_sysconfdir}/%{name}/Caddyfile


%clean
rm -rf %{buildroot}


%pre
# Create user and group if nonexistent
# Try using a common numeric uid/gid if possible
if [ ! $(getent group %{gid}) ]; then
	groupadd -r %{gid} > /dev/null 2>&1 || :
fi
if [ ! $(getent passwd %{uid}) ]; then
	useradd -M -r -d %{_sharedstatedir}/%{name} -g %{gid} %{uid} > /dev/null 2>&1 || :
fi


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun_with_restart %{name}.service


%files
%defattr(-,root,root,-)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}
%{_unitdir}/*
%attr(755,%{uid},%{gid}) %dir %{_sharedstatedir}/%{name}
%doc README.md
%license LICENSE


%changelog
* Mon Nov 07 2022 Lars Kiesow <lkiesow@uos.de> - 2.6.2-1
- Fix user home directory

* Sun Nov 06 2022 Lars Kiesow <lkiesow@uos.de> - 2.6.2-0
- Initial build
