@namespace
class SpriteKind:
    camera = SpriteKind.create()
    Block = SpriteKind.create()
    image = SpriteKind.create()
list2: List[number] = []
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
    global selectedBlock, blockListX, blockListY, blockListType, playerGridX, playerGridY, blockX, blockY, minBlockY, maxBlockY, minBlockX, maxBlockX, coins, itemsUnlocked
    music.stop_all_sounds()
    music.set_volume(12)
    music.play(music.create_song(assets.song("""
            Music
        """)),
        music.PlaybackMode.LOOPING_IN_BACKGROUND)
    selectedBlock = 0
    blockListX = []
    blockListY = []
    blockListType = []
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
        itemsUnlocked = 1

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

def placeBlock():
    global selectedBlock
    music.play(music.melody_playable(music.thump),
        music.PlaybackMode.IN_BACKGROUND)
    scene.camera_shake(4, 200)
    if selectedBlock == 1:
        tiles.set_tile_at(tiles.get_tile_location(blockX, blockY),
            assets.tile("""
                stone
            """))
        tiles.set_wall_at(tiles.get_tile_location(blockX, blockY), True)
        blockListType.append(1)
        blockListX.append(blockX)
        blockListY.append(blockY)
    else:
        pass
    selectedBlock = 0
    updateBlockSelect()

def on_b_pressed():
    if state == 1:
        blockSelectMenu()
    elif state == 2:
        loadLevel()
controller.B.on_event(ControllerButtonEvent.PRESSED, on_b_pressed)

def breakBlock():
    global coins
    music.play(music.melody_playable(music.thump),
        music.PlaybackMode.IN_BACKGROUND)
    scene.camera_shake(4, 200)
    index = 0
    while index <= len(blockListX):
        if blockListX[index] == blockX and blockListY[index] == blockY:
            if blockListType[index] == 1:
                coins += 1
            blockListX.remove_at(index)
            blockListY.remove_at(index)
            blockListType.remove_at(index)
            break
        index += 1
    tiles.set_tile_at(tiles.get_tile_location(blockX, blockY),
        assets.tile("""
            transparency16
        """))
    updateBlockSelect()

def on_a_pressed():
    global coins, selectedBlock
    if state == 1:
        if blockX == playerGridX and blockY == playerGridY:
            start()
        elif selectedBlock == 0:
            if tiles.tile_at_location_equals(tiles.get_tile_location(blockX, blockY),
                assets.tile("""
                    stone
                """)):
                breakBlock()
        else:
            if blockAvailable == 1:
                placeBlock()
            else:
                music.play(music.melody_playable(music.buzzer),
                    music.PlaybackMode.IN_BACKGROUND)
    elif state == 2:
        # Buy stone block
        # d
        if shopMenuSelect == 0:
            if coins >= 1:
                music.play(music.melody_playable(music.power_up),
                    music.PlaybackMode.IN_BACKGROUND)
                coins += -1
                selectedBlock = 1
                loadLevel()
            else:
                music.play(music.melody_playable(music.buzzer),
                    music.PlaybackMode.IN_BACKGROUND)
                rob.say_text("Too expensive!", 1000, False)
        else:
            pass
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
    index2 = 0
    while index2 <= len(list2):
        if blockListType[index2] == 1:
            tiles.set_tile_at(tiles.get_tile_location(blockListX[index2], blockListY[index2]),
                assets.tile("""
                    stone
                """))
            tiles.set_wall_at(tiles.get_tile_location(blockListX[index2], blockListY[index2]),
                True)
        else:
            pass
        index2 += 1
    scene.set_background_image(assets.image("""
        bg
    """))
    grid.place(rob, tiles.get_tile_location(playerGridX, playerGridY))
    grid.snap(rob)
    grid.place(blockSelect, tiles.get_tile_location(blockX, blockY))
    scene.camera_follow_sprite(blockSelect)
def blockSelectMenu():
    global state, aButton, number
    state = 2
    rob.set_position(96, 22)
    sprites.destroy(blockSelect)
    tiles.set_current_tilemap(tilemap("""
        empty
    """))
    scene.center_camera_at(0, 0)
    aButton = sprites.create(assets.image("""
        aButton
    """), SpriteKind.image)
    refreshShop()
    if coins == 0:
        number = sprites.create(assets.image("""
            0
        """), SpriteKind.image)
    elif coins == 1:
        number = sprites.create(assets.image("""
            1
        """), SpriteKind.image)
    elif coins == 2:
        number = sprites.create(assets.image("""
            2
        """), SpriteKind.image)
    number.set_position(123, 17)
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
            empty
        """))
        blockSelect.say_text("Go!")
    else:
        if selectedBlock == 0:
            if tiles.tile_at_location_equals(tiles.get_tile_location(blockX, blockY),
                assets.tile("""
                    stone
                """)):
                blockSelect.set_image(assets.image("""
                    blockSelect0X
                """))
            else:
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

def refreshShop():
    if itemsUnlocked == 1:
        if shopMenuSelect == 0:
            scene.set_background_image(assets.image("""
                blockSelectScreen1a
            """))
            aButton.set_position(67, 18)
        else:
            pass
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
number: Sprite = None
aButton: Sprite = None
rob: Sprite = None
shopMenuSelect = 0
blockAvailable = 0
blockSelect: Sprite = None
state = 0
itemsUnlocked = 0
coins = 0
maxBlockX = 0
minBlockX = 0
maxBlockY = 0
minBlockY = 0
blockY = 0
blockX = 0
playerGridY = 0
playerGridX = 0
blockListType: List[number] = []
blockListY: List[number] = []
blockListX: List[number] = []
selectedBlock = 0
level = 0
scene.set_background_image(assets.image("""
    bg
"""))
level = 1
setupLevel()
loadLevel()

def on_on_update():
    global blockX, state
    if state == 3:
        if rob.is_hitting_tile(CollisionDirection.RIGHT):
            rob.vx = -50
            rob.set_image(assets.image("""
                robLeft
            """))
        if rob.is_hitting_tile(CollisionDirection.LEFT):
            rob.vx = 50
            rob.set_image(assets.image("""
                rob
            """))
        if tiles.tile_at_location_equals(rob.tilemap_location(), assets.tile("""
            lava
        """)):
            scene.camera_shake(4, 200)
            rob.set_velocity(0, 10)
            rob.ay = 20
            sprites.destroy(rob, effects.fire, 500)
            music.stop_all_sounds()
            music.play(music.melody_playable(music.big_crash),
                music.PlaybackMode.IN_BACKGROUND)
            music.set_volume(12)
            blockX += -1
            music.play(music.create_song(assets.song("""
                    Music
                """)),
                music.PlaybackMode.LOOPING_IN_BACKGROUND)
            loadLevel()
        if tiles.tile_at_location_equals(rob.tilemap_location(), assets.tile("""
            flag
        """)):
            rob.set_velocity(rob.vx / 20, 0)
            effects.confetti.start_screen_effect(1000)
            music.stop_all_sounds()
            music.set_volume(60)
            music.play(music.melody_playable(music.magic_wand),
                music.PlaybackMode.IN_BACKGROUND)
            state = 4
    else:
        pass
game.on_update(on_on_update)
