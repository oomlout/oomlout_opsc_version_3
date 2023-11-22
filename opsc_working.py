import opsc
import opsc_library_gen



# Define the objects to be used in the OpenSCAD object
objects = [
    {'shape': 'cube', 'type': 'positive', 'size': 10},
    {'shape': 'sphere', 'type': 'negative', 'radius': 5},
    {'shape': 'my_custom_object', 'type': 'positive', 'param1': 10, 'param2': 20},
]


objects = [
    {'shape': 'cube', 'type': 'positive', 'size': [10,5,23]},
    {'shape': 'cube', 'type': 'positive', 'pos' : [5,5,10] ,'size': [5,5,5]},
    {'shape': 'cube', 'type': 'positive', 'size': [10,5,23]},
    {'shape': 'cube', 'type': 'positive', 'size': [10,5,23]},
    {'shape': 'cube', 'type': 'positive', 'size': [10,5,23]},
    {'shape': 'sphere', 'type': 'negative', 'radius': 5},
    {'shape': 'my_custom_object', 'type': 'positive', 'param1': 10, 'param2': 20},
]




objects = opsc.test(20)

#opsc.opsc_make_object('outputs/my_object.scad', objects, save_all=True)

opsc_library_gen.gen_library({},save_file=True)