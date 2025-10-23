TILE_SIZE = 50

# # = Wall
# . = Empty
# P = Player Spawn
# E = Criminals Spawn
# T = Police Spawn

MAP_LAYOUT = [
    "##############################################",
    "#P T                                       E #",
    "# T                                       E E#",
    "#                                            #",
    "#T T                                      E E#",
    "#                                            #",
    "#   #####      ######################      # #",
    "#   #                                    #   #",
    "#   #          #                #          # #",
    "#              #                #            #",
    "#              #                #            #",
    "#   #          #                #          # #",
    "#   #                                    #   #",
    "#   #####      ######################      # #",
    "#                                            #",
    "#                                            #",
    "#                                            #",
    "#                                            #",
    "#                                            #",
    "##############################################",
]

MAP_WIDTH = len(MAP_LAYOUT[0]) * TILE_SIZE
MAP_HEIGHT = len(MAP_LAYOUT) * TILE_SIZE