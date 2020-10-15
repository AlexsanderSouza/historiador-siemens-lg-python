from influxdb import InfluxDBClient
import time
import datetime
import snap
import clx_comm
import sys
import os


# Reinicia pragrama
def restart_program(d):
    print "Reiniciando"
    json_erro = [
        {
            "measurement": "log",
            "time": d,
            "fields": {
                "msg": str("Programa reiniciado automaticamente")
            }
        }
    ]
    try:
        clientInflux.write_points(json_erro)
    except:
        print "Erro ao gravar logs no influxdb"
    python = sys.executable
    os.execl(python, python, * sys.argv)


# Configuracao do Collector
ipSiemens = '192.168.0.1'
dbSiemens = 1000
ipClx = "192.168.1.20"
slotClx = 0
ipInfludb ="localhost"
portInfluxdb = 8086
userInflux ="xx"
passwordInflux = "xx@123"
bdInflux ="historiador"
#Variaveis iniciais
errorRockwell = 0
errorSiemens = 0
cont = 0 
tempo = 1 #Tempo de gravacao em segundos, para temperatura -> tempo = tempo*15 
try:
    clientInflux = InfluxDBClient(ipInfludb, portInfluxdb, userInflux, passwordInflux, bdInflux)
except :
    print "Erro ao canectar-se com o influxdb"
print "Running"
while (True):
    # Tempo de gravacao e leitura dos dados siemens
    time.sleep(tempo)
    cont = cont + 1
    # Obtem a data e hora do momento da gravacao dos dados
    datetimeAux = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    # Obtem dados do PLC Siemens
    try :
        snap.read_siemens(str(ipSiemens), int(dbSiemens))
    except :
        snap.temp = ["ERRO"]
    # Em caso de 15 erros seguidos reiniciar programa
    if snap.temp[0] == "ERRO":
        errorSiemens = errorSiemens + 1
        if errorSiemens == 3 :
            restart_program(datetimeAux)
    if snap.temp[0] != "ERRO" :
        errorSiemens = 0
        json_pressureS = [
            {
                "measurement": "pressureS",
                "time": datetimeAux,
                "fields": {
                    "pressure_001": float(snap.temp[8]),
                    "pressure_002": float(snap.temp[9]),
                    "pressure_003": float(snap.temp[18]),
                    "pressure_004": float(snap.temp[19])
                }
            }
        ]
        try:
            clientInflux.write_points(json_pressureS)
        except:
            print("Erro ao gravar no Banco de dados")
    # Em 15 segundos grava temperatura no banco
    # print cont
    if cont == 15 :
        cont = 0
        # Obtem dados do PLC Rockwell
        rockwell = clx_comm.read_tag(str(ipClx), int(slotClx),"Secador_1.DB_Historian", 50)
        rockwell2 = clx_comm.read_tag(str(ipClx), int(slotClx),"Secador_2.DB_Historian", 50)
        # Em caso de 5 erros seguidos reiniciar programa
        if rockwell[0] == "ERRO":
            errorRockwell = errorRockwell + 1
            if errorRockwell == 3 :
                restart_program(datetimeAux)
        if rockwell[0] != "ERRO":
            errorRockwell = 0
            json_temperatureR = [
                {
                    "measurement": "temperatureR",
                    "time": datetimeAux,
                    "fields": {
                        "temp_001": float(round(rockwell[0][1],3)),
                        "temp_002": float(round(rockwell[1][1],3)),
                        "temp_003": float(round(rockwell[2][1],3)),
                        "temp_004": float(round(rockwell[3][1],3)),
                        "temp_005": float(round(rockwell[4][1],3)),
                        "temp_006": float(round(rockwell[5][1],3)),
                        "temp_007": float(round(rockwell[6][1],3)),
                        "temp_008": float(round(rockwell[7][1],3)),
                        "temp_009": float(round(rockwell[8][1],3)),
                        "temp_010": float(round(rockwell[9][1],3)),
                        "temp_011": float(round(rockwell[10][1],3)),
                        "temp_012": float(round(rockwell[11][1],3)),
                        "temp_013": float(round(rockwell[12][1],3)),
                        "temp_014": float(round(rockwell[13][1],3)),
                        "temp_015": float(round(rockwell[14][1],3)),
                        "temp_016": float(round(rockwell[15][1],3)),
                        "temp_017": float(round(rockwell2[0][1],3)),
                        "temp_018": float(round(rockwell2[1][1],3)),
                        "temp_019": float(round(rockwell2[2][1],3)),
                        "temp_020": float(round(rockwell2[3][1],3)),
                        "temp_021": float(round(rockwell2[4][1],3)),
                        "temp_022": float(round(rockwell2[5][1],3)),
                        "temp_023": float(round(rockwell2[6][1],3)),
                        "temp_024": float(round(rockwell2[7][1],3)),
                        "temp_025": float(round(rockwell2[8][1],3)),
                        "temp_026": float(round(rockwell2[9][1],3)),
                        "temp_027": float(round(rockwell2[10][1],3)),
                        "temp_028": float(round(rockwell2[11][1],3)),
                        "temp_029": float(round(rockwell2[12][1],3)),
                        "temp_030": float(round(rockwell2[13][1],3)),
                        "temp_031": float(round(rockwell2[14][1],3)),
                        "temp_032": float(round(rockwell2[15][1],3))
                    }
                }
            ] 
            try:
                clientInflux.write_points(json_temperatureR)
            except:
                print("Erro ao gravar no Banco de dados")
        if snap.temp[0] != "ERRO" :
            json_temperatureS = [
                {
                    "measurement": "temperatureS",
                    "time": datetimeAux,
                    "fields": {
                        "temp_001": float(snap.temp[0]),
                        "temp_002": float(snap.temp[1]),
                        "temp_003": float(snap.temp[2]),
                        "temp_004": float(snap.temp[3]),
                        "temp_005": float(snap.temp[4]),
                        "temp_006": float(snap.temp[5]),
                        "temp_007": float(snap.temp[6]),
                        "temp_008": float(snap.temp[7]),
                        "temp_009": float(snap.temp[10]),
                        "temp_010": float(snap.temp[11]),
                        "temp_011": float(snap.temp[12]),
                        "temp_012": float(snap.temp[13]),
                        "temp_013": float(snap.temp[14]),
                        "temp_014": float(snap.temp[15]),
                        "temp_015": float(snap.temp[16]),
                        "temp_016": float(snap.temp[17]),
                        "temp_017": float(snap.temp[20]),
                        "temp_018": float(snap.temp[21]),
                        "temp_019": float(snap.temp[22]),
                        "temp_020": float(snap.temp[23]),
                        "temp_021": float(snap.temp[24]),
                        "temp_022": float(snap.temp[25]),
                        "temp_023": float(snap.temp[26]),
                        "temp_024": float(snap.temp[27]),
                        "temp_025": float(snap.temp[28]),
                        "temp_026": float(snap.temp[29]),
                        "temp_027": float(snap.temp[30]),
                        "temp_028": float(snap.temp[31]),
                        "temp_029": float(snap.temp[32]),
                        "temp_030": float(snap.temp[33]),
                        "temp_031": float(snap.temp[34]),
                        "temp_032": float(snap.temp[35]),
                        "temp_033": float(snap.temp[36]),
                        "temp_034": float(snap.temp[37]),
                        "temp_035": float(snap.temp[38]),
                        "temp_036": float(snap.temp[39]),
                        "temp_050": float(snap.temp[50]),
                        "temp_051": float(snap.temp[51]),
                        "temp_052": float(snap.temp[52]),
                        "temp_053": float(snap.temp[53]),
                        "temp_054": float(snap.temp[54]),
                        "temp_055": float(snap.temp[55]),
                        "temp_056": float(snap.temp[56]),
                        "temp_057": float(snap.temp[57]),
                        "temp_058": float(snap.temp[58]),
                        "temp_059": float(snap.temp[59]),
                        "temp_060": float(snap.temp[60]),
                        "temp_061": float(snap.temp[61]),
                        "temp_062": float(snap.temp[62]),
                        "temp_063": float(snap.temp[63]),
                        "temp_064": float(snap.temp[64]),
                        "temp_065": float(snap.temp[65]),
                        "temp_066": float(snap.temp[66]),
                        "temp_067": float(snap.temp[67]),
                        "temp_068": float(snap.temp[68]),
                        "temp_069": float(snap.temp[69]),
                        "temp_070": float(snap.temp[70])
                    }
                }
            ]       
            try:
                clientInflux.write_points(json_temperatureS)
            except:
                print("Erro ao gravar no Banco de dados")
