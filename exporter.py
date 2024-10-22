import sqlite3
import json
import yaml
import time
import ast
import requests
import os

# Path to your SQLite database file
DB_FILE = '/app/data/database.sqlite'

url = os.environ.get("prometheusUrl", "http://host.docker.internal:9090/-/reload")
reload_prom = os.environ.get("reloadProm", True)

blackboxUrl = os.environ.get("blackboxUrl", "blackbox:9115")

# Path to save JSON file
JSON_FILE = '/app/save/proxy_hosts.json'

def prometheus_config_exporter(targets):

    static_config = []

    for target in targets:
        static_config.append({
            "targets": [f'http://{target[1]}:{target[2]}'],
            "labels": {
                "remoteUrl": target[0],
                "localUrl": f'{target[1]}:{target[2]}',
                "service": target[3],
                "domain": target[4],
            },
        },)

    config = {
        "scrape_configs": [
            {
                "job_name": "blackbox",
                "metrics_path": "/probe",
                "params": {
                    "module": ["http_2xx"]
                },
                "static_configs": static_config,
                "relabel_configs": [
                    {
                        "source_labels": ["__address__"],
                        "target_label": "__param_target",
                    },
                    {
                        "source_labels": ['__param_target'],
                        "target_label": "instance",
                    },
                    {
                        "target_label": "__address__",
                        "replacement": blackboxUrl,
                    }
                ],
            },
        ],
    }

    new_config = yaml.dump(config, default_flow_style=False)

    existing_config = []

    with open('/app/save/prometheus.yml', 'r') as f:
        existing_config = yaml.safe_load(f)

    if existing_config == config:
        print(f"{time.ctime()}: Prometheus configuration file is up-to-date.")
        return

    with open('/app/save/prometheus.yml', 'w') as f:
        f.write(new_config)

    print(f"{time.ctime()}: Prometheus configuration file has been updated.")

    if reload_prom:
	    print(f"{time.ctime()}: Reloading Prometheus configuration.")
	
	    response = requests.post(url)
	    print(response.status_code)
	    print(response.text)
	    print(f"{time.ctime()}: Prometheus configuration has been reloaded.")


def export_proxy_hosts():
    while True:
        try:
            # Connect to SQLite database
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            # Query to fetch proxy hosts information
            query = """
                SELECT domain_names, forward_host, forward_port 
                FROM proxy_host 
                WHERE is_deleted == 0 AND enabled == 1;
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Close database connection
            conn.close()
            targets = []

            # Convert rows to JSON format
            proxy_hosts = []
            for row in rows:
                domains = ast.literal_eval(row[0])
                ending = str(row[2])
                for endpoint in domains:
                    mainDomain = domains[0].split('.')
                    if len(mainDomain) == 2:
                        service = 'LandingPage'
                        domain = f'{mainDomain[0]}.{mainDomain[1]}'
                    else:
                        service = mainDomain[0]
                        domain = f'{mainDomain[1]}.{mainDomain[2]}'

                    targets.append([endpoint, row[1], ending, service, domain])

                # Perpare host.json File
                domain_names = row[0]  # Assuming first domain is the primary one
                upstreamaddr = row[1]
                port = row[2]
                proxy_hosts.append({
                    "remote-url": domain_names,
                    "upstreamaddr": upstreamaddr,
		    "port": port
                })

            # Write Prometheus configuration to file
            prometheus_config_exporter(targets)

            # Write JSON data to file
            with open(JSON_FILE, 'w') as f:
                json.dump(proxy_hosts, f, indent=2)

            print(f"{time.ctime()}: JSON file has been updated.")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(600)  # Sleep for 600 seconds (10 minutes)

if __name__ == '__main__':
    export_proxy_hosts()
