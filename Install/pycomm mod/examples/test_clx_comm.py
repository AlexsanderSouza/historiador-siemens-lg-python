from pycomm.ab_comm.clx import Driver as ClxDriver
import logging

from time import sleep


if __name__ == '__main__':

    logging.basicConfig(
        filename="ClxDriver.log",
        format="%(levelname)-10s %(asctime)s %(message)s",
        level=logging.DEBUG
    )
    c = ClxDriver()

    print c['port']
    print c.__version__
    

    if c.open('192.168.0.167',3):
        try:
            # r_array = c.read_array("F20_CreamReceoption.Tickets",2)
            # print r_array
            # for tag in r_array:
            #     print (tag)
            # x = c.read_tag(['Python_Teste_01'])
            # print x[0][1]
            # print(c.read_tag(['F20_CreamReceoption']))
            # print(c.read_tag('Python_Teste_03'))
            # print(c.read_tag(['Python_Teste_04']))
            print(c.read_string('F20_CreamReceoption.Tickets[0].StartTime'))
            
            # print(c.read_tag(['parts', 'ControlWord', 'Counts']))
            # print(c.write_string('Python_Teste_06', 'Flex Automacao'))
            # print(c.write_tag(('TankSelectedToExpedition', 26, 'INT')))
            # print(c.write_tag([('Counts', 26, 'INT')]))
            # print(c.write_tag([('Counts', -26, 'INT'), ('ControlWord', -30, 'DINT'), ('parts', 31, 'DINT')]))
            c.close()
        except Exception as e:
            c.close()
            print e
            pass
    # To read an array
    #  r_array = c.read_array("F20_CreamReceoption", 1750)
    #  for tag in r_array:
    #      print (tag)
    # To read string
    # c.write_string('TEMP_STRING', 'my_value')
    # c.read_string('TEMP_STRING')
    # reset tha array to all 0
    # w_array = []
    # for i in xrange(1750):
    #     w_array.append(0)
    # c.write_array("TotalCount", w_array, "SINT")

        

        