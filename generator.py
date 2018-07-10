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
            # p(component.text)
            # p("found arduino!")
            p('// Code generated for Arduino ',component.get('model'))
            p('// with ',component.get('digitalPorts'),' digital ports in total')
            p('// and  ',component.get('analogPorts'),' analog ports in total')
            p(component.get('conector'))
        

        else:
            lib = component.get('library')
            if lib not in libs:
                libs.append(lib)
                p(lib)
