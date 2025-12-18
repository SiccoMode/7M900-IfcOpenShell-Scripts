import numpy
import ifcopenshell
import ifcopenshell.api.geometry
import ifcopenshell.api.context
import ifcopenshell.api.spatial

# Loading the Ifc model and declaring a 4by4 eye matrix
model = ifcopenshell.open("Huis_zonder_footing.ifc")
matrix = numpy.eye(4)

# Writing attribute data for new instance of IfcFooting 
footing_attribute_data = {
    'GlobalId': ifcopenshell.guid.new(),
    'Name': 'Footing',
    'Description': 'Concrete Footing Substructure',
    'OwnerHistory': model.by_type("IfcOwnerHistory")[0],

}
footing = model.create_entity('IfcFooting', **footing_attribute_data)

print(footing)

context = ifcopenshell.api.context.add_context(model, context_type="Model")
body = ifcopenshell.api.context.add_context(model, context_type="Model",
    context_identifier="Body", target_view="MODEL_VIEW", parent=context)
storey = model.by_type('IfcBuildingStorey')[0]


# Footing profile and 3d geometry for the footing object. 
footing_profile = model.create_entity("IfcTShapeProfileDef", ProfileName="T-EXAMPLE", ProfileType="AREA",
    Depth=600, FlangeWidth=500, WebThickness=300, FlangeThickness=150)

representation = ifcopenshell.api.geometry.add_profile_representation(model, context=body, profile=footing_profile, depth=4.2)

# Some sub-optimal trial and error rotations
matrix = ifcopenshell.util.placement.rotation(90, "X") @ matrix
matrix = ifcopenshell.util.placement.rotation(90, "Z") @ matrix
matrix = ifcopenshell.util.placement.rotation(180, "X") @ matrix

# Coordinates of the bottom left node of the floor slab, where to place the profile for extrusion
matrix[:,3][0:3] = (-2.25, -1.6, -0.6)

ifcopenshell.api.geometry.edit_object_placement(model, matrix=matrix, product=footing)

ifcopenshell.api.geometry.assign_representation(
    model,
    product=footing,
    representation=representation,
)
ifcopenshell.api.spatial.assign_container(
    model, products=[footing], relating_structure=storey
)

# writing to new file and success statement
model.write("huis_met_footing.ifc")
print("Sim-sala-BIM!")