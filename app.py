from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

days = ("Tuesday", "Wednesday", "Thursday")
halves = ("AM", "PM")
minutes = ("00", "15", "30", "45")

doctors = [
	{
		"id": "0",
		"first_name": "Peach",
		"last_name": "Toadstool",
		"appointments": {
			"Tuesday": {
				"10:15AM": [
					{
						"id": "0_Tuesday_10:15AM_PikaChu",
						"first_name": "Pika",
						"last_name": "Chu",
						"kind": "New Patient"
					},
					{
						"id": "0_Tuesday_10:15AM_Waluigi",
						"first_name": "Wa",
						"last_name": "Luigi",
						"kind": "Follow-up"
					}
				]
			},
			"Wednesday": {},
			"Thursday": {}
		}
	},
	{
		"id": "1",
		"first_name": "Tigger",
		"last_name": "Robin",
		"appointments": {
			"Tuesday": {},
			"Wednesday": {
				"2:00PM": [
					{
						"id": "1_Wednesday_2:00PM_WinniePooh",
						"first_name": "Winnie",
						"last_name": "Pooh",
						"kind": "New Patient"
					}
				]
			},
			"Thursday": {}
		}
	},
	{
		"id": "2",
		"first_name": "Minnie",
		"last_name": "Mouse",
		"appointments": {
			"Tuesday": {},
			"Wednesday": {},
			"Thursday": {}
		}
	},
]


class Doctors(Resource):

	def get(self):
		results = []
		for doctor in doctors:
			results.append("id {}: Dr. {} {}".format(
				doctor["id"],
				doctor["first_name"],
				doctor["last_name"]))
		return results, 200


class Doctor(Resource):
	
	# returns appointments for a doctor on a certain day
	# 404 if the doctor is not found
	# 200 with empty list if no appts that day
	def get(self, id, day):
		n = int(id)
		if not is_doctor(n):
			return "Doctor not found", 404
		if day not in days:
			return "{} invalid day".format(day), 400
		return doctors[n]['appointments'][day], 200

	
	# adds a new appointment to a doctor's calendar
	def post(self, id, day):
		parser = reqparse.RequestParser()
		parser.add_argument("time")
		parser.add_argument("first_name")
		parser.add_argument("last_name")
		parser.add_argument("kind")
		args = parser.parse_args()
		n = int(id)
		if not is_doctor(n):
			return "Doctor not found", 404
		if day not in days:
			return "{} invalid day".format(day), 400
		time = args["time"]
		if not is_good_time_format(time):
			return "{} invalid time".format(time), 400
		existing_appts = len(doctors[n]["appointments"][day])
		if existing_appts >= 3:
			return "too many appointments for {} {}".format(day, time), 400
		appt_id = "{}_{}_{}_{}{}".format(id, day, time, args["first_name"], args["last_name"])
		appt = {
			"id": appt_id,
			"first_name": args["first_name"],
			"last_name": args["last_name"],
			"kind": args["kind"]}
		if time not in doctors[n]["appointments"][day]:
			doctors[n]["appointments"][day][time] = [appt]
		else:
			doctors[n]["appointments"][day][time].append(appt)
		return appt, 201
		
	# deletes an appointment from a doctor's calendar
	def delete(self, id, day):
		parser = reqparse.RequestParser()
		parser.add_argument("appt_id")
		parser.add_argument("time")
		args = parser.parse_args()
		appt_id = args["appt_id"]
		n = int(id)
		time = args["time"]
		return doctors[n]["appointments"]
		if not is_doctor(n):
			return "Doctor not found", 404
		if day not in days:
			return "{} invalid day".format(day), 400
		if time not in doctors[n]["appointments"][day]:
			return "Appointment not found", 404
		for appt in doctors[n]["appointments"][day][time]:
			if appt["id"] == appt_id:
				doctors[n]["appointments"][day][time].remove(appt)
				return "{} is deleted".format(appt_id), 200
		return "Appointment not found", 404
		

def is_doctor(n):
	return len(doctors) > n
	

def is_good_time_format(time):
	if ':' not in time:
		return False
	hour, min_half = time.split(':')
	# check hour
	if int(hour) not in range(1,13):
		return False
	if len(min_half) != 4:
		return False
	# check minutes and AM/PM
	min = min_half[:2]
	half = min_half[2:]
	if min not in minutes or half not in halves:
		return False
	return True


api.add_resource(Doctors, "/doctors")
api.add_resource(Doctor, "/doctor/<string:id>/<string:day>")
		
app.run(debug=True)
		
		
		
		
		