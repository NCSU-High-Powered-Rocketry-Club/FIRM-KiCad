# Assmann WSW A-USBC-20F0-EA-GSR05  --  USB 2.0 Type-C receptacle, 16P, IPX8
# Built from drawing ASS 9424CO rev00 (sheet 1/2).
#
# Model coordinate system == KiCad model space with offset 0 / rotate 0:
#   model X = footprint X,  model Y = -footprint Y,  model Z = up, Z=0 at PCB top.
# So the port (which faces footprint +Y) points toward model -Y.
#
# Regenerate with:  freecadcmd 3dmodels/src/A-USBC-20F0-EA-GSR05.py
import os, math
import FreeCAD as App
import Part
from FreeCAD import Vector as V

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "A-USBC-20F0-EA-GSR05.step")

# ---- dimensions from the drawing (mm) --------------------------------------
STANDOFF   = 0.37      # 0.37 +/- 0.10, housing bottom above PCB
TOP        = 5.06      # overall height above PCB
CL         = 2.25      # port centreline above PCB
BODY_W     = 10.34     # metal shell width
FLANGE_W   = 10.84     # widest point (sealing flange)
NOSE_W     = 8.94      # mating shell outer width
NOSE_H     = 3.16
PORT_W     = 8.34      # 8.34 +0.06/-0.02
PORT_H     = 2.56      # 2.56 +/- 0.04
TONGUE_W   = 6.69
TONGUE_T   = 0.70

# Y positions, model frame (port at -Y, tails at +Y); datum Y=0 = locating posts
Y_NOSE_F   = -4.40     # front tip of the mating shell
Y_FLANGE_F = -2.88     # front face of the sealing flange
Y_FLANGE_R = -2.15
Y_BODY_R   =  3.05     # rear wall of the housing
Y_TAIL_F   =  3.15     # contact tails run over the land pattern ...
Y_TAIL_R   =  4.35     # ... 3.15 .. 4.35 (= 3.15/4.35 on the PCB layout)

POST_D     = 1.00      # 2-o1.00 +/-0.1, spaced 5.00 +/- 0.15
POST_X     = 2.50
POST_LEN   = 1.50      # 2-1.50

TAB_T      = 0.25      # shield tabs, into the 2.00 x 0.60 slots at +/-4.97
TAB_X      = 4.97
TAB_LEN    = 1.90
TAB_Y      = 0.38      # slot centre, model frame (footprint y = -0.38)
TAB_DROP   = 1.20

WIDE_X     = (3.165, 2.36)          # 4-0.43 contacts
WIDE_W     = 0.43
NARROW_X   = (1.75, 1.25, 0.75, 0.25)   # 8-0.20 contacts
NARROW_W   = 0.20
TAIL_T     = 0.12

BOSS_D, BOSS_H, BOSS_X, BOSS_Y = 1.40, 0.40, 2.00, 0.50


def along(edge, axis, tol=1e-6):
    """True if `edge` is a straight line running along `axis` ('X'|'Y'|'Z')."""
    if not isinstance(edge.Curve, Part.Line):
        return False
    d = edge.Curve.Direction
    want = {"X": (1, 0, 0), "Y": (0, 1, 0), "Z": (0, 0, 1)}[axis]
    return all(abs(abs(a) - b) < tol for a, b in zip((d.x, d.y, d.z), want))


def box(x0, x1, y0, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def stadium(width, height, y0, y1, zc):
    """Box of `width` x `height` in X-Z extruded along Y, ends rounded in X-Z."""
    b = box(-width / 2, width / 2, y0, y1, zc - height / 2, zc + height / 2)
    r = height / 2 - 0.02          # just shy of a true semicircle
    return b.makeFillet(r, [e for e in b.Edges if along(e, "Y")])


parts = {}

# --- metal housing ----------------------------------------------------------
body = box(-BODY_W / 2, BODY_W / 2, Y_FLANGE_R, Y_BODY_R, STANDOFF, TOP)
body = body.makeFillet(0.30, [e for e in body.Edges if along(e, "Z")])

flange = box(-FLANGE_W / 2, FLANGE_W / 2, Y_FLANGE_F, Y_FLANGE_R, STANDOFF, TOP)
flange = flange.makeFillet(0.35, [e for e in flange.Edges if along(e, "Z")])

nose = stadium(NOSE_W, NOSE_H, Y_NOSE_F, Y_FLANGE_F, CL)

shell = body.fuse(flange).fuse(nose)

# shield tabs, bent down through the PCB slots
for sx in (-1, 1):
    x = sx * TAB_X
    shell = shell.fuse(box(x - TAB_T / 2, x + TAB_T / 2,
                           TAB_Y - TAB_LEN / 2, TAB_Y + TAB_LEN / 2,
                           -TAB_DROP, STANDOFF + 0.5))

# port cavity + tongue
cav = stadium(PORT_W, PORT_H, Y_NOSE_F - 0.1, 1.20, CL)
shell = shell.cut(cav)

# stamped dimples on the top face
for sx in (-1, 1):
    shell = shell.fuse(Part.makeCylinder(BOSS_D / 2, BOSS_H,
                                         V(sx * BOSS_X, BOSS_Y, TOP), V(0, 0, 1)))
parts["shell"] = (shell, (0.72, 0.74, 0.78))          # nickel-plated steel

# --- insulator: tongue ------------------------------------------------------
tongue = stadium(TONGUE_W, TONGUE_T, -3.60, 1.20, CL)
parts["tongue"] = (tongue, (0.10, 0.10, 0.11))        # black LCP

# --- locating posts ---------------------------------------------------------
posts = None
for sx in (-1, 1):
    c = Part.makeCylinder(POST_D / 2, POST_LEN + STANDOFF,
                          V(sx * POST_X, 0.0, STANDOFF - POST_LEN), V(0, 0, 1))
    posts = c if posts is None else posts.fuse(c)
parts["posts"] = (posts, (0.10, 0.10, 0.11))

# --- contact tails ----------------------------------------------------------
tails = None
for xs, w in ((WIDE_X, WIDE_W), (NARROW_X, NARROW_W)):
    for x0 in xs:
        for sx in (-1, 1):
            x = sx * x0
            t = box(x - w / 2, x + w / 2, Y_TAIL_F, Y_TAIL_R, 0.0, TAIL_T)
            tails = t if tails is None else tails.fuse(t)
parts["tails"] = (tails, (0.85, 0.70, 0.35))          # gold flash

# ---- assemble & export -----------------------------------------------------
doc = App.newDocument("usbc")
objs = []
for name, (shape, col) in parts.items():
    o = doc.addObject("Part::Feature", name)
    o.Shape = shape
    objs.append((o, col))
doc.recompute()

bb = None
for o, _ in objs:
    bb = o.Shape.BoundBox if bb is None else bb.united(o.Shape.BoundBox)
print("bbox X %.2f..%.2f  Y %.2f..%.2f  Z %.2f..%.2f"
      % (bb.XMin, bb.XMax, bb.YMin, bb.YMax, bb.ZMin, bb.ZMax))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
coloured = False
try:
    import ImportGui
    for o, col in objs:
        o.ViewObject.ShapeColor = col
    ImportGui.export([o for o, _ in objs], OUT)
    coloured = True
except Exception as e:
    print("no colour export (%s); writing plain STEP" % type(e).__name__)
    import Import
    Import.export([o for o, _ in objs], OUT)
print("wrote", OUT, "coloured" if coloured else "plain")
