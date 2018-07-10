import unicodedata

import xml.etree.ElementTree as ET
tree = ET.parse('./iot.xml')
root = tree.getroot()




file = open('gen.cpp', 'w')  # clear file
with open('gen.cpp', 'a') as file:

    def p(*args, **kwargs):
        print(''.join(map(str,args)), **kwargs)
        file.write(''.join(map(str,args)), **kwargs)
        file.write('\n')

    file.truncate()
    # p(root.tag)
    libs = []


    for i, component in enumerate(root):
        # p(component.tag)#, component.attrib)
        if component.tag =='Arduino':
            arduinoModel = component.get('model')
            totalDigitalPorts = int(component.get('digitalPorts'))
            totalAnalogPorts = component.get('analogPorts')
            p(component.get('connector'))
            # p(component.text)
            # p("found arduino!")
            digitalPorts=0
            analogPorts=0

        else:
            lib = component.get('library')
            if lib not in libs:
                libs.append(lib)
                p('#include <',lib,'>')
            


            for port in range(0,int(component.get('digitalPorts'))):
                digitalPorts+=1
                p(component.get('type'),' ',component.get('name'),' = ', component.get('type'),'(',  port,')')
                



    p('// Code generated for Arduino ', arduinoModel)
    p('// with ',totalDigitalPorts,' digital ports in total with ',digitalPorts,' in use and ',totalDigitalPorts-digitalPorts,' free')
    p('// and  ',totalAnalogPorts,' analog ports in total')

    p('void setup(){\n\n}')
    p('void loop(){\n\n}')