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
    def __init__(self, text, group, coordinates):
        self.text = text
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
                arduino.name = name
                arduino.model = model
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
                    Relation(name, element[3].text, coordinates))
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


def addThis(component, relation, direction):
    global relations
    for child in relations:
        if child == relation:
            if direction == 'to':
                child.toEle = component
            elif direction == 'from':
                child.fromEle


def addInfoToRelations():
    for relation in relations:
        # print(relation.__dict__)
        if 'test' in relation.name:
            additional = relation.additional.split(';')
            print(additional)

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

            print(x1, y1, '   ', x2, y1, '     w:', w)
            print(x1, y2, '   ', x2, y2, '     h:', h)

            print(relation.name)

            # print(additional[0])
            # print(additional[1])
            # print(additional[2])
            # print(additional[3])

            toRight = False
            toLeft = False
            toBottom = False
            toTop = False

            if xF < xT:
                toRight = True
                print('toRight')
            elif xF > xT:
                toLeft = True
                print('toLeft')
            if yF < yT:
                toBottom = True
                print('toBottom')
            elif yF > yT:
                toTop = True
                print('toTop')

            for component in components:
                cx1 = int(component.coordinates['x'])
                cy1 = int(component.coordinates['y'])
                cx2 = int(cx1)+int(component.coordinates['w'])
                cy2 = int(cy1)+int(component.coordinates['h'])

                if 'SimpleClass' in component.name:
                    print(component.name)
                    print(cx1, cy1, '     ', cx2, cy1)
                    print(cx1, cy2, '     ', cx2, cy2)

                    boundaries = [cx1, cx2, cy1, cy2]
                    horizontal = range(cx1, cx2+1)
                    vertical = range(cy1, cy2+1)
                    # bond = [range(1, 4) + range(6, 99)]
                    # if 1 in bond:
                    #     print('in bound\n\n')
                    # else:
                    #     print('not in bound \n\n')
                    # print('x', x, x2, toLeft)
                    # print(horizontal)
                    # print(x in horizontal)
                    if toLeft:
                        if x1 in horizontal:
                            print('touching on horizontal')
                        if toTop:
                            if y1 in vertical:

                                print('touching vertical')
                                addThis(component, relation, 'to')
                        elif toBottom:
                            if y1+h in vertical:
                                addThis(component, relation, 'to')

                                print('touching vertical')
                        else:
                            if (y1+y1+h)/2:
                                print('touching vertical')
                                addThis(component, relation, 'to')

                    elif toRight:
                        print(x1+w, horizontal)
                        if x1+w in horizontal:
                            print('touching on horizontal')
                        if toTop:
                            print(y1, vertical)
                            if y1 in vertical:
                                print('touching vertical')
                                addThis(component, relation, 'to')

                        elif toBottom:
                            if y1+h in vertical:
                                print('touching vertical')
                                addThis(component, relation, 'to')

                        else:
                            if((y1+y1+h)/2):
                                print('touching vertical')
                                addThis(component, relation, 'to')

                    elif toTop:
                        # print(x, horizontal)
                        if (x1+x1+w)/2 in horizontal:
                            print('touching horizontal')
                            print(y1, vertical)
                            if y1 in vertical:
                                print('touching vertical')
                                addThis(component, relation, 'to')

                    elif toBottom:
                        if x1 in horizontal:
                            print('touching horizontal')
                            if y1+h in vertical:
                                print('touching vertical')
                                addThis(component, relation, 'to')

                            # print(y, y+h, vertical)
                            # print('y+h', y+h)
                            # if toTop and y in vertical:
                            #     print('touching x and y on ', x, y, '\n')
                            # elif toBottom and y+h in vertical:
                            #     print('touching x and y2 on ', x, y+h, '\n')
                            # if toTop and y in boundaries:
                            #     print('touching x and y on ', x, y, '\n')
                            # elif toBottom and y+h in boundaries:
                            #     print('ttttouching x and y2 on ', x, y+h, '\n')

                            # print('center:', (x2-x1)/2+x1, (y2-y1)/2+y1)
                            # print('')


def printAll():
    # for item in methods:
    #     print(item.group)
    # for item in components:
    #     print(item.__dict__)
    #     print(item.methods)
    #     print('digital', item.digitalPorts)
    #     print(item.group)
    for item in relations:
        if item.toEle != None:
            print(item.name, ' aponta de ', ' para ', item.toEle.name)

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
