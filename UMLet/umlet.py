import unicodedata

import xml.etree.ElementTree as ET

libs = []

components = []


class Component:
    def __init__(self, digitalPorts, analogPorts, libName, coordinates, group):
        self.digitalPorts = digitalPorts
        self.analogPorts = analogPorts
        self.libName = libName
        self.coordinates = coordinates
        self.methods = []
        self.group = group
    methods = []
    # def __repr__(self):
    #     return 'teste'
    # this.digitalPorts, this.analogPorts, this.libName, this.coordinates


class Arduino(Component):
    pass


arduino = Arduino


class Method:
    def __init__(self, text, group, coordinates):
        self.text = text
        self.group = group
        self.coordinates = coordinates
    text = 'none'


methods = []

relations = []


class Relation:
    def __init__(self, fromEle, toEle, additional, coordinates):
        self.fromEle = fromEle
        self.toEle = toEle
        self.additional = additional
        self.coordinates = coordinates


def readUML():

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

        for i, element in enumerate(root):

            if element.tag == 'element':
                # p(component.tag)#, component.attrib)
                coordinates = {}
                coordinates['x'] = element[1][0].text
                coordinates['y'] = element[1][1].text
                coordinates['w'] = element[1][2].text
                coordinates['h'] = element[1][3].text

                attributes = element[2].text
                digitalPorts = 0
                analogPorts = 0
                method = 'none'
                group = 0
                lib = 'none'

                for line in attributes.splitlines():
                    if 'digitalPorts' in line:
                        digitalPorts = int(''.join(filter(str.isdigit, line)))
                        # print('found digital: ', digitalPorts)
                    elif 'analogPorts' in line:
                        analogPorts = int(''.join(filter(str.isdigit, line)))
                    elif 'group' in line:
                        group = int(''.join(filter(str.isdigit, line)))
                        # print('found group: ', group)
                    elif ')' in line:
                        methodText = line
                    elif 'lib' in line:
                        lib = line.replace('lib', '').replace(
                            ' ', '').replace('=', '')

                if 'method' in attributes:
                    global methods
                    # tempElement = {}
                    # tempElement = Method
                    # tempElement.text = methodText
                    # tempElement.coordinates = coordinates
                    # tempElement.group = group
                    # group = 0
                    methods.append(Method(methodText, group, coordinates))
                    # methods[len(methods):] = [tempElement]
                    # print('tempmethodgroup', methods[-1].group)
                    # method

                elif 'Arduino' in attributes:
                    # print('found')
                    global arduino
                    arduino.digitalPorts = digitalPorts
                    arduino.analogPorts = analogPorts
                    arduino.coordinates = coordinates
                    arduino.group = group

                elif element[0].text == "Relation":
                    global relations
                    # tempElement = {}
                    # tempElement = Relation
                    # tempElement.additional = element[3].text
                    # tempElement.coordinates = coordinates
                    # tempElement.group = group

                    relations.append(
                        Relation('', '', element[3].text, coordinates))
                else:
                    global components
                    # tempElement = {}
                    # tempElement = Component
                    # tempElement.digitalPorts = digitalPorts
                    # # print('here digital', tempElement.digitalPorts)
                    # tempElement.analogPorts = analogPorts
                    # tempElement.coordinates = coordinates
                    # tempElement.group = group
                    components.append(
                        Component(digitalPorts, analogPorts, lib, coordinates, group))
        # for method in methods:
            # print('methodgroup', method.group)
            # if element[0].text == 'UMLClass':
            #     # for child in element:
            #     #     if child.tag == 'coordinates':
            #     #         print(child[0].text)

            # if child.tag == 'id':
            #     if child.text == 'Relation':

            #         Relation rel
            # print(child)
            # print(coordinate.tag)
            # elif child.tag == 'panel_attributes':
            #     print(child.tag)

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

            # p('void setup(){\n\n}')
            # p('void loop(){\n\n}')


def addMethodsToComponents():
    for method in methods:
        # print(method.__dict__)
        for component in components:
            # print(method.group, component.group)
            if int(method.group) == int(component.group):

                component.methods.append(method)

        if int(method.group) == int(arduino.group):
            # print(method.group, component.group)
            # print(method.__dict__)
            # global arduino
            arduino.methods.append(method)
        # print('arduino', arduino.group)
        # print('method', method.group)


def printAll():
    # for item in methods:
    #     print(item.group)
    for item in components:
        print(item.__dict__)
        # print(item.methods)
        # print('digital', item.digitalPorts)
    #     print(item.group)
    # # for item in relations:
    # #     print(item.__dict__)

    print(arduino.__dict__)
    # print(arduino.methods[0].__dict__)


readUML()
addMethodsToComponents()


printAll()
print('end')
