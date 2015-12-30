'''
Created on Nov 23, 2015

@author: ams
'''

import svgwrite
from svgwrite import cm, mm 
import math
import sys

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

def snowflake(center, strSeed, dwg):
    edge = dwg.defs.add(dwg.g(id="flake_edge{0}_{1}".format(center[0], center[1])))
    bg = dwg.defs.add(dwg.g(id="background{0}_{1}".format(center[0], center[1]), stroke="aqua", stroke_width=15, stroke_linecap='round'))
    fg = dwg.defs.add(dwg.g(id="foreground{0}_{1}".format(center[0], center[1]), stroke="black", stroke_width=2, stroke_linecap='round'))
    start = toUser((center[0], center[1]-3.3))
    end = toUser(center)
    edge.add(dwg.path(d="M {0},{1} L {2},{3}".format(start[0], start[1], end[0], end[1])))
    
    for index in range(len(strSeed) - 1):
        d = distance(strSeed[index], strSeed[index + 1])/5.5
        a = angle(strSeed[index])
        r = length(strSeed[index + 1])/5.5
        x = abs(math.cos(a) * r)
        y = abs(math.sin(a) * r)
        start = toUser((center[0],center[1] - d))
        end = toUser((center[0] + x, center[1] - y))
        edge.add(dwg.path(d="M {0},{1} L {2},{3}".format(start[0], start[1], end[0], end[1])))
    
    #Reflect the whole group across the centerline
    edge_m = dwg.defs.add(dwg.g(id="edge_b{0}_{1}".format(center[0], center[1])))
    edge_m.add(dwg.use(edge, insert=(0, 0)))
    edge_m.scale(-1, 1)
    edge_m.translate(-2*center[0]*35.43307 ,0)
    
    #Rotate and duplicate for 6-way symmmetry
    for i in range(6):
        rotation = i * 60
        newEdge = dwg.g(id="edge_{0}_{1}_{2}".format(rotation, center[0], center[1]))
        newEdge.add(dwg.use(edge_m, insert = (0,0)))
        newEdge.add(dwg.use(edge, insert = (0,0)))
        newEdge.rotate(rotation, center=(toUser((center))))
        bg.add(newEdge)
        fg.add(newEdge)
        
    dwg.add(bg)
    dwg.add(fg)

def single_flake(path, string):
    size = (10,10)
    fullpath = path + string + ".svg"
    dwg = svgwrite.Drawing(fullpath, size=(toCm(size)), profile='full')
    snowflake((5,5),string,dwg)
    dwg.save()

def single_flake_png(path, string):
    fullpath = path + string + ".svg"
    pngpath = path + string + ".png"
    #Convert the svg to PNG
    #Thanks to http://stackoverflow.com/questions/6589358/convert-svg-to-png-in-python
    import cairo
    import rsvg
    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 350, 350)
    ctx = cairo.Context(img)
    handle = rsvg.Handle(fullpath)
    handle.render_cairo(ctx)
    img.write_to_png(pngpath)
    
if __name__ == '__main__':
    single_flake("./flakes/", "testsnow")                
