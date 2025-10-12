from Autodesk.Revit.DB import FilteredElementCollector, Wall
doc = __revit__.ActiveUIDocument.Document

collector = FilteredElementCollector(doc)
walls = collector.OfClass(Wall).ToElements()

for wall in walls:
	Name = wall.Name
	