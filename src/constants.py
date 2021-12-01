# project-wide constants

# screen constants
SCREEN_DIM = (800, 600)  # screen dimensions
FPS = 60  # framerate for the application
ALGO_PLAY_FRAMES = 20  # number of frames for each algorithm step

# font
FONT_SIZE = 16  # font size for all text

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)

BLUE = (66, 135, 245)
LIGHT_BLUE = (64, 199, 230)
DARK_RED = (130, 11, 0)
MED_GREEN = (32, 148, 0)

# drawing/functionality constants
BG_COLOR = WHITE  # screen background fill color

VERTEX_DEFAULT_RADIUS = 10  # size of drawn vertices (unless selected)
VERTEX_HOVER_RADIUS = 12  # distance from which a vertex will register a click
VERTEX_DEFAULT_COLOR = BLUE  # color of drawn vertices
VERTEX_HOVER_COLOR = LIGHT_BLUE  # color of selected (hovered-over) vertex

EDGE_DEFAULT_WIDTH = 2  # width of drawn edges (unless selected)
EDGE_HOVER_WIDTH = 4  # distance from which an edge will register a click
EDGE_DEFAULT_COLOR = BLACK  # color of drawn edges
EDGE_HOVER_COLOR = BLACK  # color of selected (hovered-over) edge

SUCCESS_COLOR = MED_GREEN  # color of success messages
ERROR_COLOR = DARK_RED  # color of error/failure messages

INCLUDED_EDGE_COLOR = MED_GREEN  # color of edge included in spanning tree
EXCLUDED_EDGE_COLOR = GREY  # color of edge excluded from spanning tree
CHECKING_EDGE_COLOR = LIGHT_BLUE  # color of edge being checked
