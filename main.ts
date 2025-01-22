namespace SpriteKind {
    export const camera = SpriteKind.create()
    export const Block = SpriteKind.create()
    export const image = SpriteKind.create()
}

//  States
//  
//  0 - Main Menu
//  
//  1 - Editor
//  
//  2 - Block Select
//  
//  3 - Game
//  
//  4 - End Screen
//  
//  5 - Start Screen

// blockSelected
//
// 0 - default

//  Variables
let state: number = 0
let level: number = 1

let cursorX: number = 0
let cursorY: number = 0
let minCursorX: number = 0
let minCursorY: number = 0
let maxCursorX: number = 0
let maxCursorY: number = 0

let coins: number = 0
let itemsUnlocked: number = 0
let blockSelected: number = 0
let canStart: boolean = false

let map2: tiles.TileMapData = null
let cutsceneMap: tiles.TileMapData = null

let rob: Sprite = null
let cursor: Sprite = null


controller.A.onEvent(ControllerButtonEvent.Pressed, function () {
    if (state == 0) {
        startScreen()
    } else if (state == 1) {
        if (canStart) {
            start()
        }
    } else if (state == 2) {

    } else if (state == 3) {

    } else if (state == 4) {

    }

})
controller.B.onEvent(ControllerButtonEvent.Pressed, function () {
    if (state == 0) {
        startScreen()
    } else if (state == 1) {

    } else if (state == 2) {

    } else if (state == 3) {

    } else if (state == 4) {

    }

})
controller.up.onEvent(ControllerButtonEvent.Pressed, function () {

    if (state == 0) {
        startScreen()
    } else if (state == 1) {
        if (cursorY > minCursorY) {
            cursorY -= 1
            updateCursor()
        }

    } else if (state == 2) {

    } else if (state == 3) {

    } else if (state == 4) {

    }

})
controller.down.onEvent(ControllerButtonEvent.Pressed, function () {

    if (state == 0) {
        startScreen()
    } else if (state == 1) {
        if (cursorY < maxCursorY) {
            cursorY += 1
            updateCursor()
        }

    } else if (state == 2) {

    } else if (state == 3) {

    } else if (state == 4) {

    }

})
controller.left.onEvent(ControllerButtonEvent.Pressed, function () {
    if (state == 0) {
        startScreen()
    } else if (state == 1) {
        if (cursorX > minCursorX) {
            cursorX -= 1
            updateCursor()
        }

    } else if (state == 2) {

    } else if (state == 3) {

    } else if (state == 4) {

    }

})
controller.right.onEvent(ControllerButtonEvent.Pressed, function () {

    if (state == 0) {
        startScreen()
    } else if (state == 1) {
        if (cursorX < maxCursorX) {
            cursorX += 1
            updateCursor()
        }

    } else if (state == 2) {

    } else if (state == 3) {

    } else if (state == 4) {

    }

})

game.onUpdate(function () {
    if (state == 1) {

    } else if (state == 2) {

    } else if (state == 3 && rob != null) {
        if (rob.isHittingTile(CollisionDirection.Right)) {
            rob.vx = -40
            animation.runImageAnimation(rob, assets.animation`robWalkRight`, 15, true)
        }

        if (rob.isHittingTile(CollisionDirection.Left)) {
            rob.vx = 40
            animation.runImageAnimation(rob, assets.animation`robWalkLeft`, 15, true)
        }
    }
})

function titleScreen() {

    state = 0
    scene.setBackgroundImage(assets.image`mainMenuScreen`)

    //  Music
    music.stopAllSounds()
    music.setVolume(45)
    music.play(music.createSong(assets.song`menuSong`), music.PlaybackMode.LoopingInBackground)

    //  Create title text
    let titleScreenText = textsprite.create("Rob's Lab")
    scaling.scaleToPercent(titleScreenText, 250)
    titleScreenText.setPosition(80, 15)

    //  Create bottom text
    let bottomText = textsprite.create("Press any button to start.")
    bottomText.setPosition(80, 110)

    timer.background(function () {
        while (state == 0) {
            pause(500)
            bottomText.setText("")
            pause(500)
            bottomText.setText("Press any button to start.")
        }
    })
    pauseUntil(() => (state != 0))
    sprites.destroy(bottomText)
    sprites.destroy(titleScreenText)
}

function startScreen() {

    state = 5
    scene.setBackgroundImage(assets.image`transition`)
    //  Create start text
    let startText = textsprite.create("Level " + ("" + ("" + level)) + " start!")
    startText.setPosition(80, 60)
    scaling.scaleToPercent(startText, 140)
    music.stopAllSounds()
    pause(50)
    music.setVolume(120)
    music.play(music.melodyPlayable(music.powerUp), music.PlaybackMode.UntilDone)
    pause(500)
    sprites.destroy(startText)
    setupLevel()
    loadLevel()
}

function setupLevel() {

    blockSelected = 0

    if (level == 1) {
        map2 = assets.tilemap`level1`
        cutsceneMap = assets.tilemap`cutscene1`
        minCursorX = 0
        minCursorY = 10
        maxCursorX = 7
        maxCursorY = 15
    } else if (level == 2) {

    } else if (level == 3) {

    } else if (level == 4) {

    } else if (level == 5) {

    } else if (level == 6) {

    } else if (level == 7) {

    }

    music.stopAllSounds()
    music.setVolume(45)
    music.play(music.createSong(assets.song`music`), music.PlaybackMode.LoopingInBackground)
    tiles.setCurrentTilemap(map2)

    cursor = sprites.create(assets.image`cursor0`)
    cursorX = tiles.getTilesByType(assets.tile`robSpawn`)[0].col + 1
    cursorY = tiles.getTilesByType(assets.tile`robSpawn`)[0].row
    scene.cameraFollowSprite(cursor)
}

function loadLevel() {
    state = 1

    tiles.setCurrentTilemap(map2)
    scene.setBackgroundImage(assets.image`bg`)

    updateCursor()
}

function updateCursor() {
    let cursorLocation = tiles.getTileLocation(cursorX, cursorY)
    tiles.placeOnTile(cursor, cursorLocation)
    cursor.sayText(null)
    canStart = false
    if (tiles.tileAtLocationEquals(cursorLocation, assets.tile`robSpawn`)) {
        cursor.setImage(assets.image`empty`)
        cursor.sayText("Go!")
        canStart = true
    } else if (blockSelected == 0) {
        cursor.setImage(assets.image`cursor0`)
    }

}

function start() {
    state = 3

    cursor.sayText("")

    music.stopAllSounds()
    music.setVolume(45)
    music.play(music.createSong(assets.song`startMusic`), music.PlaybackMode.LoopingInBackground)

    let spawnLoc = tiles.getTilesByType(assets.tile`robSpawn`)[0]
    rob = sprites.create(assets.image`robRight`)
    animation.runImageAnimation(rob, assets.animation`robWalkRight`, 15, true)
    tiles.placeOnTile(rob, spawnLoc)
    rob.ay = 250
    rob.vx = 40
    tiles.setTileAt(spawnLoc, assets.image`empty`)
    scene.cameraFollowSprite(rob)
}

titleScreen()