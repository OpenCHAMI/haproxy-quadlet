<!--
SPDX-FileCopyrightText: © 2026 OpenCHAMI a Series of LF Projects, LLC

SPDX-License-Identifier: MIT
-->

# haproxy-quadlet

Podman Quadlet packaging for the haproxy edge proxy of an OpenCHAMI deployment. The RPM ships `haproxy.container`, a `10-defaults.conf` drop-in carrying the deployment glue (volumes, published ports, networks), the `haproxy-certs` volume that holds its TLS certificates, and a default `haproxy.cfg` that terminates TLS and routes `/hsm/v2`, `/boot-service/`, `/metadata-service/`, `/tokensmith/`, and `/configurator` to their backing services. Upstream haproxy is pulled from `cgr.dev/chainguard/haproxy`; this package's version tracks the packaging, not haproxy itself.

## Usage

```bash
make rpm-build
sudo dnf install ./dist/rpmbuild/RPMS/noarch/openchami-haproxy-quadlet-*.rpm
sudo systemctl daemon-reload
sudo systemctl start haproxy.service
```

Edit `/etc/openchami/configs/haproxy.cfg` to change routing. For Podman or systemd changes, add a drop-in under `/etc/containers/systemd/haproxy.container.d/` rather than editing the packaged one, then run `systemctl daemon-reload`.

TLS certificates are read from the `haproxy-certs` volume, which `openchami-acme-quadlets` populates; supply your own there if you are not using ACME.
