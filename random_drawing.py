# -*- coding: utf8 -*-

"""
random_drawing.py
python version: 2.7.8
author asyx21
date: 25.11.2022

This program makes secret Santa's draw pseudo-randomly taking into account potential exclusion in between two or more players.

The results are written in separate files and are sent by email provided that player's have one.

Inputs (arguments): player_file.txt, output_folder
Outputs: creates files "Name.txt" in which each person has another person's assigned to give a gift
By default those results files a created inside the folder "results/"
"""

import os
import sys
import random
import glob

#############################################################
# global variables
#############################################################
players_file = "players.example.txt"
results_folder = "results"

#############################################################
# parsing program arguments
#############################################################
if len(sys.argv) < 2:
	print('You can specify candidates file as argument. Example "python random_drawing.py players.txt"\n\n')

players_file = sys.argv[1] if len(sys.argv) >= 2 else players_file
print('Player file: "{}"'.format(players_file))

if len(sys.argv) >= 3:
	results_folder = sys.argv[2]


#############################################################
# functions: file and folder I/O
#############################################################
def extract_players_info(file):
	players_names = list()
	players = list()
	players_info = dict()

	with open(file, 'r') as file_read:
		players = [line.rstrip('\n') for line in file_read]
		file_read.close()

	for line in players:
		if line == '' or line.startswith('#'):
			continue
		person = line.split(",")

		#print person
		# players_info['name'][0] correspond au pseudo, players_info['name'][1] à l'email
		players_info[person[0]] = (person[1], person[2], person[3])
		players_names.append(person[0])

	print('\nHere is the list of {} names:\n\n{}\n\n'.format(str(len(players_names)), players_names))
	return (players_names, players, players_info)

def prepare_results_folder(res_folder):
	# change directory
	#print os.getcwd()
	try:
		os.chdir(res_folder)
	except:
		# create folder if not exists
		os.mkdir(res_folder)
		os.chdir(res_folder)

	# clean old files in folder
	txtFiles = glob.glob("*.txt")
	for f in txtFiles:
		os.remove(f)


#############################################################
# functions: drawings logic
#############################################################
def is_in_exclusion(name_chosen, exclusion):
	exclusion_list = exclusion.split('|')
	return name_chosen in exclusion_list

def drawings_random(players_names):
	random.shuffle(players_names, random.random)

	# copy players list in another one with an offset
	players_names_shifted = players_names[:(len(players_names)-1)]
	players_names_shifted.insert(0, players_names[len(players_names)-1])
	#print players_names_shifted
	return players_names_shifted

def drawings(players_names, players_info):
	dict_names = dict()
	exclusion_did_not_work = 0

	while exclusion_did_not_work < 30:
		exclusion_did_not_work = exclusion_did_not_work + 1
		print('drawings attempt: ', exclusion_did_not_work)
		players_names_shifted = drawings_random(players_names)

		success = True
		# assign each drawn result to its Santa
		for index, santa in enumerate(players_names):
			dict_names[santa] = players_names_shifted[index]
			
			#print('Santa', santa, 'choice', dict_names[santa], 'EXCL', players_info[santa][2])

			if is_in_exclusion(dict_names[santa], players_info[santa][2]):
				dict_names = dict()
				success = False
				break
	
		#print('SUCCESS', success)
		if success == True:
			exclusion_did_not_work = 100

	if not bool(dict_names): print('drawings FAILED')
	else: print('drawings success !')
	return dict_names


#############################################################
# function: helpers
#############################################################
def display_specific_result(dict_names, names):
	# to print a player's draw in particular
	print('\n')
	for key, val in dict_names.items():
		if key in names:
			print('{} -> {}'.format(key, val))


#############################################################
# program entrypoint
#############################################################
if __name__ == '__main__':
	# names parsing
	[players_names, player, players_info] = extract_players_info(players_file)

	# drawings
	dict_names = drawings(players_names, players_info)
	display_specific_result(dict_names, ['Carlos', 'Marija'])

	prepare_results_folder(results_folder)

	# creates results files
	for key, name in dict_names.items():
		pseudo = players_info[name][0]
		santa_file = key + ".txt"
		if pseudo != '':
			surprise_name = 'You are the Santa of {} "{}"\n\nMerry Christmas !\n'.format(name, pseudo)
		else:
			surprise_name = 'You are the Santa of {}\n\nMerry Christmas !\n'.format(name)
		
		with open(santa_file, 'w+') as file:
			file.write(surprise_name)
			file.close()

	print('\nPROGRAM FINISHED: Results in folder "{}"\n'.format(results_folder))
	#raw_input("press any key to end program")

