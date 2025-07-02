# PARAMETERS_START
# {
#   "width": {"type": "number", "default": 4, "min": 1, "max": 200, "step": 1, "label": "Width (units)", "description": "Width of the block"},
#   "length": {"type": "number", "default": 2, "min": 1, "max": 200, "step": 1, "label": "Length (units)", "description": "Length of the block"},
#   "height": {"type": "number", "default": 4, "min": 1, "max": 50, "step": 1, "label": "Height (units)", "description": "Height of the block"},
# }
# PARAMETERS_END
# TODO: look at max value for parameters

def lego_brick(pip_width: int = 2, pip_depth: int = 2, unit_block_height: int = 2):
    pip_diameter = 4.8  # mm
    pip_spacing = 8.0  # mm center-to-center
    border_size = 7.8  # mm
    block_width = (pip_width - 1) * pip_spacing + border_size  # mm
    block_depth = (pip_depth - 1) * pip_spacing + border_size  # mm
    block_height = unit_block_height * 3.2  # mm
    pip_height = 1.6 + block_height  # mm
    lego = Part() + extrude(Rectangle(block_width, block_depth), amount=block_height)
    pips = Sketch() + GridLocations(
        pip_spacing, pip_spacing, pip_width, pip_depth
    ) * Circle(pip_diameter / 2)
    lego += extrude(pips, amount=pip_height)
    lego2 = offset(
        lego,
        amount=-1.2,
        openings=lego.faces().sort_by(Axis.Z)[0],
        kind=Kind.INTERSECTION,
    )
    if min((pip_width, pip_depth)) > 1:
        mid_supp = Sketch() + GridLocations(
            pip_spacing, pip_spacing, pip_width - 1, pip_depth - 1
        ) * (Circle(6.5 / 2) - Circle(4.8 / 2))
    elif min((pip_width, pip_depth)) == 1:
        mid_supp = Sketch() + Circle(3 / 2) - Circle(3 / 2 - 0.8)
    lego2 += extrude(mid_supp, amount=block_height)
    return lego2

output = [
    {"name": f"lego_brick_{width}x{length}x{height}", "part": lego_brick(width, length, height), "color": "#10b981"}
]
