import requests
import schedule
import time
from datetime import datetime



base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
api_url_telegram = "https://api.telegram.org/bot2008989212:AAGpVJ1WY3jmI8uCfP4Izrho2YcRx95UM8E/sendMessage?chat_id=@__groupid__&text="
group_id = "CowinVaccineUpdatesWB"
kolkata_district_ids = [710,711,712,713,714,715,716,717,718,719,720,711,722,723,724,725,726,727,728,729,730,731,732,733,734,735,736,737,783] 

def fetch_data_from_cowin(district_id):
	query_params = "?district_id={}&date={}".format(district_id, today_date)
	final_url= base_cowin_url + query_params
	response = requests.get(final_url)
	extract_vaccine_data(response)
	#print(response.text)


def fetch_data_for_state(kolkata_district_ids):
	for district_id in kolkata_district_ids:
		fetch_data_from_cowin(district_id)


def extract_vaccine_data(response):
	response_json=response.json()
	for center in response_json["centers"]:
		message=""
		for session in center["sessions"]:
			if session["available_capacity_dose1"] > 0 or session["available_capacity_dose2"] > 0:
				message += "---------***---------\nDistrict: {}\nBlock: {}\nPincode: {}\nDate: {}\nVaccine name: {}\nAge: {}\nType: {} \nDose 1: {}, Dose 2: {}\nSlots: {}\n---------***---------".format(
					center["district_name"], center["block_name"], center["pincode"],session["date"],session["vaccine"],session["min_age_limit"],center["fee_type"],session["available_capacity_dose1"],session["available_capacity_dose2"],session["slots"] )
		send_message_telegram(message)

def send_message_telegram(message):
	final_telegram_url = api_url_telegram.replace("__groupid__", group_id)
	final_telegram_url = final_telegram_url + message
	response = requests.get(final_telegram_url)
	print(response)



if __name__ == "__main__":
	schedule.every(10).seconds.do(lambda: (fetch_data_for_state(kolkata_district_ids)))
	#schedule.every().day.at("10:30").do(lambda: (fetch_data_for_state(kolkata_district_ids)))
	#schedule.every().hour.do(lambda: (fetch_data_for_state(kolkata_district_ids)))
	while True:
		schedule.run_pending()
		time.sleep(1)
	

