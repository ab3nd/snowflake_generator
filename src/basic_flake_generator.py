'''
Created on Nov 23, 2015

@author: ams
'''

import svgwrite
from svgwrite import cm, mm 
import math

def toCm(coords):
    return (coords[0] * cm, coords[1] * cm)

def toUser(coords):
    uuPerCm = 35.43307 
    return (coords[0] * uuPerCm, coords[1] * uuPerCm)

def distance(a,b):
    return abs(ord(a) - ord(b))

def length(a):
    return ord(a) - 97

def angle(a):
    #1 degree is 0.0174533 radians
    return (((ord(a)-97)*(360/26))/2.0) * 0.0174533
    
if __name__ == '__main__':
    size = (100, 100)
    center = (size[0]/2, size[1]/2)
    dwg = svgwrite.Drawing('test.svg', size=(toCm(size)), profile='full')
    edge = dwg.defs.add(dwg.g(id="flake_edge", stroke="black", stroke_width=1))
    
    #for group in [back, middle, edge]:
    edge.add(dwg.line(toCm((center[0], center[1]-10)), toCm(center)))

    testString = "dvdhthr"
    for index in range(len(testString) - 1):
        d = distance(testString[index], testString[index + 1])/2.0
        a = angle(testString[index])
        r = length(testString[index + 1])/2.0
        x = abs(math.cos(a) * r)
        y = abs(math.sin(a) * r)
        edge.add(dwg.line(toCm((center[0],center[1] - d)), toCm((center[0] + x, center[1] - y))))
        
    #dwg.add(edge)
     
    #Reflect the whole group across the centerline
    edge_m = dwg.defs.add(dwg.g(id='edge_m', stroke="black"))
    edge_m.add(dwg.use(edge, insert=(0, 0)))
    edge_m.scale(-1, 1)
    edge_m.translate(-size[0]*35.43307 ,0)
     
    #dwg.add(edge_m)
     
    #Rotate and duplicate for 6-way symmmetry
    for i in range(6):
        rotation = i * 60
        newEdge = dwg.g(id="edge_{0}".format(rotation), stroke="black")
        newEdge.add(dwg.use(edge, insert=(0,0)))
        newEdge.add(dwg.use(edge_m, insert = (0,0)))
        newEdge.rotate(rotation, center=(toUser((center))))
        dwg.add(newEdge)

    dwg.save()
