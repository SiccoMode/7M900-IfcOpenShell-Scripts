import ifcopenshell
import ifcopenshell.api
import ifcopenshell.api.pset
import ifcopenshell.api.root

model = ifcopenshell.open("huis_met_footing.ifc")

footing_type = ifcopenshell.api.root.create_entity(model, ifc_class="IfcFootingType")
pset = ifcopenshell.api.pset.add_pset(model, product=footing_type, name="Pset_ProgressTracker")

ifcopenshell.api.pset.edit_pset(model, pset=pset, properties={"Progress State": "completed", "Start Date": "19-11-2025", "End Date" : "18-12-2025", "Person Responsible" : "Sicco Oortwijn"})

footing = model.by_type('IfcFooting')[0]

ifcopenshell.api.pset.assign_pset(model, [footing], pset)

print(footing)

model.write("huis_met_footing.ifc")
print("Sim-Sala-BIM!")