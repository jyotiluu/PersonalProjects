import sys
import time
import datetime
import random

def main():
	# take user input about what activities they completed
	get_input()
	# read log of what activities have been completed in past, print point total
	activity_list = read_activity_log()
	# use log to determine which activity should be recommended to do next
	choose_next_activity(activity_list)

def get_input():
	input_more = True
	data = ""
	now = datetime.datetime.now().strftime("%m-%d-%Y")
	while input_more:
		print("Which task did you complete? \n\t1. Read \n\t2. Exercise \n\t3. Journal \n\t4. Code \nPlease enter a number: ")
		sys.stdout.flush()
		activity_completed = input()
		# arbitrary values set by me for each activity
		if activity_completed == '1' or activity_completed.lower() == 'read':
			data = "%s Read 5"%now
		elif activity_completed == '2'or activity_completed.lower() == 'exercise':
			data = "%s Exercise 2"%now
		elif activity_completed == '3'or activity_completed.lower() == 'journal':
			data = "%s Journal 1"%now
		elif activity_completed == '4'or activity_completed.lower() == 'code':
			data = "%s Code 2"%now
		else:
			print("Sorry that's not a valid input")
			input_more = False
			break
		# save the input to a file 
		file = open("points.txt", "a")
		file.write("%s \n"%data)
		print("Did you complete another task? \nEnter y/n: ")
		repeat = input()
		if repeat.lower() == "y":
			input_more = True
		else: 
			input_more = False

def read_activity_log():
	activity_list = []
	points_list = []
	with open("points.txt") as file:
		for line in file:
			(date, activity, points) = line.split()
			activity_list.append(activity)
			points_list.append(int(points))
	print("Current point total: %s \n"%sum(points_list))
	return activity_list

def choose_next_activity(activity_list):
	reading_count = excercising_count = journaling_count = coding_count = 0
	# tally up previous points from activities
	if len(activity_list) > 0:
		for activity in activity_list:
			if activity == 'Read':
				reading_count += 1
			elif activity == 'Exercise':
				excercising_count += 1
			elif activity == 'Journal':
				journaling_count += 1
			elif activity == 'Code':
				coding_count += 1
		# all activities equal -- recommend random activity
		if reading_count == excercising_count == journaling_count == coding_count: 
			num = random.randint(0, 3)
			print("You should", activity_list[num].lower(), "for 30 minutes")
		# not equal point totals -- pick lowest category
		else: 
			if (reading_count <= excercising_count) and (reading_count <= journaling_count): 
				print("You should read for 30 minutes")
			elif (excercising_count <= reading_count) and (excercising_count <= journaling_count): 
				print("You should exercise for 30 minutes")
			elif (journaling_count <= excercising_count) and (journaling_count <= reading_count): 
				print("You should journal for 30 minutes")

if __name__ == "__main__":
    main()