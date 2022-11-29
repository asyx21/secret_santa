# -*- coding: utf8 -*-

"""
send_emails.py
python version: 2.7.8
author asyx21
date: 25.11.2022

This program sends Secret Santa's results to players
		
/!\ WARNING You should run "random_drawing.py" before /!\\

Inputs (arguments): participants.txt, results_folder
Outputs: None (automatic email sending)
"""

import os
import sys
from mailjet_rest import Client
from dotenv import load_dotenv
from common import extract_players_info

# Load environment variables
load_dotenv()
api_key = os.getenv('MAILJET_API_KEY')
api_secret = os.getenv('MAILJET_API_SECRET')
sender_address = os.getenv('SENDER_ADDRESS')
sender_name = os.getenv('SENDER_NAME')


#############################################################
# global variables
#############################################################
players_file = "players.example.txt"
results_folder = "results"
subject = "Christmas at home, Secret Santa draw :)"

# MaiJet Client
mailjet = Client(auth=(api_key, api_secret), version='v3.1')


#############################################################
# parsing program arguments
#############################################################
if len(sys.argv) < 2:
	print('You can specify players info file and results folder as arguments. Example "python send_emails.py players.txt results"\n\n')

players_file = sys.argv[1] if len(sys.argv) >= 2 else players_file
print('Player file input: "{}"'.format(players_file))

if len(sys.argv) >= 3:
	results_folder = sys.argv[2]
print('Loading results from: "{}"'.format(results_folder))


#############################################################
# functions: file and folder I/O
#############################################################
def get_secret_message(filename):
	msg = ''
	with open(filename, 'r') as file:
		msg = [line.rstrip('\n') for line in file]
		file.close()
	return msg[0]


#############################################################
# functions: email logic
#############################################################
def mailjet_send_email(fromaddress, fromname, message, toaddress, toname, subject):
	data = {
	  'Messages': [
	    {
	      "From": {
	        "Email": fromaddress,
	        "Name": "Santa Claus"
	      },
	      "To": [
	        {
	          "Email": toaddress,
	          "Name": toname
	        }
	      ],
	      "Subject": subject,
	      "TextPart": "Secret Santa auto email",
	      "HTMLPart": "<h3>Hi " + toname + "!</h3><br /><h4>" + message + "</h4><br /><p>See you soon, Merry Christmas !</p><br /><p>" + fromname + "</p>",
	      "CustomID": "AppSecretSanta"
	    }
	  ]
	}

	result = mailjet.send.create(data=data)
	if result.status_code != 200:
		print('Error sending to {}'.format(toaddress))
		print(result.json())
	else:
		print('Email successfuly sent to {}'.format(toname))


#############################################################
# program entrypoint
#############################################################
if __name__ == '__main__':
	player_no_email = list()
	[names_list, players_info, _] = extract_players_info(players_file)

	for name in names_list:
		# get result file
		result_file = name + ".txt"
		# get player email
		detination_address = players_info[name][1]

		secretMsg = get_secret_message(results_folder + "/" + result_file)

		# Memorize players who don't have email address
		if detination_address == '' or detination_address == ' ':
			player_no_email.append(name)
		else:
			mailjet_send_email(sender_address, sender_name, secretMsg, detination_address, name, subject)
			pass
		
	if len(player_no_email):
		print("\nFollowing players do not have email address:\n")
		print(player_no_email)

	print("\nPROGRAM FINISHED: send_email.py\n")
