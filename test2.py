#
# cocos2d
# http://python.cocos2d.org
#

from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

import random
import math

import pyglet
from pyglet.window import key
from pyglet.gl import *

import cocos
from cocos.director import director
import cocos.collision_model as cm
import cocos.euclid as eu
# import cocos.actions as ac

from cocos import actions, layer, sprite, scene

class HelloWorld(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(HelloWorld, self).__init__()

        # a cocos.text.Label is a wrapper of pyglet.text.Label
        # with the benefit of being a cocosnode
        label = cocos.text.Label('Hello, World!',
                                 font_name='Times New Roman',
                                 font_size=32,
                                 anchor_x='center', anchor_y='center')

        label.position = 320, 240
        self.add(label)
        # self.add_sprite()

    def add_sprite(self):
        heroimage = pyglet.resource.image('hero.png')
        player = cocos.sprite.Sprite(heroimage)
        player.position = (100, 100)
        self.add(player)


#class for movement of main character
class HeroShipMovement(actions.Move):
    def step(self, dt):
        super(HeroShipMovement, self).step(dt)
        velocity_x = 200 * (keyboard[key.RIGHT] - keyboard[key.LEFT])
        velocity_y = 200 * (keyboard[key.UP] - keyboard[key.DOWN])
        self.target.velocity = (velocity_x, velocity_y)

        #move = self.target.position
        #for move in range(0, 400):
           # move = move + 25
           # self.target.position = move;


class HeroShip(cocos.sprite.Sprite):
    def __init__(self, image):
        super(HeroShip, self).__init__(image)
        self.image = image
        self.position = (100, 100)
        self.velocity = (0,0)
        self.cshape = cm.AARectShape(eu.Vector2(self.position), 32, 32)


class Asteroid(cocos.sprite.Sprite):
    def __init__(self, image, position):
        super(Asteroid, self).__init__(image)
        self.image = image
        self.position = position
        self.velocity = (0,0)
        self.cshape = cm.CircleShape(eu.Vector2(self.position), 16)


class GameLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__()
        self.CollMan = cm.CollisionManager()
        self.add_hero()
        self.add_asteroids()
        # self.add_boss()
        # self.CollMan.add(hero)
        self.schedule(self.update)

    def add_hero(self):
        heroImage = pyglet.resource.image('hero.png')
        # hero = cocos.sprite.Sprite(heroImage)
        self.hero = HeroShip(heroImage)
        # hero.position = (150, 150)
        self.hero.do(HeroShipMovement())
        self.add(self.hero)

    def add_boss(self):
        bossImage = pyglet.resource.image('boss.png')
        boss = cocos.sprite.Sprite(bossImage)
        boss.position = (300, 200)
        self.add(boss)

    def add_asteroids(self):
        aster1Image = pyglet.resource.image('asteroid.png')
        aster1Position = (150, 550)
        aster1Velocity = (0, 1000)

        aster2Image = pyglet.resource.image('asteroid_2.png')
        aster2Position = (200, 500)
        aster2Velocity = (100, 25)

        self.asteroid1 = Asteroid(aster1Image, aster1Position)
        self.asteroid2 = Asteroid(aster2Image, aster2Position)
        # boss.position = (300, 200)
        self.add(self.asteroid1)
        self.add(self.asteroid2)

        self.asteroid1.do(actions.MoveBy( (0, -600), 4) )
        self.asteroid2.do(actions.MoveBy( (100, -600), 8) )

    def update(self, dt):
        self.CollMan.clear()
        self.CollMan.add(self.hero)
        self.CollMan.add(self.asteroid1)
        self.CollMan.add(self.asteroid2)


if __name__ == "__main__":

    global keyboard

    # director init takes the same arguments as pyglet.window
    cocos.director.director.init()

    #initializing pyglet, which allows for keyboard import for character movement
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    # We create a new layer, an instance of HelloWorld
    hello_layer = HelloWorld()
    game_layer = GameLayer()

    # A scene that contains the layer hello_layer
    main_scene = cocos.scene.Scene(hello_layer, game_layer)

    # And now, start the application, starting with main_scene
    cocos.director.director.run(main_scene)

    # or you could have written, without so many comments:
    #      director.run( cocos.scene.Scene( HelloWorld() ) )