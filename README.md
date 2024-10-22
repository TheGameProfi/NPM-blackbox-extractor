# NPM-blackbox-extractor
Python Script to extract the active Proxies from the 'Nginx Proxy Manager' using the Database

This Script exports the Active Proxies into an blackbox-exporter-target file, and can reloads the Prometheus Config via the API.

## Configuration
For Examples of Compose Files see [examples/](examples/)

### Prometheus
Default it takes the `host.docker.internal:9090`, for that you would need to pass through the docker host:
```bash
# Docker run
docker run -it --add-host=host.docker.internal:host-gateway ...
```
```yml
# Docker Compose
services:
  extra_hosts:
    - "host.docker.internal:host-gateway"
  ...
```
If you have a different Url or behind a Proxy you can change the PrometheusUrl via the Environment Var `prometheusUrl` (with http/https and if the subpath).
Or if you don't want the Prometheus to be reloaded you can deactivate it by passing the environment Var `reloadProm=False`

For running the Exporter without docker you can either pass the Envs or change it in the [exporter.py](exporter.py#L12)

### Blackbox
Default the Extractor is using `blackbox:9115` as blackboxUrl to change it pass the env Var `blackboxUrl` without http/https (https not tested).
Or when running locally you can change it in [Line 15](exporter.py#L15)

---
```text
___________.__             ________                     __________                _____.__ 
\__    ___/|  |__   ____  /  _____/_____    _____   ____\______   \_______  _____/ ____\__|
  |    |   |  |  \_/ __ \/   \  ___\__  \  /     \_/ __ \|     ___/\_  __ \/  _ \   __\|  |
  |    |   |   Y  \  ___/\    \_\  \/ __ \|  Y Y  \  ___/|    |     |  | \(  <_> )  |  |  |
  |____|   |___|  /\___  >\______  (____  /__|_|  /\___  >____|     |__|   \____/|__|  |__|
                \/     \/        \/     \/      \/     \/
```
