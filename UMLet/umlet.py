import unicodedata
import xml.etree.ElementTree as ET
libs = []
components = []


class Component:
    def __init__(self, name, model, digitalPorts, analogPorts, libName, coordinates, group):
        self.name = name
        self.model = model
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
    def __init__(self, name, group, coordinates):
        self.name = name
        self.group = group
        self.coordinates = coordinates
    text = 'none'


methods = []

relations = []


class Relation:
    def __init__(self, name, additional, coordinates):
        self.name = name
        self.additional = additional
        self.coordinates = coordinates

    fromEle = None
    toEle = None


def readUML():

    tree = ET.parse('./UMLet/Model2.xml')
    root = tree.getroot()

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
            model = 'none'
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
                elif 'model' in line:
                    model = lib = line.replace('model', '').replace(
                        ' ', '').replace('=', '')

            name = attributes.splitlines()[0].replace('//', '')
            if 'method' in attributes:
                global methods
                methods.append(Method(methodText, group, coordinates))

            elif 'Arduino' in attributes:
                global arduino
                arduino.name = name
                arduino.model = model
                arduino.digitalPorts = digitalPorts
                arduino.analogPorts = analogPorts
                arduino.coordinates = coordinates
                arduino.group = group

            elif "relation" in attributes:
                global relations
                relations.append(
                    Relation(name, element[3].text, coordinates))
            else:
                global components
                components.append(
                    Component(name, model, digitalPorts, analogPorts, lib, coordinates, group))
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


def addComponentsToRelation(fromComponent, toComponent, relation):
    # print('adding:', fromComponent.name, toComponent.name, relation.name)
    global relations
    for child in relations:
        if child == relation:
            child.fromEle = fromComponent
            child.toEle = toComponent


def checkBoundaries(x, y, element):
    x1 = int(element.coordinates['x'])
    y1 = int(element.coordinates['y'])
    x2 = int(x1)+int(element.coordinates['w'])
    y2 = int(y1)+int(element.coordinates['h'])
    horizontal = range(x1, x2+1)
    vertical = range(y1, y2+1)
    if x in horizontal and y in vertical:
        return element


def getElementAtPosition(x, y):
    # print('looking for component at', x, y)
    for component in components:
        result = checkBoundaries(x, y, component)
        if result:
            return result

        for method in component.methods:
            result = checkBoundaries(x, y, method)
            if result:
                return result

    result = checkBoundaries(x, y, arduino)
    if result:
        return result
    for method in arduino.methods:
        result = checkBoundaries(x, y, method)
        if result:
            return result
    # if 'SimpleClass' in component.name:
    # print(component.name)
    # print(cx1, cy1, '     ', cx2, cy1)
    # print(cx1, cy2, '     ', cx2, cy2)


def addInfoToRelations():
    for relation in relations:
        additional = relation.additional.split(';')

        xF = int(float(additional[0]))  # from and to
        yF = int(float(additional[1]))
        xT = int(float(additional[2]))
        yT = int(float(additional[3]))

        w = int(relation.coordinates['w'])
        h = int(relation.coordinates['h'])

        x1 = int(relation.coordinates['x']) + xF
        y1 = int(relation.coordinates['y']) + yF
        x2 = int(relation.coordinates['x']) + w - (w-xT)
        y2 = int(relation.coordinates['y']) + h - (h-yT)

        # print(relation.name)
        # print(additional)
        # print(x1, y1, '   ', x2, y1, '     w:', w)
        # print(x1, y2, '   ', x2, y2, '     h:', h)
        print(getElementAtPosition(x2, y2))
        addComponentsToRelation(getElementAtPosition(
            x1, y1), getElementAtPosition(x2, y2), relation)


def printAll():
    # for item in methods:
    #     print(item.group)
    # for item in components:
    #     print(item.__dict__)
    #     print(item.methods)
    #     print('digital', item.digitalPorts)
    #     print(item.group)
    for item in relations:

        print(item.name)
        print('aponta de ', item.fromEle.name,
              ' para ', item.toEle.name)

    print(arduino.__dict__)
    # print(arduino.methods[0].__dict__)


def generateCode():
    file = open('./UMLet/gen.cpp', 'w')  # clear file
    with open('./UMLet/gen.cpp', 'a') as file:

        def p(*args, **kwargs):
            print(''.join(map(str, args)), **kwargs)
            file.write(''.join(map(str, args)), **kwargs)
            file.write('\n')
        file.truncate()

        p('// Code generated for Arduino ', arduino.model)
        p('// with ', arduino.digitalPorts, ' digital ports in total with ',
          200, ' in use and ', 200, ' free')
        p('// and  ', arduino.analogPorts, ' analog ports in total')
        p('void setup(){\n\n}')
        p('void loop(){\n\n}')

        # print(libMethods)
    # for port in range(0, int(component.get('digitalPorts'))):
    #     digitalPorts += 1
    #     p(component.get('type'), ' ', component.get('name'),
    #       ' = ', component.get('type'), '(',  digitalPorts, ')')

    # for port in range(0, int(component.get('digitalPorts'))):
    #     digitalPorts += 1
    #     p(component.get('type'), ' ', component.get('name'),
    #       ' = ', component.get('type'), '(',  digitalPorts, ')')


readUML()
addMethodsToComponents()
addInfoToRelations()
printAll()
# generateCode()
print('end')
