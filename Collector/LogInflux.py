from influxdb import InfluxDBClient
import datetime

try:
    clientInflux = InfluxDBClient('localhost', 8086, 'xx', 'xx@123', 'historiador')
except :
    print "Erro ao canectar-se com o influxdb"


def influx_log(msg):
    datetimeAux = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    json_erro = [
        {
            "measurement": "log",
            "time": datetimeAux,
            "fields": {
                "msg": str(msg)
            }
        }
    ]
    try:
        clientInflux.write_points(json_erro)
    except:
        print "Erro ao gravar logs no influxdb"

def influx_plc(status):
    datetimeAux = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    json_erro = [
        {
            "measurement": "system",
            "time": datetimeAux,
            "fields": {
                "status": int(status)
            }
        }
    ]
    try:
        clientInflux.write_points(json_erro)
    except:
        print "Erro ao gravar logs no influxdb"


