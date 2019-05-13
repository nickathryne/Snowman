# File: SnowmanGame.py
"""
This module is the file for Snowman, a modified version of Hangman
in which the object is to find the magic word before Calvin completes the
snowman that will become a Deranged Mutant Killer Monster Snow Goon.
"""

from pgl import GWindow, GLabel, GLine, GArc
from SnowmanConstants import *
import random
from SnowmanWords import SNOWMAN_WORDS
from SnowmanGraphics import createEmptySnowman, addSnowmanPart

# Main program

def SnowmanGame():

	def clickAction(e):
		"""
		Checks if there is a letter where was clicked and identifies
		the letter. Counts incorrect guesses and implements game over
		and resets the screen.
		"""
		nonlocal incorrect_guesses, snowman, mystery_word, full_word, word_display, game_over, letters_chosen, timer
		if e.getY() > GWINDOW_HEIGHT - WORD_BASE and not game_over:
			pick = gw.getElementAt(e.getX(), e.getY())
			if pick is not None:
				letter = pick.getLabel()
				if letter in letters_chosen:
					gw.remove(gw.getElementAt(GWINDOW_WIDTH / 2, GWINDOW_HEIGHT - MESSAGE_BASE))
					message = GLabel('You already picked that letter!')
					message.setFont(MESSAGE_FONT)
					gw.add(message, (GWINDOW_WIDTH - message.getWidth()) / 2, GWINDOW_HEIGHT - MESSAGE_BASE)
				else:
					letters_chosen.append(letter)
					gw.remove(gw.getElementAt(GWINDOW_WIDTH / 2, GWINDOW_HEIGHT - MESSAGE_BASE))
					if letterFound(letter):
						pick.setColor(CORRECT_COLOR)
					else:
						pick.setColor(INCORRECT_COLOR)
						incorrect_guesses += 1
						addSnowmanPart(snowman, incorrect_guesses)
			else:
				gw.remove(gw.getElementAt(GWINDOW_WIDTH / 2, GWINDOW_HEIGHT - MESSAGE_BASE))
				message = GLabel('Click a letter!')
				message.setFont(MESSAGE_FONT)
				gw.add(message, (GWINDOW_WIDTH - message.getWidth()) / 2, GWINDOW_HEIGHT - MESSAGE_BASE)
			if incorrect_guesses == 8:
				game_over = True
				gw.remove(gw.getElementAt(GWINDOW_WIDTH / 2, GWINDOW_HEIGHT - MESSAGE_BASE))
				message = GLabel('YOU LOSE!')
				message.setFont(MESSAGE_FONT)
				message.setColor(INCORRECT_COLOR)
				gw.add(message, (GWINDOW_WIDTH - message.getWidth()) / 2, GWINDOW_HEIGHT - MESSAGE_BASE)
				animateSnowman()
		elif not game_over:
			gw.remove(gw.getElementAt(GWINDOW_WIDTH / 2, GWINDOW_HEIGHT - MESSAGE_BASE))
			message = GLabel('Click a letter!')
			message.setFont(MESSAGE_FONT)
			gw.add(message, (GWINDOW_WIDTH - message.getWidth()) / 2, GWINDOW_HEIGHT - MESSAGE_BASE)
		elif game_over:
			timer.stop()
			gw.clear()
			full_word = random.choice(SNOWMAN_WORDS)
			mystery_word = '-' * len(full_word)
			word_display = GLabel(mystery_word)
			word_display.setFont(WORD_FONT)
			gw.add(word_display, (GWINDOW_WIDTH - word_display.getWidth()) / 2, GWINDOW_HEIGHT - WORD_BASE)
			alphabet ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
			for i in range(len(alphabet)):
				letter = GLabel(alphabet[i])
				letter.setFont(LETTER_FONT)
				x = ((GWINDOW_WIDTH - len(alphabet) * letter.getWidth()) / (len(alphabet) + 1)) * (1 + i) + i * letter.getWidth()
				gw.add(letter, x , GWINDOW_HEIGHT - LETTER_BASE)
			incorrect_guesses = 0
			snowman = createEmptySnowman(gw)
			game_over = False
			letters_chosen = []



	def letterFound(ch):
		"""
		Checks if the letter clicked is in the word and replaces dashes with
		the letter everywhere it appears
		"""
		nonlocal full_word, mystery_word, word_display, game_over
		s = 0
		if full_word.find(ch) != -1:
			while s <= len(full_word):
				if full_word.find(ch, s) != -1:
					letter = full_word.find(ch, s)
					mystery_word = mystery_word[:letter] + ch + mystery_word[letter + 1:]
					s += letter + 1
				else: 
					s = len(full_word) + 1
			gw.remove(word_display)
			word_display = GLabel(mystery_word)
			word_display.setFont(WORD_FONT)
			gw.add(word_display, (GWINDOW_WIDTH - word_display.getWidth()) / 2, GWINDOW_HEIGHT - WORD_BASE)
			if mystery_word == full_word:
				message = gw.getElementAt(GWINDOW_WIDTH / 2, GWINDOW_HEIGHT - MESSAGE_BASE)
				gw.remove(message)
				message = GLabel('YOU WIN!')
				message.setFont(MESSAGE_FONT)
				message.setColor(CORRECT_COLOR)
				gw.add(message, (GWINDOW_WIDTH - message.getWidth()) / 2, GWINDOW_HEIGHT - MESSAGE_BASE)
				game_over = True
				animateMelting()
			return True

	def animateSnowman():
		"""
		Moves the snowman menacingly if the game is lost.
		"""
		nonlocal timer
		def step():
			nonlocal snowman, dx, dy, full_word
			if snowman.getX() > (GWINDOW_WIDTH - BASE_SIZE) or snowman.getX() < BASE_SIZE:
				dx *= -1
				gw.remove(gw.getElementAt(GWINDOW_WIDTH / 2, GWINDOW_HEIGHT - WORD_BASE))
				word_display = GLabel(full_word)
				word_display.setFont(WORD_FONT)
				word_display.setColor(INCORRECT_COLOR)
				gw.add(word_display, (GWINDOW_WIDTH - word_display.getWidth()) / 2, GWINDOW_HEIGHT - WORD_BASE)
			elif snowman.getY() < (GWINDOW_HEIGHT - BASE_SIZE - BODY_SIZE - HEAD_SIZE) or snowman.getY() > SNOWMAN_BASE:
				dy *= -1
			snowman.move(dx, dy)
		x_1 = .5 * EYE_SEP + (1 + .1) * EYE_SIZE
		y_1 = -BASE_SIZE - BODY_SIZE - HEAD_SIZE + .17 * HEAD_SIZE
		x_2 = .5 * EYE_SEP
		y_2 = -BASE_SIZE - BODY_SIZE - HEAD_SIZE + .255 * HEAD_SIZE
		brow_1 = GLine(-x_1, y_1, -x_2, y_2)
		brow_2 = GLine(x_1, y_1, x_2, y_2)
		snowman.add(brow_1)
		snowman.add(brow_2)
		TIME_STEP = 70
		dx = (GWINDOW_WIDTH - BASE_SIZE) / TIME_STEP
		dy = (GWINDOW_HEIGHT - BASE_SIZE - BODY_SIZE - HEAD_SIZE) / (TIME_STEP)
		timer = gw.createTimer(step, TIME_STEP)
		timer.setRepeats(True)
		timer.start()

	def animateMelting():
		"""
		Moves the snowman off-screen if the game is won.
		"""
		nonlocal timer
		def step():
			nonlocal snowman, dy
			snowman.move(0, dy)
		TIME_STEP = 70
		dy = (GWINDOW_HEIGHT + BASE_SIZE + BODY_SIZE + HEAD_SIZE) / TIME_STEP
		timer = gw.createTimer(step, TIME_STEP)
		timer.setRepeats(True)
		timer.start()

	random.seed()
	gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
	full_word = random.choice(SNOWMAN_WORDS)
	mystery_word = '-' * len(full_word)
	word_display = GLabel(mystery_word)
	word_display.setFont(WORD_FONT)
	gw.add(word_display, (GWINDOW_WIDTH - word_display.getWidth()) / 2, GWINDOW_HEIGHT - WORD_BASE)

	alphabet ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	for i in range(len(alphabet)):
		letter = GLabel(alphabet[i])
		letter.setFont(LETTER_FONT)
		x = ((GWINDOW_WIDTH - len(alphabet) * letter.getWidth()) / (len(alphabet) + 1)) * (1 + i) + i * letter.getWidth()
		gw.add(letter, x , GWINDOW_HEIGHT - LETTER_BASE)

	gw.addEventListener('click', clickAction)
	incorrect_guesses = 0
	snowman = createEmptySnowman(gw)
	game_over = False
	letters_chosen = []
	timer = None

# Startup code

if __name__ == "__main__":
	SnowmanGame()
