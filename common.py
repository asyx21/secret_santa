"""
Common functions for Secret Santa app
"""

def extract_players_info(file):
	players_names = list()
	text_lines = list()
	players_info = dict()

	with open(file, 'r') as file_read:
		text_lines = [line.rstrip('\n') for line in file_read]
		file_read.close()

	for line in text_lines:
		if line == '' or line.startswith('#'):
			continue
		person = line.split(",")

		#print person
		# players_info['name']: [0] = pseudonym, [1] = email, [2] = exclusion
		players_info[person[0]] = (person[1], person[2], person[3])
		players_names.append(person[0])

	print('\nHere is the list of {} names:\n\n{}\n\n'.format(str(len(players_names)), players_names))
	return (players_names, players_info, text_lines)
