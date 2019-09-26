import weakref
import re
import unicodedata
import xml.etree.ElementTree as ET

libs = []


class Element:

    def linkParent(self, element):
        self.parentName = element.name  # might have problems with garbage collection
    # self.parent = weakref.ref(parent) # best way to do this

    def getParent(self):
        for component in components:
            if component.name == self.parentName:
                return component
        if arduino.name == self.parentName:
            return arduino

    def linkToElement(self, element):
        self.toElement = element.name

    def getToElements(self):
        # print('serching from', self.name)
        elements = []
        for relation in relations:
            if relation.fromElement == self:
                # print('found ', relation.fromElement.name,
                    #   'pointing to', relation.toElement.name)
                elements.append(relation.toElement)

        return elements


class Component(Element):
    def __init__(self, name, model, digitalPorts, analogPorts, libName, coordinates, group):
        self.name = name
        self.model = model
        self.digitalPorts = digitalPorts
        self.analogPorts = analogPorts
        self.libName = libName
        self.coordinates = coordinates
        self.methods = []
        self.group = group

    def getParent(self):
        return arduino
    # parentName = ''
    methods = []


components = []


class Arduino(Component):
    pass


arduino = Arduino


class Method(Element):
    def __init__(self, name, group, coordinates):
        self.name = name
        self.group = group
        self.coordinates = coordinates
    parentName = ''


methods = []


class Relation:
    def __init__(self, name, additional, coordinates):
        self.name = name
        self.additional = additional
        self.coordinates = coordinates
    fromElement = None
    toElement = None


relations = []


def readUML():
    tree = ET.parse('./UMLet/Model2.xml')
    root = tree.getroot()

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
        for component in components:
            if int(method.group) == int(component.group):
                method.linkParent(component)
                component.methods.append(method)

        if int(method.group) == int(arduino.group):
            method.linkParent(arduino)
            arduino.methods.append(method)


def addElementsToRelation(fromElement, toElement, relation):
    global relations
    for child in relations:
        if child == relation:
            fromElement.linkToElement(toElement)
            child.fromElement = fromElement
            child.toElement = toElement


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

        addElementsToRelation(getElementAtPosition(
            x1, y1), getElementAtPosition(x2, y2), relation)


def printAll():
    # for relation in relations:
    #     if 'single' in relation.fromElement.name:

    #         print(relation.name, 'aponta de ', relation.fromElement.name, ' para ',
    #               relation.toElement.name, ' de ', relation.toElement.getParent().name)

    #         print(relation.fromElement.getToElements())
    #         print(relation.toElement, relation.toElement.name)
    #         print('\n')
    pass
    # for item in methods:
    #     print(item.group)
    # for item in components:
    #     print(item.__dict__)
    #     print(item.methods)
    #     print('digital', item.digitalPorts)
    #     print(item.group)

    # print(arduino.__dict__)
    # print(arduino.methods[0].__dict__)


def generateCode():
    file = open('./UMLet/gen.cpp', 'w')  # clear file
    with open('./UMLet/gen.cpp', 'a') as file:
        file.truncate()

        def p(*args, **kwargs):
            print(''.join(map(str, args)), **kwargs)
            file.write(''.join(map(str, args)), **kwargs)
            file.write('\n')
        tab = '    '

        def generateDecision(element):
            for method in element.methods:
                p(method.name, '{\n')
                print(element.name, ' ', method.name,
                      ' ', method.getToElements())

                for toElement in method.getToElements():
                    for rel in relations:
                        if rel.toElement == toElement:
                            relation = rel
                            print(rel.name)
                    if 'if' in toElement.name and relation:
                        value = ''
                        ifTrue = ''
                        ifFalse = ''
                        print(relation.name)
                        if 'getThis' in relation.name:
                            value = relation.toElement.name.split(' ', 1)[
                                1]
                        elif 'True' in relation.name:
                            ifTrue = relation.toElement.name
                        elif 'False' in relation.name:
                            ifFalse = relation.toElement.name

                        check = re.sub(
                            r'[0-9]+', '', toElement.name.replace('if', '').replace(' ', ''))
                        condition = re.sub(
                            r'[<>=]+', '', toElement.name.replace(
                                'if', '').replace(' ', ''))

                        p(tab, 'if (', value, check, ' ', condition, '){ \n')
                        p(tab*2, ifTrue, ';')
                        p(tab, '}')

                        if ifFalse:
                            p(tab, 'else {')
                            p(tab*2, ifFalse, ';')

                        p(tab, '}')
                    p('\n}')

                    # else:
                    # else:  # just method calling without decision-taking
                    #     p(toElement.name)

        usedDigital = 0
        usedAnalog = 0
        for component in components:
            usedDigital += component.digitalPorts
            usedAnalog += component.analogPorts

        p('// Code generated for Arduino ', arduino.model)
        p('// with ', arduino.digitalPorts, ' digital ports in total with ',
          usedDigital, ' in use and ', arduino.digitalPorts-usedDigital, ' free')
        p('// and ', arduino.analogPorts, ' analog ports in total with ',
          usedAnalog, ' in use and ', arduino.analogPorts - usedAnalog, ' free')

        generateDecision(arduino)

        # generateDecision(components[0])
        for component in components:
            pass
            # for method in component.methods:
            #     p(method.name)


readUML()
addMethodsToComponents()
addInfoToRelations()
printAll()
generateCode()
print('----------------------------TheEnd--------------------------------')
