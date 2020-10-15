from snap7 import util
from snap7 import client
import LogInflux
import time
 
plc = client.Client()

def read_siemens(ipSiemens, db):
    global temp
    if not plc.get_connected() :
        try:
            startTemp = time.time()
            print "Conectando ao PLC Siemens..."
            plc.connect(ipSiemens, 0, 1) # connect to PLC
            msg1 = "Conectado ao PLC Siemens, tempo:" + str(time.time() - startTemp) +" IP:"+str(ipSiemens)+" db:"+str(db)
            print msg1
            LogInflux.influx_log(msg1)
        except:
            msg1 = "Sem conexao com PLC Siemens IP:"+ str(ipSiemens)
            print msg1
            LogInflux.influx_log(msg1)
            LogInflux.influx_plc(1) # 1 para status de erro
            plc.disconnect()
            temp = ["ERRO"]
            
    if plc.get_connected() :
        try:
            area = 0x84    # area for DB memory
            start = 0      # location we are going to start the read
            length = 288    # tamanho em bytes da leitura, com uma casa a mais do ultimo dado desejado no PLC
            # bit = 0
            # which bit in the db memory byte we are reading 
            startTemp = time.time()
            byte = plc.read_area(area,db,start,length)
            temp = []
            i = 0
            # Cria Array com dados do PLC
            while i <= length-4:
                temp.append(round(util.get_real(byte,i),3))
                i=i+4
            LogInflux.influx_plc(0) # 0 para status OK
        except :
            msg1 = "PLC Siemens falha na leitura ip:"+ str(ipSiemens)
            print msg1
            LogInflux.influx_log(msg1)
            LogInflux.influx_plc(1)
            plc.disconnect()
            temp = ["ERRO"]



    