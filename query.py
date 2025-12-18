import ifcopenshell

model = ifcopenshell.open("huis_met_footing.ifc")

wall = model.by_type("IfcWall")[0]

localplacement = wall.ObjectPlacement


print(localplacement)