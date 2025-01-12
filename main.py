@namespace
class SpriteKind:
    camera = SpriteKind.create()
    Block = SpriteKind.create()
    image = SpriteKind.create()
# States
# 
# 0 - Main Menu
# 
# 1 - Editor
# 
# 2 - Block Select
# 
# 3 - Game
# 
# 4 - End Screen
def setupLevel():
    global selectedBlock, playerGridX, playerGridY, blockX, blockY, minBlockY, maxBlockY, minBlockX, maxBlockX, coins
    selectedBlock = 0
    if level == 1:
        playerGridX = 1
        playerGridY = 13
        blockX = 0
        blockY = 13
        minBlockY = 10
        maxBlockY = 15
        minBlockX = 0
        maxBlockX = 7
        coins = 1

def on_up_pressed():
    global blockY
    if state == 1:
        if blockY > minBlockY:
            blockY += -1
        grid.place(blockSelect, tiles.get_tile_location(blockX, blockY))
        updateBlockSelect()
    elif state == 2:
        pass
controller.up.on_event(ControllerButtonEvent.PRESSED, on_up_pressed)

def on_b_pressed():
    if state == 1:
        blockSelectMenu()
    elif state == 2:
        loadLevel()
controller.B.on_event(ControllerButtonEvent.PRESSED, on_b_pressed)

def on_a_pressed():
    if state == 1 and (blockX == playerGridX and blockY == playerGridY):
        start()
    elif state == 2:
        loadLevel()
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

def on_left_pressed():
    global blockX
    if state == 1:
        if blockX > minBlockX:
            blockX += -1
        grid.place(blockSelect, tiles.get_tile_location(blockX, blockY))
        updateBlockSelect()
    elif state == 2:
        pass
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

def loadLevel():
    global state, rob, blockSelect
    state = 1
    rob = sprites.create(assets.image("""
        rob
    """), SpriteKind.player)
    blockSelect = sprites.create(assets.image("""
        blockSelect0
    """), SpriteKind.Block)
    updateBlockSelect()
    sprites.destroy_all_sprites_of_kind(SpriteKind.image)
    tiles.set_current_tilemap(tilemap("""
        level1
    """))
    scene.set_background_image(assets.image("""
        bg
    """))
    grid.place(rob, tiles.get_tile_location(playerGridX, playerGridY))
    grid.snap(rob)
    grid.place(blockSelect, tiles.get_tile_location(blockX, blockY))
    scene.camera_follow_sprite(blockSelect)
def blockSelectMenu():
    global state, aButton
    state = 2
    sprites.destroy(rob)
    sprites.destroy(blockSelect)
    tiles.set_current_tilemap(tilemap("""
        empty
    """))
    scene.set_background_image(assets.image("""
        blockSelectScreen1a
    """))
    scene.center_camera_at(0, 0)
    aButton = sprites.create(assets.image("""
        aButton
    """), SpriteKind.image)
    aButton.set_position(67, 18)
    scaling.scale_to_percent(aButton, 70, ScaleDirection.UNIFORMLY, ScaleAnchor.MIDDLE)
    animation.run_image_animation(aButton, assets.animation("""
        buttonAnim
    """), 500, True)
def updateBlockSelect():
    global blockAvailable
    blockSelect.say_text("")
    if tiles.tile_at_location_is_wall(tiles.get_tile_location(blockX, blockY)) or tiles.tile_at_location_equals(tiles.get_tile_location(blockX, blockY),
        assets.tile("""
            lava
        """)) or (tiles.tile_at_location_equals(tiles.get_tile_location(blockX, blockY),
        assets.tile("""
            flag
        """)) or False):
        blockAvailable = 0
    else:
        blockAvailable = 1
    if blockX == playerGridX and blockY == playerGridY:
        blockSelect.set_image(assets.image("""
            blockSelect0X
        """))
        blockSelect.say_text("Go!")
    else:
        if selectedBlock == 0:
            blockSelect.set_image(assets.image("""
                blockSelect0
            """))
        elif selectedBlock == 1:
            if blockAvailable == 1:
                blockSelect.set_image(assets.image("""
                    blockSelect1
                """))
            else:
                blockSelect.set_image(assets.image("""
                    blockSelect1X
                """))

def on_right_pressed():
    global blockX
    if state == 1:
        if blockX < maxBlockX:
            blockX += 1
        grid.place(blockSelect, tiles.get_tile_location(blockX, blockY))
        updateBlockSelect()
    elif state == 2:
        pass
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def on_down_pressed():
    global blockY
    if state == 1:
        if blockY < maxBlockY:
            blockY += 1
        grid.place(blockSelect, tiles.get_tile_location(blockX, blockY))
        updateBlockSelect()
    elif state == 2:
        pass
controller.down.on_event(ControllerButtonEvent.PRESSED, on_down_pressed)

def start():
    global state
    music.stop_all_sounds()
    music.play(music.create_song(assets.song("""
            startMusic
        """)),
        music.PlaybackMode.LOOPING_IN_BACKGROUND)
    state = 3
    sprites.destroy(blockSelect)
    scene.camera_follow_sprite(rob)
    rob.ay = 500
    rob.vx = 50
blockAvailable = 0
aButton: Sprite = None
rob: Sprite = None
blockSelect: Sprite = None
state = 0
coins = 0
maxBlockX = 0
minBlockX = 0
maxBlockY = 0
minBlockY = 0
blockY = 0
blockX = 0
playerGridY = 0
playerGridX = 0
selectedBlock = 0
level = 0
scene.set_background_image(assets.image("""
    bg
"""))
level = 1
setupLevel()
loadLevel()
music.set_volume(12)
music.play(music.create_song(assets.song("""
        Music
    """)),
    music.PlaybackMode.LOOPING_IN_BACKGROUND)