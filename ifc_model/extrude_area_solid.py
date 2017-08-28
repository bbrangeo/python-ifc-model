from .representation_item import RepresentationItem
from .arbitrary_closed_profile_def import ArbitraryClosedProfileDef
from .arbitrary_profile_def_with_voids import ArbitraryProfileDefWithVoids
from .rectangle_profile_def import RectangleProfileDef
from .i_shape_profile_def import IShapeProfileDef
from .circle_profile_def import CircleProfileDef

class ExtrudedAreaSolid(RepresentationItem):
    def __init__(self, repr):
        self.repr = repr
        self.type = 'ExtrudedAreaSolid'

    def area_from_class(self, name):
        classes = {
            'ArbitraryClosedProfileDef': ArbitraryClosedProfileDef,
            'ArbitraryProfileDefWithVoids': ArbitraryProfileDefWithVoids,
            'RectangleProfileDef': RectangleProfileDef,
            'IShapeProfileDef': IShapeProfileDef,
            'CircleProfileDef': CircleProfileDef
        }
        return classes[name](self)

    def from_ifc(self, ifc_data):
        assert ifc_data.is_a('IfcExtrudedAreaSolid')
        super(ExtrudedAreaSolid, self).from_ifc(ifc_data)
        # TODO: ifc_data.Position is a Axis2Placement3D, maybe get an own class?
        self.location = ifc_data.Position.Location.Coordinates
        self.direction = [0, 0, 0]
        if ifc_data.Position.RefDirection:
            self.direction = ifc_data.Position.RefDirection.DirectionRatios
        area_type = self.ifc_data.SweptArea.is_a()
        self.depth = self.ifc_data.Depth
        self.area = self.area_from_class(area_type[3:])
        self.area.from_ifc(self.ifc_data.SweptArea)

    def from_json(self, data):
        super(ExtrudedAreaSolid, self).from_json(data)
        self.area = self.area_from_class(data['area']['type'])
        self.depth = data['depth']
        self.location = data['location']
        self.direction = data['direction']
        self.area.from_json(data['area'])

    def to_json(self):
        data = super(ExtrudedAreaSolid, self).to_json()
        data['type'] = self.type
        data['depth'] = self.depth
        data['location'] = self.location
        data['direction'] = self.direction
        data['area'] = self.area.to_json()
        return data
