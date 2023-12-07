from solid import *
import copy
import os

mode = "laser"
#mode = "3d_print"

defined_objects = {}

radius_dict = {}
countersunk_dict = {}

def set_mode(m):
    global mode
    mode = m
    radius_dict['m6'] = 6.5/2
    radius_dict['m3'] = 3.3/2
    if mode == "laser":
        radius_dict['m6'] = 6/2
        radius_dict['m3'] = 3/2

    countersunk_dict['m3'] = {}
    countersunk_dict['m3']['little_rad'] = radius_dict['m3']
    countersunk_dict['m3']['big_rad'] = (5.5+0.6)/2
    if mode == "laser":
        countersunk_dict['m3']['big_rad'] = (4.75+0.6)/2
        countersunk_dict['m3']['little_rad'] = (4.75+0.6)/2

    countersunk_dict['m3']['height'] = 1.7

def opsc_make_object(filename, objects, save_type="none",resolution=50, layers = 1, tilediff = 200, mode="laser", overwrite=True, start = 1.5, render=True):
    filename_test = filename.replace(".scad",".png")
    if overwrite or not os.path.exists(filename_test):
        set_mode(mode)
        save_type = save_type.lower()
        path = os.path.dirname(filename)
        if not os.path.exists(path) and path != "":
            os.makedirs(path)
        final_object = opsc_get_object(objects, mode = mode)
        # Save the final object to the specified filename    
        #file_header = """$fn = %s;
#use <MCAD/involute_gears.scad>
#"""
        file_header = "$fn = %s;"
        scad_render_to_file(final_object, filename, file_header=file_header % resolution, include_orig_code=False)
        if save_type == "all":
            saveToAll(filename, render=render)
        elif save_type == "dxf":
            saveToDxf(filename)
        if mode == "laser":
            filename_laser = filename.replace(".scad","_flat.scad")
            scad_render_to_file(getLaser(final_object, layers=layers, tilediff=tilediff, start = start), filename_laser, file_header='$fn = %s;' % resolution, include_orig_code=False) 
            if save_type == "all":
                saveToAll(filename_laser, render=render)
            elif save_type == "dxf" or save_type == "laser":
                saveToDxf(filename_laser)
            
    else:
        print("File already exists: " + filename)

def opsc_get_object(objects, mode = "laser"):
    # Create the solidpython objects only include the positive objects and if they don't have inclusion or their inclusion is either all or mode
    # Initialize an empty list to store the results
    
    
    # objects is a list of dicts, but might also contain lists please flatten it so its a single dimension list of dicts please check recursively
    
    #do it 4 times
    pass
    for i in range(8):
        objects_2 = []
        for obj in objects:
            # use recursion
            if isinstance(obj, dict):
                objects_2.append(obj)
            elif isinstance(obj, list):
                objects_2.extend(obj)
        objects = objects_2


    ################## rotation
    positive_objects = []
    negative_objects = []
    """
    # Iterate over the "objects" list    
    for objs in objects:
        #if objs is a list put it in a list
        #unpacking in case its a list of lists
        if isinstance(objs, dict):
            objs = [objs]
            if isinstance(objs, dict):
                objs = [objs]
        for obj in objs:
        # Check if the current object has a "type" key with a value of "positive"
            if obj['type'] == 'rotation':
                # rotation tpye            
                type = obj['type']
                typetype = obj.get('typetype',"p")
                rot = obj.get('rot',"")
                if rot == "":
                    rot_x = obj.get('rot_x',0)
                    rot_y = obj.get('rot_y',0)
                    rot_z = obj.get('rot_z',0)
                    rot = [rot_x, rot_y, rot_z]
                    obj["rot"] = rot
                    obj.pop('rot_x', None)
                    obj.pop('rot_y', None)
                    obj.pop('rot_z', None)
                objects = obj.get('objects',[])
                #return_value = opsc_get_object(objects, mode = mode)
                if typetype == "p" or typetype == "positive":
                    pass
                    #positive_objects.append(return_value)
                elif typetype == "n" or typetype == "negative":
                    pass
                    #negative_objects.append(return_value)
    # Initialize an empty list to store the results
    """

    types = {}
    types["rotation"] = []
    types["positive"] = []
    types["negative"] = []
    types["positive_positive"] = []
    types["negative_negative"] = []


    for typ in types:    
        for obj in objects:
            test_type = obj.get('type',"")
            if test_type == "p":
                obj['type'] = "positive"
            elif test_type == "n":
                obj['type'] = "negative"           
            
            if obj['type'] == typ:
                inclusion = obj.get('inclusion',"all")
                if inclusion == "all" or inclusion == mode:
                    if typ != "rotation":
                        opsc_item = get_opsc_item(obj)
                        types[typ].append(opsc_item)
                    else:
                        typtyp = obj.get('typetype',"p")
                        objects_2 = obj.get('objects',[])
                        pos = copy.deepcopy(obj.get('pos',[0,0,0]))
                        rot = obj.get('rot',"")
                        pass
                        # expand object list
                        for i in range(8):
                            objects_3 = []
                            for obj in objects_2:
                                # use recursion
                                if isinstance(obj, dict):
                                    objects_3.append(obj)
                                elif isinstance(obj, list):
                                    objects_3.extend(obj)
                            objects_2 = objects_3

                        #for obj in objects_2:
                        #    obj["type"] = "p"


                        opsc_objects = opsc_get_object(objects_2, mode = mode)
                        
                        if rot == "":
                            rot_x = obj.get('rot_x',0)
                            rot_y = obj.get('rot_y',0)
                            rot_z = obj.get('rot_z',0)
                            rot = [rot_x, rot_y, rot_z]
                            obj["rot"] = rot
                            obj.pop('rot_x', None)
                            obj.pop('rot_y', None)
                            obj.pop('rot_z', None)
                        opsc_objects = translate(pos)(rotate(a=rot)((opsc_objects)))
                        if typtyp == "p" or typtyp == "positive":
                            types["positive"].append(opsc_objects)
                        elif typtyp == "n" or typtyp == "negative":
                            types["negative"].append(opsc_objects)

    for typ in types:
        for obj in types[typ]:
            #remove any None
            if obj == None:
                types[typ].remove(obj)
                print("removed None")
            
        
    positive_object = union()(*types["positive"])
    # Union the negative objects
    negative_object = union()(*types["negative"])
    # Create the final object by subtracting the negative objects from the positive objects
    return_value = difference()(positive_object, negative_object)

    if (len(types["positive_positive"]) > 0):
        positive_positive_object = union()(*types["positive_positive"])
        return_value = union()(return_value, positive_positive_object)
    if (len(types["negative_negative"]) > 0):
        negative_negative_object = union()(*types["negative_negative"])
        return_value = difference()(return_value, negative_negative_object)
    return return_value

def get_opsc_item(params):
    # An array of function names for basic shapes
    basic_shapes = ['cube', 'sphere', 'cylinder']
    # An array of function names for other shapes
    other_shapes = ['hole', 'slot', 'slot_small', 'text_hollow', "tube", 'tray', 'rounded_rectangle', 'rounded_rectangle_extra', 'sphere_rectangle', 'countersunk', 'polyg', 'polyg_tube', 'polyg_tube_half', 'bearing', 'oring', 'vpulley', 'd_shaft', 'gear', 'pulley_gt2']

    # Convert radius to r if present, and remove radius from the params dictionary
    if 'radius' in params:
        if isinstance(params['radius'], str):
            # Use the radius_dict to map the radius string value to a numerical value
            params['r'] = radius_dict[params['radius']]
        else:
            params['r'] = params['radius']
        del params['radius']
    

    if params['shape'] in basic_shapes:
        # Remove shape and unexpected dictionary values
        allowed_keys = {'size', 'r', 'r1', 'r2', 'd', 'h', 'rw', 'rh', 'dw', 'dh'}
        shape_params = {k: v for k, v in params.items() if k in allowed_keys}

        m = params.get('m', '')
        func = globals()[params['shape']]
        return_value = get_opsc_transform(params,func(**shape_params))
        return_value = (return_value).set_modifier(m)
        return return_value
        
    elif params['shape'] == 'polygon':
        # Remove shape and unexpected dictionary values
        h  = params.get('height',"")
        if h == "":
            h  = params.get('depth',"")
        if h == "":
                h = params['h']
        allowed_keys = {'points'}
        shape_params = {k: v for k, v in params.items() if k in allowed_keys}

        m = params.get('m', '')
        func = globals()[params['shape']]
        return_value = get_opsc_transform(params,linear_extrude(h)(globals()[params['shape']](**shape_params)))
        return_value = (return_value).set_modifier(m)
        return return_value
    elif params['shape'] == 'text':        
        h  = params.get('height',params.get("h", params.get("depth", 10)))
        center = params.get('center', False)
        if center:
            params['halign'] = 'center'
            params['valign'] = 'center'
        allowed_keys = {'text', 'size', 'font', 'halign', 'valign', 'spacing', 'direction', 'language', 'script'}
        shape_params = {k: v for k, v in params.items() if k in allowed_keys}
        m = params.get('m', '')
        func = globals()[params['shape']]
        if h != 0:
            return_value = get_opsc_transform(params,linear_extrude(h)(globals()[params['shape']](**shape_params)))
        else:
            return_value = get_opsc_transform(params,globals()[params['shape']](**shape_params))
        return_value = (return_value).set_modifier(m)
        #strip translations away if they are
        return return_value
        
    # If the object type is not a basic shape, check if it's a defined object or one of the other shapes
    elif params['shape'] in other_shapes:
        p2 = copy.deepcopy(params)
        p2["pos"] = [0,0,0]
        return get_opsc_transform(params,globals()[params['shape']](p2))

def get_opsc_transform(params, solid_obj):
    # Rotate the object based on the 'rot' field in the params dictionary, or the 'rotX', 'rotY', and 'rotZ' fields if 'rot' is not present
    col = params.get('color', "")
    rot = params.get('rot', [])
    if rot:
        rotX, rotY, rotZ = rot
    else:
        rotX = params.get('rotX', 0)
        rotY = params.get('rotY', 0)
        rotZ = params.get('rotZ', 0)
    rotation = [rotX, rotY, rotZ]
    if rotation != [0, 0, 0]:
        solid_obj = rotate(rotation)(solid_obj)

    # Translate the object based on the 'pos' field in the params dictionary, or the 'x', 'y', and 'z' fields if 'pos' is not present
    pos = params.get('pos', [])
    if pos:
        x, y, z = pos
    else:
        x = params.get('x', 0)
        y = params.get('y', 0)
        z = params.get('z', 0)
    translation = [x, y, z]
    if translation != [0, 0, 0]:
        solid_obj = translate(translation)(solid_obj)
    if col != "":
        solid_obj = color(c=col)(solid_obj)
    return solid_obj


import random

def opsc_easy_array(type, shape, repeats, pos_start, shift_arr, **kwargs):
    for i in range(0,3):
        repeats.append(1)
        pos_start.append(0)
        shift_arr.append(0)
    return_objects = []

    for x in range(0,repeats[0]):
        for y in range(0,repeats[1]):
            for z in range(0,repeats[2]):
                return_objects.append(opsc_easy(type, shape, pos=[pos_start[0]+x*shift_arr[0],pos_start[1]+y*shift_arr[1],pos_start[2]+z*shift_arr[2]], **kwargs))
    return return_objects                

def opsc_easy(type, shape, **kwargs):
    obj = {
        'type': type,
        'shape': shape
    }
    params_allowed = []
    params_base = ['color','center','comment','size', 'r', 'radius', 'r1', 'r2', 'd', 'h', 'rw', 'rh', 'dw', 'dh', 'pos', 'x', 'y', 'z', 'rot', 'rotX', 'rotY', 'rotZ', "w", "inclusion", 'sides', 'height', 'width', "m", "id", "od", "depth", "exclude_clearance", "clearance", "points","text","valign","halign","font","inset","wall_thickness","extra","wall_thickness", "loc", "objects"]
    params_allowed.extend(params_base)
    params_gear = ['number_of_teeth', 'circular_pitch', 'diametral_pitch', 'pressure_angle', 'clearance', 'gear_thickness', 'rim_thickness', 'rim_width', 'hub_thickness', 'hub_diameter', 'bore_diameter', 'circles', 'backlash', 'twist', 'involute_facets', 'flat']
    params_allowed.extend(params_gear)
    for param in params_allowed:
        if param in kwargs:
            obj[param] = kwargs[param]
    return obj

def hole(params):
    try:
        params["r"] = params["r"]
    except:
        params["r"] = params["radius"]
    
    p2 = copy.deepcopy(params) 

    # Check if the radius is a string and replace it with the corresponding value from the dictionary
    if isinstance(p2['r'], str):
        p2['r'] = radius_dict[p2['r']]
    
    # Set the height to 100 if not specified
    if 'h' not in p2:
        p2['h'] = 100
        p2["pos"] = [0,0,-50]
    p2["center"] = True
    # Create the cylinder object
    p2["shape"] = "cylinder"
    p2["type"] = "positive"

    return get_opsc_item(p2)

def tube(params):
    try:
        params["r"] = params["r"]
    except:
        params["r"] = params["radius"]
    p2 = copy.deepcopy(params)  
    # Check if the radius is a string and replace it with the corresponding value from the dictionary
    if isinstance(p2['r'], str):
        p2['r'] = radius_dict[p2['r']]
    
    # Set the height to 100 if not specified
    if 'h' not in p2:
        if 'height' in p2:
            p2['h'] = p2['height']
        elif 'depth' in p2:
            p2['h'] = p2['depth']
        else:
            p2['h'] = 100
            p2["pos"] = [0,0,-50]
    p2["center"] = True
    # Create the cylinder object
    p2["shape"] = "cylinder"
    p2["type"] = "negative"
    inside = get_opsc_item(p2) 
    p2 = copy.deepcopy(p2)
    p2["type"] = "positive"
    p2["r"] = p2["r"] + p2["wall_thickness"]    
    outside = get_opsc_item(p2)
    return difference()(outside,inside)

def gear(params):
    default = True
    if default:
        number_of_teeth = params.get("number_of_teeth", 24)
        circular_pitch = params.get("circular_pitch", False) # couldn't figure this one out
        diametral_pitch = params.get("diametral_pitch", 0.533333) #(teeth / diameter mm) gear 15 mm wide has 8 teeth
        pressure_angle = params.get("pressure_angle", 20) #internet thinks legos is about 20
        clearance = params.get("clearance", 0.5)
        gear_thickness = params.get("gear_thickness", None)
        if gear_thickness == None:
            gear_thickness = params.get("depth", 10)
        rim_thickness = params.get("rim_thickness", gear_thickness)
        rim_width = params.get("rim_width", 0)
        hub_thickness = params.get("hub_thickness", 0)
        hub_diameter = params.get("hub_diameter", 0)
        bore_diameter = params.get("bore_diameter", 0)
        circles = params.get("circles", 0)
        backlash = params.get("backlash", 0.5)
        twist = params.get("twist", 0)
        involute_facets = params.get("involute_facets", 0)
        flat = params.get("flat", False)
    else:
        number_of_teeth = params.get("number_of_teeth", 24)
        circular_pitch = params.get("circular_pitch", False) # couldn't figure this one out
        diametral_pitch = params.get("diametral_pitch", 0.533333) #(teeth / diameter mm) gear 15 mm wide has 8 teeth
        pressure_angle = params.get("pressure_angle", 35) #internet thinks legos is about 20
        clearance = params.get("clearance", 0.5)
        gear_thickness = params.get("gear_thickness", None)
        if gear_thickness == None:
            gear_thickness = params.get("depth", 10)
        rim_thickness = params.get("rim_thickness", gear_thickness)
        rim_width = params.get("rim_width", 0)
        hub_thickness = params.get("hub_thickness", 0)
        hub_diameter = params.get("hub_diameter", 0)
        bore_diameter = params.get("bore_diameter", 0)
        circles = params.get("circles", 0)
        backlash = params.get("backlash", 0.5)
        twist = params.get("twist", 0)
        involute_facets = params.get("involute_facets", 0)
        flat = params.get("flat", False)

    involute_gear = import_scad("MCAD/involute_gears.scad")

    return involute_gear.gear(number_of_teeth=number_of_teeth, circular_pitch=circular_pitch, diametral_pitch=diametral_pitch, pressure_angle=pressure_angle, clearance=clearance, gear_thickness=gear_thickness, rim_thickness=rim_thickness, rim_width=rim_width, hub_thickness=hub_thickness, hub_diameter=hub_diameter, bore_diameter=bore_diameter, circles=circles, backlash=backlash, twist=twist, involute_facets=involute_facets, flat=flat)

def countersunk(params):
    p2 = copy.deepcopy(params)
    counter_rad = p2['r']
    p2['r'] = radius_dict[p2['r']]
    hp = copy.deepcopy(p2)
    hp["type"] = "positive"
    hp["shape"] = "hole"
    del hp["rot"]
    hol = get_opsc_item(hp)
    
    cp = copy.deepcopy(p2)
    cp["h"] = countersunk_dict[counter_rad]["height"]
    cp["r2"] = countersunk_dict[counter_rad]["little_rad"]
    cp["r1"] = countersunk_dict[counter_rad]["big_rad"]
    del cp["r"]
    del cp["rot"]
    cp["type"] = "positive"
    cp["shape"] = "cylinder"
    cp["pos"] = [0,0,0]

    top = get_opsc_item(cp)
    return union()(hol,top)

def d_shaft(kwargs):
    
    #p2["m"] = "#"
    radius = kwargs.get("radius", kwargs.get("r", ""))
    id = kwargs.get("id", "") #the radius of the d side
    depth = kwargs.get("depth", kwargs.get("h", ""))
    typ = kwargs.get("type", kwargs.get("t", "positive"))
    pos = kwargs.get("pos", [0,0,0])
    typ_other = ""
    #if typ = negative make it n
    if typ == "negative":
        typ = "n"
    if typ == "positive":
        typ = "p"
    if typ == "n":
        typ_other = "p"
    if typ == "p":
        typ_other = "n"
    if typ == "pp":
        typ_other = "nn"
    if typ == "nn":
        typ_other = "pp"
    


    shaft = copy.deepcopy(kwargs) 
    shaft["shape"] = "cylinder"
    shaft["h"] = depth
    shaft["r"] = radius
    pos_shift = [0,0,-depth]
    shaft["pos"]  = [pos[0] + pos_shift[0], pos[1] + pos_shift[1], pos[2] + pos_shift[2]]
    shaft["type"] = typ
    shaft_shape = get_opsc_item(shaft)

    indent = copy.deepcopy(kwargs) 
    indent["shape"] = "cube"
    indent.pop("r","")
    dif = radius*2-(id)
    width = radius*2
    height = dif
    depth = depth
    indent["size"] = [width,height,depth]
    pos1 = copy.deepcopy(pos)
    pos1[0] += -radius
    pos1[1] += radius - dif
    pos1[2] += -depth
    indent["pos"]  = pos1
    indent["type"] = typ_other
    #indent["m"] = "#"
    indent_shape = get_opsc_item(indent)    

    return difference()(shaft_shape, indent_shape)

def slot_small(params):  
    p2 = copy.deepcopy(params) 
    if isinstance(p2['r'], str):
        p2['r'] = radius_dict[p2['r']]
    p2["type"] = "positive"
    p2["shape"] = "hole"
    try:
        del p2["rot"]
    except:
        pass
    p2["pos"] = [0,0,0]
    left = copy.deepcopy(p2)
    right = copy.deepcopy(p2)
    left["pos"][0] = p2["w"] / 2 
    
    right["pos"][0] = -p2["w"] / 2
    pass
    leftObj = get_opsc_item(left)
    rightObj = get_opsc_item(right)
    return hull()(leftObj, rightObj)

def slot(params):  
    p2 = copy.deepcopy(params) 
    if isinstance(p2['r'], str):
        p2['r'] = radius_dict[p2['r']]
    p2["type"] = "positive"
    p2["shape"] = "hole"
    try:
        del p2["rot"]
    except:
        pass
    p2["pos"] = [0,0,0]
    left = copy.deepcopy(p2)
    right = copy.deepcopy(p2)
    left["pos"][0] = p2["w"] / 2 - p2["r"] 
    
    right["pos"][0] = -p2["w"] / 2 + p2["r"] 
    pass
    leftObj = get_opsc_item(left)
    rightObj = get_opsc_item(right)
    return hull()(leftObj, rightObj)

def pulley_gt2(params):
    number_of_teeth = params.get("number_of_teeth", 24)
    depth = params.get("depth", 6)
    pulley_gt2_scad = import_scad("pulley_gt2.scad")

    return pulley_gt2_scad.pulley_gt2(number_of_teeth=number_of_teeth, depth=depth)

def rounded_rectangle(params): 
    m = params.get("m", "")  
    p2 = copy.deepcopy(params) 
    p2["m"] = ""
    p2["h"] = p2["size"][2]
    p2["pos"] = p2.get("pos", [0, 0, 0]) 
    p2["type"] = "positive"
    p2["shape"] = "hole"
    p2["pos"] = [0,0,0]
    
    if 'rot' in p2:
        del p2["rot"]   
    if 'r' not in p2:
        p2["r"] = 5 
    tl = copy.deepcopy(p2)
    tr = copy.deepcopy(p2)
    bl = copy.deepcopy(p2)
    br = copy.deepcopy(p2)
    tl["pos"][0] = -(p2["size"][0] - p2["r"]*2)/2
    tl["pos"][1] = (p2["size"][1] - p2["r"]*2)/2
    tr["pos"][0] = (p2["size"][0] - p2["r"]*2)/2
    tr["pos"][1] = (p2["size"][1] - p2["r"]*2)/2
    bl["pos"][0] = -(p2["size"][0] - p2["r"]*2)/2
    bl["pos"][1] = -(p2["size"][1] - p2["r"]*2)/2
    br["pos"][0] = (p2["size"][0] - p2["r"]*2)/2
    br["pos"][1] = -(p2["size"][1] - p2["r"]*2)/2
    del tl["size"]
    del tr["size"]
    del bl["size"]
    del br["size"]
    tlo = get_opsc_item(tl)
    tro = get_opsc_item(tr)
    blo = get_opsc_item(bl)
    bro = get_opsc_item(br)    
    return hull()(tlo, tro, blo, bro).set_modifier(m)


def tray(params):
    wall_thickness = params.get("wall_thickness", 1)
    #see if size is there is not then set to width height depth_mm
    try:
        params["size"] = params["size"]
    except:
        params["size"] = [params["width"], params["height"], params["depth"]]
        del params["width"]
        del params["height"]
        del params["depth"]

    radius =   params.get("radius", 5)
    
    outside = rounded_rectangle(params)
    p2 = copy.deepcopy(params)
    inside_radius = radius - wall_thickness/2
    p2["r"] = inside_radius
    #remove wall thickness from size
    p2["size"][0] = p2["size"][0] - wall_thickness
    p2["size"][1] = p2["size"][1] - wall_thickness
    p2["size"][2] = p2["size"][2] + 100    
    inside = sphere_rectangle(p2)

    return difference()(outside, translate([0,0,wall_thickness/2])(inside))

def rounded_rectangle_extra(params): 
    m = params.get("m", "")

    inset = params.get("inset", 0)
    radius = params.get("r", 5)
    rotY = params.get("rotY", 0)
    params.pop("r")    
    
    params["r1"] = radius
    params["r2"] = radius - inset/2
    change = params["r1"]
    if rotY == 180:        
        params["r2"] = radius
        params["r1"] = radius - inset/2
        change = params["r2"]


    p2 = copy.deepcopy(params) 
    p2["m"] = ""
    p2["h"] = p2["size"][2]
    p2["pos"] = p2.get("pos", [0, 0, 0]) 
    p2["type"] = "positive"
    p2["shape"] = "cylinder"
    p2["pos"] = [0,0,0]
    
    if 'rot' in p2:
        del p2["rot"]   
    
    tl = copy.deepcopy(p2)
    tr = copy.deepcopy(p2)
    bl = copy.deepcopy(p2)
    br = copy.deepcopy(p2)
    tl["pos"][0] = -(p2["size"][0] - change*2)/2
    tl["pos"][1] = (p2["size"][1] - change*2)/2
    tr["pos"][0] = (p2["size"][0] - change*2)/2
    tr["pos"][1] = (p2["size"][1] - change*2)/2
    bl["pos"][0] = -(p2["size"][0] - change*2)/2
    bl["pos"][1] = -(p2["size"][1] - change*2)/2
    br["pos"][0] = (p2["size"][0] - change*2)/2
    br["pos"][1] = -(p2["size"][1] - change*2)/2
    del tl["size"]
    del tr["size"]
    del bl["size"]
    del br["size"]
    tlo = get_opsc_item(tl)
    tro = get_opsc_item(tr)
    blo = get_opsc_item(bl)
    bro = get_opsc_item(br)    
    return hull()(tlo, tro, blo, bro).set_modifier(m)



def sphere_rectangle(params): 
    m = params.get("m", "")  
    
    
    #radius
    if 'rot' in params:
        del params["rot"]   
    if 'r' not in params:
        params["r"] = 5 
    
    p2 = copy.deepcopy(params) 


    

    height = p2["size"][2]
    radius = p2["r"]
    p2["m"] = ""
    p2["h"] = height-radius*2
    p2["pos"] = p2.get("pos", [0, 0, 0]) 
    p2["type"] = "positive"
    p2["shape"] = "hole"
    p2["pos"] = [0,0,radius]
    
    p3 = copy.deepcopy(params)
    radius = p3["r"]
    p3["m"] = ""    
    p3["pos"] = p3.get("pos", [0, 0, 0]) 
    p3["type"] = "positive"
    p3["shape"] = "sphere"
    p3["pos"] = [0,0,radius]
    
    p4 = copy.deepcopy(params)
    radius = p4["r"]
    p4["m"] = ""    
    p4["pos"] = p4.get("pos", [0, 0, 0]) 
    p4["type"] = "positive"
    p4["shape"] = "sphere"
    #p4["m"] = "#"
    p4["pos"] = [0,0,height-radius]
    

    tls = [copy.deepcopy(p2), copy.deepcopy(p3), copy.deepcopy(p4)]
    trs = [copy.deepcopy(p2), copy.deepcopy(p3), copy.deepcopy(p4)]
    bls = [copy.deepcopy(p2), copy.deepcopy(p3), copy.deepcopy(p4)]
    brs = [copy.deepcopy(p2), copy.deepcopy(p3), copy.deepcopy(p4)]

    for tl in tls:     
        tl["pos"][0] = -(p2["size"][0] - p2["r"]*2)/2
        tl["pos"][1] = (p2["size"][1] - p2["r"]*2)/2
        del tl["size"]
    
    for tr in trs:
        tr["pos"][0] = (p2["size"][0] - p2["r"]*2)/2
        tr["pos"][1] = (p2["size"][1] - p2["r"]*2)/2
        del tr["size"]
    
    for bl in bls:
        bl["pos"][0] = -(p2["size"][0] - p2["r"]*2)/2
        bl["pos"][1] = -(p2["size"][1] - p2["r"]*2)/2
        del bl["size"]
    
    for br in brs:
        br["pos"][0] = (p2["size"][0] - p2["r"]*2)/2
        br["pos"][1] = -(p2["size"][1] - p2["r"]*2)/2
        del br["size"]

    
    tlo = []
    for tl in tls:
        tlo.append(get_opsc_item(tl))
    tlo = union()(tlo)
    tro = []
    for tr in trs:
        tro.append(get_opsc_item(tr))
    tro = union()(tro)
    blo = []
    for bl in bls:
        blo.append(get_opsc_item(bl))
    blo = union()(blo)
    bro = []
    for br in brs:
        bro.append(get_opsc_item(br))
    bro = union()(bro)

    #return tlo.set_modifier(m)

    return hull()(tlo, tro, blo, bro).set_modifier(m)



def bearing(params):
    p2 = copy.deepcopy(params) 
    #p2["m"] = "#"
    id = params["id"]
    od = params["od"]
    pos = params["pos"]
    depth = params["depth"]
    clearance_original = params.get("clearance", 2)

    p2["shape"] = "cylinder"
    p2["h"] = depth
    main_inner = copy.deepcopy(p2)
    main_inner["r"] = id
    main_outer = copy.deepcopy(p2)
    main_outer["r"] = od
    
    ## Extra clearance
    p2["h"] = 100
    p2["pos"] = [pos[0], pos[1], pos[2] - 50]
    extra_inner = copy.deepcopy(p2)
    extra_outer = copy.deepcopy(p2)

    clearance = (od - id - clearance_original/2 )
    exclude_clearance = params.get("exclude_clearance", False)

    
    extra_inner["r"] = id + clearance/2
    extra_outer["r"] = od - clearance/2

    mi = get_opsc_item(main_inner)
    mo = get_opsc_item(main_outer)
    
    eo = get_opsc_item(extra_outer)

    if not exclude_clearance:        
        ei = get_opsc_item(extra_inner)
        if id > 10: # make sure middle remains
            shape = translate([0,0,-depth/2])(union()(difference()(mo,mi), difference()(eo,ei)))
        else: #no need for middle on smaller bearings
            shape = translate([0,0,-depth/2])(union()(difference()(mo,mi), difference()(eo)))
    else:
        ex = 4
        extra_inner["h"] = depth+ex
        extra_inner["pos"] = [pos[0], pos[1], pos[2] - ex/2]
        ei = get_opsc_item(extra_inner)
        shape = translate([0,0,-depth/2])(mo, ei)
    return shape



    return get_opsc_item(p2)

def oring(params):
    p2 = copy.deepcopy(params) 
    id = params["id"]
    depth = params["depth"]    

    p2["shape"] = "cylinder"
    p2["h"] = depth

    rot_rad = id + depth/2
    rv = rotate_extrude(angle=360)(translate([rot_rad,0,0])(circle(r=depth/2)))

    return rv

def vpulley(params):
    id = params["id"]     

    b_y = 0
    b_x = 3.6
    t_y = 23
    t_x = 12
    points = []
    points.append([b_x, b_y])
    points.append([t_x, t_y])
    points.append([-t_x, t_y])
    points.append([-b_x, b_y])

    rot_rad = id
    shape = rotate([0,0,-90])(polygon(points=points))
    rv = rotate_extrude(angle=360)(translate([rot_rad,0,0])(shape))

    return rv    

def polyg_tube(params):
    p2 = copy.deepcopy(params)
    p2["r"] = p2["r1"]
    p2["type"] = "positive"
    outer_tube = polyg(p2)
    p2 = copy.deepcopy(params)
    p2["r"] = p2["r2"]
    p2["type"] = "negative"
    inner_tube = polyg(p2)
    return get_opsc_transform(params,difference()(outer_tube,inner_tube))

def polyg_tube_half(params):
    p2 = copy.deepcopy(params)
    
    keys = ["pos", "rotX", "rotY", "rotZ"]
    # remove all keys in key from p2
    for key in keys:
        if key in p2:
            del p2[key]

    
    item = polyg_tube(p2)
    width = p2.get("r1", 10) *2 
    height = p2.get("r1", 10)
    depth = p2.get("depth", 10)
    size = [width, height, depth]
    cut_cube = translate([0,height/2,depth/2])(cube(size=size, center=True))
    #cut difference away cube
    item = difference()(item,cut_cube)
    #item = get_opsc_transform(params,item)
    return item




def polyg(params):
    p2 = copy.deepcopy(params)
    p2.pop("rot", "")    
    p2.pop("rotX", "")   
    p2.pop("rotY", "")   
    p2.pop("rotZ", "")   
    p2["type"] = "positive"
    p2["shape"] = "polygon"
    p2["pos"] = [0,0,0]
    sides = p2.get("sides", 6)
    radius = p2["r"]    
    angles = [i * 360 / sides for i in range(sides)]
    points = regular_polygon(sides, radius)
    
    p2["points"] = points
    return get_opsc_item(p2)

import math

def regular_polygon(num_sides, radius):
    # Calculate the angle between each side
    angle = 2 * math.pi / num_sides

    # Calculate the points of the polygon
    points = []
    for i in range(num_sides):
        x = radius * math.cos(i * angle)
        y = radius * math.sin(i * angle)
        points.append((x, y))
    return points

def text_hollow(params):
    wall_thickness = params.get("wall_thickness", 0.5)
    extra = params.get("extra", "")
    params["shape"] = "text"
    p2 = copy.deepcopy(params)
    text_big = get_opsc_item(p2)    
    p2 = copy.deepcopy(params)
    little_text = text(text=p2["text"], size=p2["size"], font=p2["font"], halign=p2["halign"], valign=p2["valign"])
    little_text = offset(r=-wall_thickness)(little_text)
    little_text = linear_extrude(p2["height"]-wall_thickness)(little_text)
    #move z down wall_thickness in p2
    p2["pos"][2] = p2["pos"][2] - wall_thickness
    if extra == "reverse":
        p2["pos"][2] = p2["pos"][2] + wall_thickness * 2
    little_text = get_opsc_transform(p2,little_text)
    return difference()(text_big, little_text)


def import_scad_object(filename):
    # Import the .scad file and convert it to a solidpython object
    #filename = "parts"
    obj = import_scad(filename)
    return obj.main()



import os
import solid as solidpython



import random

def test(num_objects):
    objects = []
    for i in range(num_objects):
        # Choose a random shape
        #shape = random.choice(['cube', 'sphere', 'cylinder', 'hole', 'slot', "rounded_rectangle"])
        shape = random.choice(["rounded_rectangle"])

        # Choose a random type
        type = random.choice(['positive', 'negative'])
        
        # Create an empty object dictionary
        obj = {'shape': shape, 'type': type}
        
        # Set shape-specific parameters
        if obj['shape'] in ['cube']:
            obj['size'] =  [random.uniform(5, 15), random.uniform(5, 15), random.uniform(5, 15)]
        if obj['shape'] in ['rounded_rectangle']:
            obj['size'] =  [random.uniform(5, 15), random.uniform(5, 15), random.uniform(5, 15)]
            obj['r'] = random.uniform(0.5, 5)
        elif obj['shape'] == 'sphere':
            obj['r'] = random.uniform(5, 15)
        elif obj['shape'] in ['cylinder', 'hole']:
            obj['r'] = random.uniform(0.5, 5)
            obj['h'] = random.uniform(5, 15)
        elif obj['shape'] == 'slot':
            obj['r'] = random.uniform(0.5, 5)
            obj['h'] = random.uniform(5, 15)
            obj['w'] = random.uniform(5, 15)
        
        # Set a random position and rotation
        obj['pos'] = [random.uniform(-20, 20), random.uniform(-20, 20), random.uniform(-20, 20)]
        obj['rot'] = [random.uniform(-180, 180), random.uniform(-180, 180), random.uniform(-180, 180)]
        
        # Add the object to the list
        objects.append(obj)
    return objects

def save_to_all(fileIn, render=True):
    saveToAll(fileIn, render=render)
def saveToAll(fileIn, render=True):
    saveToFileAll(fileIn, render=render)

def save_to_dxf(fileIn, fileOut="", copy_to_laser=True):
    saveToDxf(fileIn, fileOut=fileOut, copy_to_laser=copy_to_laser)
def saveToDxf(fileIn, fileOut="", copy_to_laser=True):
    if fileOut == "":
        fileOut = fileIn.replace(".scad",".dxf")
    saveToFile(fileIn, fileOut)

def save_to_png(fileIn, fileOut=""):
    saveToPng(fileIn, fileOut=fileOut)    
def saveToPng(fileIn, fileOut="",extra="--render"):
    if fileOut == "":
        fileOut = fileIn.replace(".scad",".png")
    saveToFile(fileIn, fileOut)

def save_to_stl(fileIn, fileOut=""):
    saveToStl(fileIn, fileOut=fileOut)
def saveToStl(fileIn, fileOut=""):
    if fileOut == "":
        fileOut = fileIn.replace(".scad",".stl")
    saveToFile(fileIn, fileOut)
    
def save_to_svg(fileIn, fileOut=""):
    saveToSvg(fileIn, fileOut=fileOut)
def saveToSvg(fileIn, fileOut=""):
    if fileOut == "":
        fileOut = fileIn.replace(".scad",".svg")
    saveToFile(fileIn, fileOut)

def save_to_file(fileIn, fileOut,extra=""):
    saveToFile(fileIn, fileOut,extra="")
def saveToFile(fileIn, fileOut,extra=""):
    launchStr = f'openscad -o {fileOut} "{extra}" {fileIn}'
    if ".png" in fileOut:
        launchStr = launchStr + " --render"
    print(f"saving to file: {launchStr}")
    os.system(launchStr)    

def save_to_file_all(fileIn, extra="", render=True):
    saveToFileAll(fileIn, extra=extra, render=render)
def saveToFileAll(fileIn, extra="", render=True):
    #extra = extra + " --colorscheme Tomorrow"
    
    launch_strings = []
    #add openscad
    launch_strings.append("openscad")
    if render:
        launch_strings.append(f'--render')
    formats = ["dxf","png","svg","stl"]
    
    format_string = ""
    for f in formats:
        file_out = fileIn.replace(".scad","."+f)
        format_string = f'{format_string} -o "{file_out}"'
        #add format string to launch string
        launch_strings.append(f"-o")
        launch_strings.append(f'{file_out}')
                          
    launch_strings.append(f'{fileIn}')
                          
    launchStr = " ".join(launch_strings)
    print(f"saving to file all: {launchStr}")
    #if fileout folder doesn't exist, create it
    path = os.path.dirname(file_out)
    if not os.path.exists(path) and path != "":
        os.makedirs(path)
    os.system(launchStr)

def getLaser(final_object,start=1.5,layers=1,thickness=3,tilediff=200):
        rv= []
        for x in range(int(layers)):
            rv.append(translate([0,x*tilediff,0])(
                    projection()(
                        intersection()(translate([-500,-500,start+x*thickness])(cube(size=[1000,1000,0.1])),
                            final_object
                        )
                    )
                )
            )            
        return union()(rv)

set_mode("laser")

