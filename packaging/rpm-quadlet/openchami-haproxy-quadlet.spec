# SPDX-FileCopyrightText: 2026 OpenCHAMI Contributors
# SPDX-License-Identifier: MIT
#
# See `make rpm-build` for the tag-to-version mapping. The packaged image is
# upstream haproxy, so its tag is pinned in the quadlet file itself rather
# than derived from this package's version.

Name:           openchami-haproxy-quadlet
Version:        %{version}
Release:        %{rel}%{?dist}
Summary:        OpenCHAMI haproxy Quadlet units

License:        MIT
URL:            https://github.com/OpenCHAMI/haproxy-quadlet
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

Requires(post,preun,postun):  systemd

# podman 5.0.0 is the first release whose Quadlet generator enables
# systemd-style *.container.d drop-in directories
Requires:                     podman >= 5.0.0

# NOTE: openchami-acme-quadlets populates the haproxy-certs volume that
# terminates TLS, but a site may install its own certificates there instead.
Suggests:                     openchami-acme-quadlets >= 0.0.1
Suggests:                     boot-service-quadlet >= 0.3.2
Suggests:                     metadata-service-quadlet >= 0.2.2
Suggests:                     smd-quadlet >= 2.20.5
Suggests:                     tokensmith-quadlet >= 0.4.1

%description
Podman Quadlet unit files (container + volume) for running haproxy as the
edge proxy of an OpenCHAMI deployment.

%prep
%setup -q

%install

# systemd files
install -d %{buildroot}/usr/share/containers/systemd
install -m 644 haproxy.container %{buildroot}/usr/share/containers/systemd/
install -d %{buildroot}/usr/share/containers/systemd/haproxy.container.d
install -m 644 haproxy.container.d/10-defaults.conf \
    %{buildroot}/usr/share/containers/systemd/haproxy.container.d/

install -m 644 haproxy-certs.volume \
    %{buildroot}/usr/share/containers/systemd/haproxy-certs.volume

# configuration files
install -d %{buildroot}/etc/openchami/configs
install -m 644 haproxy.cfg %{buildroot}/etc/openchami/configs/

%files
%license LICENSES/MIT.txt
%dir /etc/openchami
%dir /etc/openchami/configs
%config(noreplace) /etc/openchami/configs/haproxy.cfg
/usr/share/containers/systemd/haproxy.container
/usr/share/containers/systemd/haproxy.container.d
/usr/share/containers/systemd/haproxy.container.d/10-defaults.conf
/usr/share/containers/systemd/haproxy-certs.volume

%post
# reload systemd so the new Quadlet-generated unit is seen
systemctl daemon-reload || :
if [ $1 -ge 2 ]; then
    systemctl try-restart haproxy.service || :
fi

%preun
if [ $1 -eq 0 ]; then
    systemctl stop haproxy.service >/dev/null 2>&1 || :
fi

%postun
# reload systemd so the removed unit is dropped
systemctl daemon-reload || :
