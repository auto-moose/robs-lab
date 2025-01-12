namespace SpriteKind {
    export const camera = SpriteKind.create()
    export const Block = SpriteKind.create()
    export const image = SpriteKind.create()
}
let list: number[] = []
// States
// 
// 0 - Main Menu
// 
// 1 - Editor
// 
// 2 - Block Select
// 
// 3 - Game
// 
// 4 - End Screen
function setupLevel () {
    selectedBlock = 0
    blockListX = []
    blockListY = []
    blockListType = []
    if (level == 1) {
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
    }
}
controller.up.onEvent(ControllerButtonEvent.Pressed, function () {
    if (state == 1) {
        if (blockY > minBlockY) {
            blockY += -1
        }
        grid.place(blockSelect, tiles.getTileLocation(blockX, blockY))
        updateBlockSelect()
    } else if (state == 2) {
    	
    }
})
function placeBlock () {
    music.play(music.melodyPlayable(music.thump), music.PlaybackMode.InBackground)
    scene.cameraShake(4, 200)
    if (selectedBlock == 1) {
        tiles.setTileAt(tiles.getTileLocation(blockX, blockY), assets.tile`stone`)
        tiles.setWallAt(tiles.getTileLocation(blockX, blockY), true)
        blockListType.push(1)
        blockListX.push(blockX)
        blockListY.push(blockY)
    } else {
    	
    }
    selectedBlock = 0
    updateBlockSelect()
}
controller.B.onEvent(ControllerButtonEvent.Pressed, function () {
    if (state == 1) {
        blockSelectMenu()
    } else if (state == 2) {
        loadLevel()
    }
})
function breakBlock () {
    music.play(music.melodyPlayable(music.thump), music.PlaybackMode.InBackground)
    scene.cameraShake(4, 200)
    for (let index = 0; index <= blockListX.length; index++) {
        if (blockListX[index] == blockX && blockListY[index] == blockY) {
            if (blockListType[index] == 1) {
                coins += 1
            }
            blockListX.removeAt(index)
            blockListY.removeAt(index)
            blockListType.removeAt(index)
            break;
        }
    }
    tiles.setTileAt(tiles.getTileLocation(blockX, blockY), assets.tile`transparency16`)
    updateBlockSelect()
}
controller.A.onEvent(ControllerButtonEvent.Pressed, function () {
    if (state == 1) {
        if (blockX == playerGridX && blockY == playerGridY) {
            start()
        } else if (selectedBlock == 0) {
            if (tiles.tileAtLocationEquals(tiles.getTileLocation(blockX, blockY), assets.tile`stone`)) {
                breakBlock()
            }
        } else {
            if (blockAvailable == 1) {
                placeBlock()
            } else {
                music.play(music.melodyPlayable(music.buzzer), music.PlaybackMode.InBackground)
            }
        }
    } else if (state == 2) {
        // Buy stone block
        // 
        if (shopMenuSelect == 0) {
            if (coins >= 1) {
                music.play(music.melodyPlayable(music.powerUp), music.PlaybackMode.InBackground)
                coins += -1
                selectedBlock = 1
                loadLevel()
            } else {
                music.play(music.melodyPlayable(music.buzzer), music.PlaybackMode.InBackground)
                rob.sayText("Too expensive!", 1000, false)
            }
        } else {
        	
        }
    }
})
controller.left.onEvent(ControllerButtonEvent.Pressed, function () {
    if (state == 1) {
        if (blockX > minBlockX) {
            blockX += -1
        }
        grid.place(blockSelect, tiles.getTileLocation(blockX, blockY))
        updateBlockSelect()
    } else if (state == 2) {
    	
    }
})
function loadLevel () {
    state = 1
    rob = sprites.create(assets.image`rob`, SpriteKind.Player)
    blockSelect = sprites.create(assets.image`blockSelect0`, SpriteKind.Block)
    updateBlockSelect()
    sprites.destroyAllSpritesOfKind(SpriteKind.image)
    tiles.setCurrentTilemap(tilemap`level1`)
    for (let index = 0; index <= list.length; index++) {
        if (blockListType[index] == 1) {
            tiles.setTileAt(tiles.getTileLocation(blockListX[index], blockListY[index]), assets.tile`stone`)
            tiles.setWallAt(tiles.getTileLocation(blockListX[index], blockListY[index]), true)
        } else {
        	
        }
    }
    scene.setBackgroundImage(assets.image`bg`)
    grid.place(rob, tiles.getTileLocation(playerGridX, playerGridY))
    grid.snap(rob)
    grid.place(blockSelect, tiles.getTileLocation(blockX, blockY))
    scene.cameraFollowSprite(blockSelect)
}
function blockSelectMenu () {
    state = 2
    rob.setPosition(96, 22)
    sprites.destroy(blockSelect)
    tiles.setCurrentTilemap(tilemap`empty`)
    scene.centerCameraAt(0, 0)
    aButton = sprites.create(assets.image`aButton`, SpriteKind.image)
    refreshShop()
    if (coins == 0) {
        number = sprites.create(assets.image`0`, SpriteKind.image)
    } else if (coins == 1) {
        number = sprites.create(assets.image`1`, SpriteKind.image)
    } else if (coins == 2) {
        number = sprites.create(assets.image`2`, SpriteKind.image)
    }
    number.setPosition(123, 17)
    scaling.scaleToPercent(aButton, 70, ScaleDirection.Uniformly, ScaleAnchor.Middle)
    animation.runImageAnimation(
    aButton,
    assets.animation`buttonAnim`,
    500,
    true
    )
}
function updateBlockSelect () {
    blockSelect.sayText("")
    if (tiles.tileAtLocationIsWall(tiles.getTileLocation(blockX, blockY)) || tiles.tileAtLocationEquals(tiles.getTileLocation(blockX, blockY), assets.tile`lava`) || (tiles.tileAtLocationEquals(tiles.getTileLocation(blockX, blockY), assets.tile`flag`) || false)) {
        blockAvailable = 0
    } else {
        blockAvailable = 1
    }
    if (blockX == playerGridX && blockY == playerGridY) {
        blockSelect.setImage(assets.image`empty`)
        blockSelect.sayText("Go!")
    } else {
        if (selectedBlock == 0) {
            if (tiles.tileAtLocationEquals(tiles.getTileLocation(blockX, blockY), assets.tile`stone`)) {
                blockSelect.setImage(assets.image`blockSelect0X`)
            } else {
                blockSelect.setImage(assets.image`blockSelect0`)
            }
        } else if (selectedBlock == 1) {
            if (blockAvailable == 1) {
                blockSelect.setImage(assets.image`blockSelect1`)
            } else {
                blockSelect.setImage(assets.image`blockSelect1X`)
            }
        }
    }
}
controller.right.onEvent(ControllerButtonEvent.Pressed, function () {
    if (state == 1) {
        if (blockX < maxBlockX) {
            blockX += 1
        }
        grid.place(blockSelect, tiles.getTileLocation(blockX, blockY))
        updateBlockSelect()
    } else if (state == 2) {
    	
    }
})
controller.down.onEvent(ControllerButtonEvent.Pressed, function () {
    if (state == 1) {
        if (blockY < maxBlockY) {
            blockY += 1
        }
        grid.place(blockSelect, tiles.getTileLocation(blockX, blockY))
        updateBlockSelect()
    } else if (state == 2) {
    	
    }
})
function refreshShop () {
    if (itemsUnlocked == 1) {
        if (shopMenuSelect == 0) {
            scene.setBackgroundImage(assets.image`blockSelectScreen1a`)
            aButton.setPosition(67, 18)
        } else {
        	
        }
    }
}
function start () {
    music.stopAllSounds()
    music.play(music.createSong(assets.song`startMusic`), music.PlaybackMode.LoopingInBackground)
    state = 3
    sprites.destroy(blockSelect)
    scene.cameraFollowSprite(rob)
    rob.ay = 500
    rob.vx = 50
}
let number: Sprite = null
let aButton: Sprite = null
let rob: Sprite = null
let shopMenuSelect = 0
let blockAvailable = 0
let blockSelect: Sprite = null
let state = 0
let itemsUnlocked = 0
let coins = 0
let maxBlockX = 0
let minBlockX = 0
let maxBlockY = 0
let minBlockY = 0
let blockY = 0
let blockX = 0
let playerGridY = 0
let playerGridX = 0
let blockListType: number[] = []
let blockListY: number[] = []
let blockListX: number[] = []
let selectedBlock = 0
let level = 0
scene.setBackgroundImage(assets.image`bg`)
level = 1
setupLevel()
loadLevel()
music.setVolume(12)
music.play(music.createSong(assets.song`Music`), music.PlaybackMode.LoopingInBackground)
