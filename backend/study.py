#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 16:45:49 2024

@author: aryn
"""
from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
from pdfminer.high_level import extract_text
import random
import re
import time
from copy import copy as duplicate
import os
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
OPENAI_API_KEY = "key"

number_of_words = int(input("How many words do you want? ")) + 1

def all_words(lst, number_of_words):
    random_integers = []

    while len(random_integers) < number_of_words:
        random_integer = random.randint(1, (number_of_words + 1))
        if random_integer not in random_integers:
            random_integers.append(random_integer)

    splitted_string = lst.split('.')
    words_and_answers = []

    for i in range(len(splitted_string)):
        split = splitted_string[i].split(":")
        words_and_answers.append(split)

    words_and_answers = [pair for pair in words_and_answers if len(pair) == 2]  # Filter out pairs with incorrect format
    
    lst = []
    for i in range(len(random_integers)):
        index = random_integers[i] - 1  # Adjust index to match Python's 0-based indexing
        if index < len(words_and_answers):
            lst.append(words_and_answers[index])

    for sublist in lst:
        for i in range(len(sublist)):
            sublist[i] = sublist[i].replace('"', '')
    
    return lst


 
class Crossword(object):
    def __init__(self, cols, rows, empty='-', maxloops=2000, available_words=[]):
        self.cols = cols
        self.rows = rows
        self.empty = empty
        self.maxloops = maxloops
        self.available_words = available_words
        self.randomize_word_list()
        self.current_word_list = []
        self.clear_grid()
        self.debug = 0
 
    def clear_grid(self):
        """Initialize grid and fill with empty character."""
        self.grid = []
        for i in range(self.rows):
            ea_row = []
            for j in range(self.cols):
                ea_row.append(self.empty)
            self.grid.append(ea_row)
 
    def randomize_word_list(self):
        """Reset words and sort by length."""
        temp_list = []
        for word in self.available_words:
            if isinstance(word, Word):
                temp_list.append(Word(word.word, word.clue))
            else:
                temp_list.append(Word(word[0], word[1]))
        # randomize word list
        random.shuffle(temp_list)
        # sort by length
        temp_list.sort(key=lambda i: len(i.word), reverse=True)
        self.available_words = temp_list

    def compute_crossword(self, time_permitted=1.00, spins=2):
        copy = Crossword(self.cols, self.rows, self.empty,
                         self.maxloops, self.available_words)

        count = 0
        time_permitted = float(time_permitted)
        start_full = float(time.time())

        # only run for x seconds
        while (float(time.time()) - start_full) < time_permitted or count == 0:
            self.debug += 1
            copy.randomize_word_list()
            copy.current_word_list = []
            copy.clear_grid()

            x = 0
            # spins; 2 seems to be plenty
            while x < spins:
                for word in copy.available_words:
                    if word not in copy.current_word_list:
                        copy.fit_and_add(word)
                x += 1
            #print(copy.solution())
            #print(len(copy.current_word_list), len(self.current_word_list), self.debug)
            # buffer the best crossword by comparing placed words
            if len(copy.current_word_list) > len(self.current_word_list):
                self.current_word_list = copy.current_word_list
                self.grid = copy.grid
            count += 1
        return
 
    def suggest_coord(self, word):
        #count = 0
        coordlist = []
        glc = -1

        # cycle through letters in word
        for given_letter in word.word:
            glc += 1
            rowc = 0
            # cycle through rows
            for row in self.grid:
                rowc += 1
                colc = 0
                # cycle through letters in rows
                for cell in row:
                    colc += 1
                    # check match letter in word to letters in row
                    if given_letter == cell:
                        # suggest vertical placement 
                        try:
                            # make sure we're not suggesting a starting point off the grid
                            if rowc - glc > 0:
                                # make sure word doesn't go off of grid   
                                if ((rowc - glc) + word.length) <= self.rows:
                                    coordlist.append([colc, rowc-glc, 1, colc+(rowc-glc),0])
                        except:
                            pass

                        # suggest horizontal placement 
                        try:
                            # make sure we're not suggesting a starting point off the grid
                            if colc - glc > 0: 
                                # make sure word doesn't go off of grid
                                if ((colc - glc) + word.length) <= self.cols:
                                    coordlist.append([colc-glc, rowc, 0, rowc+(colc-glc),0])
                        except:
                            pass

        # example: coordlist[0] = [col, row, vertical, col + row, score]
        #print(word.word)
        #print(coordlist)
        new_coordlist = self.sort_coordlist(coordlist, word)
        #print(new_coordlist)

        return new_coordlist
 
    def sort_coordlist(self, coordlist, word):
        """Give each coordinate a score, then sort."""
        new_coordlist = []
        for coord in coordlist:
            col, row, vertical = coord[0], coord[1], coord[2]
            # checking scores
            coord[4] = self.check_fit_score(col, row, vertical, word)
            # 0 scores are filtered
            if coord[4]:
                new_coordlist.append(coord)
        # randomize coord list; why not?
        random.shuffle(new_coordlist)
        # put the best scores first
        new_coordlist.sort(key=lambda i: i[4], reverse=True)
        return new_coordlist
 
    def fit_and_add(self, word):
        """Doesn't really check fit except for the first word;
        otherwise just adds if score is good.
        """
        fit = False
        count = 0
        coordlist = self.suggest_coord(word)
 
        while not fit and count < self.maxloops:
            # this is the first word: the seed
            if len(self.current_word_list) == 0:
                # top left seed of longest word yields best results (maybe override)
                vertical, col, row = random.randrange(0, 2), 1, 1

           
 
                if self.check_fit_score(col, row, vertical, word):
                    fit = True
                    self.set_word(col, row, vertical, word, force=True)

            # a subsquent words have scores calculated
            else:
                try:
                    col, row, vertical = coordlist[count][0], coordlist[count][1], coordlist[count][2]
                # no more cordinates, stop trying to fit
                except IndexError:
                    return
 
                # already filtered these out, but double check
                if coordlist[count][4]:
                    fit = True
                    self.set_word(col, row, vertical, word, force=True)
 
            count += 1

        return
 
    def check_fit_score(self, col, row, vertical, word):
        """Return score: 0 signifies no fit, 1 means a fit, 2+ means a cross.
        The more crosses the better.
        """
        if col < 1 or row < 1:
            return 0

        # give score a standard value of 1, will override with 0 if collisions detected
        count, score = 1, 1
        for letter in word.word:
            try:
                active_cell = self.get_cell(col, row)
            except IndexError:
                return 0
 
            if active_cell == self.empty or active_cell == letter:
                pass
            else:
                return 0
 
            if active_cell == letter:
                score += 1
 
            if vertical:
                # check surroundings
                if active_cell != letter: # don't check surroundings if cross point
                    if not self.check_if_cell_clear(col+1, row): # check right cell
                        return 0
 
                    if not self.check_if_cell_clear(col-1, row): # check left cell
                        return 0
 
                if count == 1: # check top cell only on first letter
                    if not self.check_if_cell_clear(col, row-1):
                        return 0
 
                if count == len(word.word): # check bottom cell only on last letter
                    if not self.check_if_cell_clear(col, row+1): 
                        return 0
            else: # else horizontal
                # check surroundings
                if active_cell != letter: # don't check surroundings if cross point
                    if not self.check_if_cell_clear(col, row-1): # check top cell
                        return 0
 
                    if not self.check_if_cell_clear(col, row+1): # check bottom cell
                        return 0
 
                if count == 1: # check left cell only on first letter
                    if not self.check_if_cell_clear(col-1, row):
                        return 0
 
                if count == len(word.word): # check right cell only on last letter
                    if not self.check_if_cell_clear(col+1, row):
                        return 0
 
            if vertical: # progress to next letter and position
                row += 1
            else: # else horizontal
                col += 1
 
            count += 1
 
        return score
 
    def set_word(self, col, row, vertical, word, force=False):
        """Set word in the grid, and adds word to word list."""
        if force:
            word.col = col
            word.row = row
            word.vertical = vertical
            self.current_word_list.append(word)
 
            for letter in word.word:
                self.set_cell(col, row, letter)
                if vertical:
                    row += 1
                else:
                    col += 1

        return
 
    def set_cell(self, col, row, value):
        self.grid[row-1][col-1] = value
 
    def get_cell(self, col, row):
        return self.grid[row-1][col-1]
 
    def check_if_cell_clear(self, col, row):
        try:
            cell = self.get_cell(col, row)
            if cell == self.empty: 
                return True
        except IndexError:
            pass
        return False
 
    def solution(self):
        """Return solution grid."""
        outStr = ""
        for r in range(self.rows):
            for c in self.grid[r]:
                outStr += '%s ' % c
            outStr += '\n'
        return outStr
 
    def order_number_words(self):
        """Orders words and applies numbering system to them."""
        self.current_word_list.sort(key=lambda i: (i.col + i.row))
        count, icount = 1, 1
        for word in self.current_word_list:
            word.number = count
            if icount < len(self.current_word_list):
                if word.col == self.current_word_list[icount].col and word.row == self.current_word_list[icount].row:
                    pass
                else:
                    count += 1
            icount += 1
 
    def display(self, order=True):
        """Return (and order/number wordlist) the grid minus the words adding the numbers"""
        outStr = ""
        if order:
            self.order_number_words()
 
        copy = self
 
        for word in self.current_word_list:
            copy.set_cell(word.col, word.row, word.number)
 
        for r in range(copy.rows):
            for c in copy.grid[r]:
                outStr += '%s ' % c
            outStr += '\n'
 
        outStr = re.sub(r'[a-z]', ' ', outStr)
        return outStr
 
    def word_bank(self):
        outStr = ''
        temp_list = duplicate(self.current_word_list)
        # randomize word list
        random.shuffle(temp_list)
        for word in temp_list:
            outStr += '%s\n' % word.word
        return outStr
 
    def legend(self):
        """Must order first."""
        outStr = ''
        for word in self.current_word_list:
            outStr += '%d. (%d,%d) %s: %s\n' % (word.number, word.col, word.row, word.down_across(), word.clue)
        return outStr


class Word(object):
    def __init__(self, word=None, clue=None):
        self.word = re.sub(r'\s', '', word.lower())
        self.clue = clue
        self.length = len(self.word)
        # the below are set when placed on board
        self.row = None
        self.col = None
        self.vertical = None
        self.number = None
 
    def down_across(self):
        """Return down or across."""
        if self.vertical: 
            return 'down'
        else: 
            return 'across'
 
    def __repr__(self):
        return self.word
 
@app.route('/generate_crossword', methods=['POST'])
def generate_crossword():
    pdf_file = request.files['pdf']  # get the PDF file from the request 
    crossword = main(pdf_file)  # generate the crossword
    return jsonify(crossword)  # return the crossword as JSON

# Main function to take user input, process notes, and generate main points and summaries
def main(pdf_file):
    openai.api_key = OPENAI_API_KEY
    # Take user input for notes
    pdf_file.save(os.path.join('files', pdf_file.filename))
    notes = extract_text((os.path.join('files', pdf_file.filename)))

    while True:
        # Construct a prompt asking for main points and a summary
        prompt = f"Please generate main points and a summary based on the following study notes, format it as a keyphrase : summary, each keyphrase and summary pair is seperated by a period, pretend you are a crossword maker and you are creating answers to the crossword and their corresponding clues:\n{notes}"

        # Call the OpenAI API to generate main points and a summary
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",  # You can use other engines like "curie" if needed
            prompt=prompt,
            max_tokens=800,  # Adjust as needed
            temperature=0.5,  # Adjust as needed
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,

            )
        
        # Print the generated main points and summary
        defs = response.choices[0].text.strip()
        
        #print(defs)
    
        word_list = all_words(defs, number_of_words)

        if(len(word_list) != number_of_words):
            continue
        else:
            break
    
    #start_full = float(time.time())

    if number_of_words <= 5:
        length = 20
    if 5 < number_of_words <= 10:
        length = 30
    if 10 < number_of_words <= 15:
        length = 40
    a = Crossword(length, length, '-', 5000, word_list)
    a.compute_crossword(2)
    print(a.word_bank())
    print(a.solution())
    print(a.display())
    print(a.legend())
    

    end_full = float(time.time())
    
    

if __name__ == "__main__":
    app.run(port=5000, debug=True)
