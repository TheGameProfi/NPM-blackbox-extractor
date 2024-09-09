# NPM-blackbox-extractor
Python Script to extract the active Proxy's from the 'Nginx Proxy Manager' using the Database

This Script exports the Active Proxy's into an blackbox-exporter-target file, and reloads the Prometheus Config via the API.
You need to change the Prometheus URL inside the [exporter.py](https://github.com/TheGameProfi/NPM-blackbox-extractor/blob/main/exporter.py#L11) in Line 11, or set `reload_prom` to `False` in Line 12

You also need to change the Blackbox exporter url/ip in [Line 52](https://github.com/TheGameProfi/NPM-blackbox-extractor/blob/main/exporter.py#L52)

---
```text
___________.__             ________                     __________                _____.__ 
\__    ___/|  |__   ____  /  _____/_____    _____   ____\______   \_______  _____/ ____\__|
  |    |   |  |  \_/ __ \/   \  ___\__  \  /     \_/ __ \|     ___/\_  __ \/  _ \   __\|  |
  |    |   |   Y  \  ___/\    \_\  \/ __ \|  Y Y  \  ___/|    |     |  | \(  <_> )  |  |  |
  |____|   |___|  /\___  >\______  (____  /__|_|  /\___  >____|     |__|   \____/|__|  |__|
                \/     \/        \/     \/      \/     \/
```
