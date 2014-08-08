"""
Primitive Utilities
===================

Provides helper functions for commonly-accomplished tasks: creating rectangles using wire segments,
for example.

"""

from eaglepy import primitives
import math

def _get_chamfer_points(p1, p2, chamfer):
    """
    Offset the start and end poitns of a line by a specified distance. 
    
    :param p1: The first point.
    :param p2: The second point.
    :param chamfer_distance: The chamfer distance.
    
    :returns: Two transformed points: ``_p1, _p2``.
    
    """
    
    d, a = _cartesian_to_polar(p2[0], p2[1], p1[0], p1[1])
    _x1 = p1[0] + chamfer * math.cos(a)
    _y1 = p1[1] + chamfer * math.sin(a)
    
    _x2 = p1[0] + (d - chamfer) * math.cos(a)
    _y2 = p1[1] + (d - chamfer) * math.sin(a)
    
    return (_x1, _y1), (_x2, _y2)


def add_wire_rect_tl(parent, 
                     x, 
                     y, 
                     rect_width, 
                     rect_height,
                     wire_width,
                     layer,
                     chamfer = 0,
                     curve = primitives.Wire.DEFAULT_CURVE,
                     extent = primitives.Wire.DEFAULT_EXTENT,
                     style = primitives.Wire.DEFAULT_STYLE,
                     cap = primitives.Wire.DEFAULT_CAP):
    """
    Add a rectangle comprised of wires with the origin in the top-left corner to a list of primitives.
    
    :param parent: A list of primitives to which to append the wires.
    :param x: The x position of the top-left corner.
    :param y: The y position of the top-left corner.
    :param rect_width: The width of the rectangle.
    :param rect_height: The height of the rectangle.
    :param wire_width: The width of each wire.
    :param layer: The number of the layer to which to add the rectangle.
    :param chamfer: The amount by which to chamfer the corners of the rectangle.
    """
    x1 = min(x, x+rect_width)
    y1 = min(y, y+rect_height)
    
    x2 = max(x, x+rect_width)
    y2 = max(y, y+rect_height)
    
    points = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]
    
    if chamfer > 0:
        new_points = []
        
        for i in range(1, len(points)):
            p1, p2 = _get_chamfer_points(points[i-1], points[i], chamfer)
            new_points.append(p1)
            new_points.append(p2)
            
        p1, p2 = _get_chamfer_points(points[-1], points[0], chamfer)
        new_points.append(p1)
        new_points.append(p2)
            
        points = new_points

    for i in range(1, len(points)):
        parent.append(primitives.Wire(points[i-1][0], points[i-1][1], points[i][0], points[i][1], wire_width, layer, curve, extent, style, cap))
        
    parent.append(primitives.Wire(points[-1][0], points[-1][1], points[0][0], points[0][1], wire_width, layer, curve, extent, style, cap))
        
def add_wire_rect_center(parent, 
                     x, 
                     y, 
                     rect_width, 
                     rect_height,
                     wire_width,
                     layer,
                     chamfer = 0,
                     curve = primitives.Wire.DEFAULT_CURVE,
                     extent = primitives.Wire.DEFAULT_EXTENT,
                     style = primitives.Wire.DEFAULT_STYLE,
                     cap = primitives.Wire.DEFAULT_CAP):
    """
    Add a rectangle comprised of wires with the origin in the center to a list of primitives.
    
    :param parent: A list of primitives to which to append the wires.
    :param x: The x position of the center.
    :param y: The y position of the center.
    :param rect_width: The width of the rectangle.
    :param rect_height: The height of the rectangle.
    :param wire_width: The width of each wire.
    :param layer: The number of the layer to which to add the rectangle.
    :param chamfer: The amount by which to chamfer the corners of the rectangle.
    """
    
    add_wire_rect_tl(parent, 
                     x - rect_width / 2.0, 
                     y - rect_height / 2.0, 
                     rect_width, 
                     rect_height, 
                     wire_width, 
                     layer, 
                     chamfer,
                     curve, 
                     extent, 
                     style, 
                     cap)
    
def add_wire_ngon(parent,
                  x,
                  y,
                  num_sides,
                  radius,
                  wire_width,
                  layer,
                  displacement = 0,
                  curve = primitives.Wire.DEFAULT_CURVE,
                  extent = primitives.Wire.DEFAULT_EXTENT,
                  style = primitives.Wire.DEFAULT_STYLE,
                  cap = primitives.Wire.DEFAULT_CAP):
    """
    Add an ``n``-sided inscribed polygon comprised of wires to a list of primitives.
    
    :param parent: A list of primitives to which to append the wires.
    :param x: The x position of the center. 
    :param y: The y position of the center. 
    :param num_sides: The number of sides of the polygon.
    :param radius: The radius of the circle in which the polygon is inscribed.
    :param wire_width: The width of each wire.
    :param layer: The number of the layer to which to add the polygon.
    :param displacement: The angular displacement of the polygon.
    
    """
    
    
    angle = 2*math.pi/float(num_sides)
    
    x = radius + radius * math.cos(displacement)
    y = radius + radius * math.sin(displacement)
    
    for i in range(num_sides):
        _x = radius + radius * math.cos((i+1)*angle + displacement)
        _y = radius + radius * math.sin((i+1)*angle + displacement)
        
        parent.append(primitives.Wire(x, y, _x, _y, wire_width, layer, curve, extent, style, cap))
    
        x = _x
        y = _y
    
def _cartesian_to_polar(x, y, xc=0, yc=0):
    """
    Given a point in cartesian coordinates, return the corresponding polar coordinates.
    
    :param x: The x value of the point.
    :param y: The y value of the point.
    :param xc: The x value of the origin position.
    :param yc: The y value of the origin position.
    """
    
    d = math.sqrt(math.pow(x - xc, 2) + math.pow(y - yc, 2))
    
    # The angle of the point
    a = math.atan2(y - yc, x - xc)
    
    return d, a
    

