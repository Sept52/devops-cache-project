Name:           cache-api
Version:        1.0.0
Release:        1%{?dist}
Summary:        Flask proxy with Redis cache
License:        MIT
BuildArch:      noarch
Source0:        %{name}-%{version}.tar.gz

%description
Proxy API: checks Redis, falls back to the Go backend.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/cache-api
mkdir -p %{buildroot}/etc/cache-api
mkdir -p %{buildroot}/usr/lib/systemd/system
install -m 0755 opt/cache-api/cache-api.py %{buildroot}/opt/cache-api/cache-api.py
install -m 0644 etc/cache-api/config.yaml %{buildroot}/etc/cache-api/config.yaml
install -m 0644 usr/lib/systemd/system/cache-api.service %{buildroot}/usr/lib/systemd/system/cache-api.service

%post
systemctl daemon-reload
systemctl enable cache-api.service || true

%files
/opt/cache-api/cache-api.py
/etc/cache-api/config.yaml
/usr/lib/systemd/system/cache-api.service

%changelog
* Sat Nov 14 2026 Danila <danila@example.com> - 1.0.0-1
- Initial package
