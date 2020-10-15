from pycomm.ab_comm.clx import Driver as ClxDriver
import time
import LogInflux

c = ClxDriver()

def read_tag(ip, slot, tag_name,qtd):
    erro = ["ERRO"]
    if not c.is_connected() :
        try :
            startTemp = time.time()
            print "Conectando ao PLC Rockwell..."
            c.open(str(ip),int(slot)) # connect to PLC
            # print "Conectado ao PLC Rockwell, tempo:",time.time() - startTemp,"IP:",ip,"slot:",slot
            msg = "Conectado ao PLC Rockwell, tempo:" + str(time.time() - startTemp) +" IP:"+str(ip)+" slot:"+str(slot)
            print msg
            LogInflux.influx_log(msg)
        except :
            msg = "Sem conexao com PLC Rockwell IP:"+str(ip)+" slot:"+str(slot)
            print msg
            LogInflux.influx_log(msg)
            LogInflux.influx_plc(2) # 2 para status de erro
            return erro
    if c.is_connected() :
        try: 
            r_array = c.read_array(str(tag_name), int(qtd))
            LogInflux.influx_plc(0) # 0 para status OK
            return r_array
        except :
            msg = "Erro ao ler dados no PLC Rockwell ip:"+str(ip)+" slot:"+str(slot)
            print msg
            LogInflux.influx_log(msg)
            LogInflux.influx_plc(2) # 2 para status de erro
            return erro
    

def read_string_tag(ip, slot, tag_name):
    if not c.is_connected() :
        try :
            startTemp = time.time()
            print "Conectando ao PLC Rockwell..."
            c.open(str(ip),int(slot)) # connect to PLC
            msg = "Conectado ao PLC Rockwell, tempo:" + str(time.time() - startTemp) +" IP:"+str(ip)+" slot:"+str(slot)
            print msg
            LogInflux.influx_log(msg)
        except :
            msg = "Sem conexao com PLC Rockwell IP:"+str(ip)+" Slot:"+str(slot)
            print msg
            LogInflux.influx_log(msg)
            return "0"
    if c.is_connected() :
        try:
            items = c.read_string(str(tag_name))
            return items
        except :
            msg = "Erro ao ler dados no PLC Rockewell ip:"+str(ip)+"slot:"+str(slot)
            print msg
            LogInflux.influx_log(msg)
            return "0"


def set_tag(ip, slot, tag,value,type1):
    if not c.is_connected() :
        try :
            startTemp = time.time()
            print "Conectando ao PLC Rockwell..."
            c.open(str(ip),int(slot)) # connect to PLC
            msg = "Conectado ao PLC Rockwell, tempo:" + str(time.time() - startTemp) +" IP:"+str(ip)+" slot:"+str(slot)
            print msg
            LogInflux.influx_log(msg)
        except :
            msg = "Sem conexao com PLC Rockwell IP:"+str(ip)+" Slot:"+str(slot)
            print msg
            LogInflux.influx_log(msg)
    if c.is_connected() :
        try:
            items = c.write_tag(str(tag), int(value), str(type1))
            print items
            return items
        except Exception as e:
            msg = "Erro ao gravar dados no PLC Rockewell ip:"+str(ip)+"slot:"+str(slot)
            print msg + " erro: "+ e
            LogInflux.influx_log(msg)
            return 0
        

        