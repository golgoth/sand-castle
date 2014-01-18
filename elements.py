#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyglet
from state import Idle, Moving, Attacking
import config

from math import radians, atan2

class Element(object):
	""" Main class of elements on board """
	def __init__(self, game, x, y, w=1, h=1):
		super(Element, self).__init__()
		self.x, self.y = x, y
		self.w, self.h = w, h

		self.game = game
		
		self._state = Idle(self)

		self.last_state = Idle(self)

		self.cur_image = self.images[Idle][0][0]

	@property
	def state(self):
		return self._state

	@state.setter
	def state(self, value):
		self.last_state = self._state
		self._state = value

	def update(self, dt):
		self.state.update(dt)

	def center(self):
		center = (self.x + self.w*config.CELL_SIZE/2 , self.y + self.h*config.CELL_SIZE/2)
		return center

	def draw(self):
		sprite = pyglet.sprite.Sprite(self.cur_image, self.x, self.y)
		sprite.draw()

	def interact(self, character):
		pass

	def collision(self):
		self.state = Idle(self)

	def cells(self):
		cell_x = int(self.x // config.CELL_SIZE)
		cell_y = int(self.y // config.CELL_SIZE)

		return [(cell_x + i, cell_y + j) for i in xrange(self.w) for j in xrange(self.h)
		        if 0 <= cell_x + i < self.game.grid.w and 0 <= cell_y + j < self.game.grid.h ]
#SubClass
class Creature(Element):

	def __init__(self, *args, **kwargs):
		super(Creature, self).__init__(*args, **kwargs)

		self.hp = 10

		self.angle = 0.0
		self.speed = 500

class StillObject(Element):
	def __init__(self, *args, **kwargs):
		super(StillObject, self).__init__(*args, **kwargs)

#SubSubClass
class Character(Creature):
	images = {

			Idle: [
			[pyglet.image.load('images/char/idle/0_{}.png'.format(pos)) for pos in ['right', 'top', 'left', 'bottom']]
			],
			Moving : [
			[pyglet.image.load('images/char/moving/{}_{}.png'.format(f,p)) for p in ['right', 'top', 'left', 'bottom']] for f in range(4) 
			],
			
			 }

	def __init__(self, *args, **kwargs):
		self.hp = 20
		self.images = Character.images

		super(Character, self).__init__(*args, w=1, h=2, **kwargs)

	def attack(self):
		#liste des cases du character
		allPosCharacter = [(self.x//config.CELL_SIZE, self.y//config.CELL_SIZE),
							 ((self.x + self.w)//config.CELL_SIZE, self.y//config.CELL_SIZE),
							 (self.x //config.CELL_SIZE,(self.y + self.h)//config.CELL_SIZE),
							 ((self.x + self.w)//config.CELL_SIZE,(self.y + self.h)//config.CELL_SIZE)]
		allPosTarget = []
		for i in range(self.x//config.CELL_SIZE - 1, self.x//config.CELL_SIZE + 2):
			for j in range (self.y//config.CELL_SIZE - 1, self.y//config.CELL_SIZE + 2):
				if not((i,j) in allPosCharacter):
					allPosTarget.append((i,j))


		posElement = (x/config.CELL_SIZE, y/config.CELL_SIZE)

		self.state = Attacking(self)


class Castle(Creature):
	images = {

			Idle: [
			[pyglet.image.load('images/castle/idle/{}.png'.format(pos)) for pos in ['etat0', 'etat1', 'etat2']]
			]
			 }
	def __init__(self, *args, **kwargs):
		self.images = Castle.images
		self.hp = 100
		super(Castle, self).__init__(*args, **kwargs)



class Monster(Creature):
	images = {

			Idle: [
			[pyglet.image.load('images/monster/idle/0_right.png')]
			],
			Moving : [
			[pyglet.image.load('images/monster/moving/{}_right.png'.format(f))] for f in range(4) 
			],
			Attacking : [
			[pyglet.image.load('images/monster/attacking/{}_{}.png'.format(f,p)) for p in ['right']] for f in range(4) 
			]
			
			 }

 
	def setAngle(self):
		c_x, c_y = self.game.castle.x, self.game.castle.y
		self.angle = atan2(c_y - self.y , c_x -self.x)
		self.state = Moving(self, 0)

	def __init__(self, *args, **kwargs):
		self.images = Monster.images
		self.hp = 30

		super(Monster, self).__init__(*args, **kwargs)
		self.speed = 100

	def collision(self):
		neighbours = self.game.grid.neighbours(self)

		for n in neighbours:
			if isinstance(n, Castle) or isinstance(n, Character):
				self.state = Attacking(self,n)
				return

class Chest(StillObject):
	images = {

			Idle: [
			[pyglet.image.load('images/chest/idle/chest_idle.png')]
			]

			 }
	def __init__(self, item, *args, **kwargs):
		self.item = item

		self.images = Chest.images
		super(Chest, self).__init__(*args, **kwargs)
	
	def interact(self, character):
		character.game.rubies += 1

if __name__ == '__main__':
	pass

