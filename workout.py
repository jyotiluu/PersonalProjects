import datetime 
import time

def main():
	current_date = datetime.datetime.now().strftime("%m-%d-%Y")
	workout_completed = ""
	print("1. 10 pushups \n2. 10 situps \n3. 10 squats")
	workout_input = input("Enter what you completed: ")
	if workout_input == "1": 
		workout_completed = "10 Pushups completed on: "
	elif workout_input == "2": 
		workout_completed = "10 Situps completed on: "
	elif workout_input == "3": 
		workout_completed = "10 Squats completed on: "
	else:
		print("Invalid input")
		exit()
	workout_data = workout_completed + current_date
	print(workout_data)
	file = open("workout_log.txt", "a")
	file.write(workout_data + "\n")

if __name__ == "__main__":
	main()
