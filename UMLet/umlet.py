import unicodedata

import xml.etree.ElementTree as ET
tree = ET.parse('./UMLet/Model2.xml')
root = tree.getroot()

file = open('gen.cpp', 'w')  # clear file
with open('gen.cpp', 'a') as file:

    def p(*args, **kwargs):
        print(''.join(map(str, args)), **kwargs)
        file.write(''.join(map(str, args)), **kwargs)
        file.write('\n')

    file.truncate()
    # p(root.tag)
    libs = []

    for i, element in enumerate(root):
        # p(component.tag)#, component.attrib)
        if element.tag == 'element':
            for child in element:
                print(child)
                if child.tag == 'coordinates':
                    for coordinate in child:
                        if coordinate == 'x':
                            print(coordinate.x)
                        print(coordinate)
                elif child.tag == 'panel_attributes':
                    print(child)

                    # arduinoModel = element.get('model')
                    # totalDigitalPorts = int(element.get('digitalPorts'))
                    # totalAnalogPorts = element.get('analogPorts')
                    # p(child.get('connector'))
                    # p(component.text)
                    # digitalPorts = 0
                    # analogPorts = 0

                    # else:
                    #     libName = element.get('library')
                    #     libPath = 'arduino-libraries/'+libName+'/src/'+libName+'.h'
                    #     libFile = open('arduino-libraries/'+libName +
                    #                    '/src/'+libName+'.h', 'r')
                    #     if libName not in libs:
                    #         libs.append(libName)
                    #         p('#include <'+libPath+'>')
                    #         # p('#include <',libName,'>')

                    #     for port in range(0, int(element.get('digitalPorts'))):
                    #         digitalPorts += 1
                    #         p(element.get('type'), ' ', element.get('name'),
                    #           ' = ', element.get('type'), '(',  digitalPorts, ')')

                    # p('// Code generated for Arduino ', arduinoModel)
                    # p('// with ', totalDigitalPorts, ' digital ports in total with ',
                    #   digitalPorts, ' in use and ', totalDigitalPorts-digitalPorts, ' free')
                    # p('// and  ', totalAnalogPorts, ' analog ports in total')

    p('void setup(){\n\n}')
    p('void loop(){\n\n}')
