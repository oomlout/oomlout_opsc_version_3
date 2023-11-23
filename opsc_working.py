import opsc




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

objects = []
#objects.append({'shape': 'cube', 'type': 'positive', 'size': [10,5,23]})
#objects.append({'shape': 'gear', 'type': 'positive', 'size': [10,5,23]})
objects.append({'shape': 'pulley_gt2', 'type': 'positive', 'number_of_teeth': 20, 'depth': 2})


#objects = opsc.test(20)

opsc.opsc_make_object('outputs/my_object.scad', objects, save_type="all")

