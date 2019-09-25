import unicodedata

import xml.etree.ElementTree as ET
tree = ET.parse('./iot.xml')
root = tree.getroot()

methods = []
libMethods = []

file = open('gen.cpp', 'w')  # clear file
with open('gen.cpp', 'a') as file:

    def p(*args, **kwargs):
        print(''.join(map(str, args)), **kwargs)
        file.write(''.join(map(str, args)), **kwargs)
        file.write('\n')

    file.truncate()
    # p(root.tag)
    libs = []

    for i, component in enumerate(root):
        # p(component.tag)#, component.attrib)
        if component.tag == 'Arduino':
            arduinoModel = component.get('model')
            totalDigitalPorts = int(component.get('digitalPorts'))
            totalAnalogPorts = component.get('analogPorts')
            p(component.get('connector'))
            # p(component.text)
            # p("found arduino!")
            digitalPorts = 0
            analogPorts = 0

        else:
            method = component.get('method')
            # p(method)
            methods.append(method)
            libName = component.get('library')
            libPath = 'arduino-libraries/'+libName+'/src/'+libName+'.h'
            libFile = open('arduino-libraries/'+libName +
                           '/src/'+libName+'.h', 'r')
            if libName not in libs:
                libs.append(libName)
                p('#include <'+libPath+'>')
                # p('#include <',libName,'>')

                longComment = False
                with open(libPath) as file_iterator:
                    for line in file_iterator:
                        if longComment:
                            if "*/" in line:
                                longComment = False
                        else:
                            if "/*" in line:  # long comment
                                longComment = True

                            if "()" in line or "(int" in line:
                                # if any(elem in ["void","int","bool"] for elem in line):

                                libMethod = line.split(
                                    "//")[0].replace("  ", "")
                                libMethods.append(libMethod)

                                # print(file_iterator)
                                print(next(file_iterator))
                            else:
                                print("denied" + line)

            # with open(libFile) as f:
            #     while 'setSpeed(' not in f.readline():
            #         continue
            #     print(f.readlines())

            # iterator = iter(libFile.splitlines())
            # for line in iterator:
            #     if "setSpeed(" in line:
            #         # print next(iterator)
            #         print (line)

            for port in range(0, int(component.get('digitalPorts'))):
                digitalPorts += 1
                p(component.get('type'), ' ', component.get('name'),
                  ' = ', component.get('type'), '(',  digitalPorts, ')')

            for port in range(0, int(component.get('digitalPorts'))):
                digitalPorts += 1
                p(component.get('type'), ' ', component.get('name'),
                  ' = ', component.get('type'), '(',  digitalPorts, ')')

    p('// Code generated for Arduino ', arduinoModel)
    p('// with ', totalDigitalPorts, ' digital ports in total with ',
      digitalPorts, ' in use and ', totalDigitalPorts-digitalPorts, ' free')
    p('// and  ', totalAnalogPorts, ' analog ports in total')

    p('void setup(){\n\n}')
    p('void loop(){\n\n}')
    print(libMethods)
