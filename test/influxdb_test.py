import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "<my-bucket>"
org = "<my-org>"
token = "<my-token>"

client = influxdb_client.InfluxDBClient(
    url="https://eu-central-1-1.aws.cloud2.influxdata.com",
    token=token,
    org=org
)

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)
write_api.write(bucket=bucket, org=org, record=p)