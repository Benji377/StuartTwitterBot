import json
import requests
import os
from keep_alive import keep_alive
from TwitterUpdate import main_file_exec
import time
from datetime import datetime, timezone, timedelta

keep_alive()

# Sets the correct timezone for replit
tz = timezone(timedelta(hours=2))

# Retrieves the current date and time
current_date = datetime.now(tz)
# Dictionary to save satellites overpass time and name
satellite_dic = {}
# API key
spectator_api_key = os.environ['API_KEY']
# Coordinates of Italy
geometry = "MULTIPOLYGON (((15.5203760108138 38.2311550969915,15.1602429541717 37.4440455185378,15.309897902089 " \
           "37.1342194687318,15.0999882341194 36.6199872909954,14.335228712632 36.9966309677548,13.8267326188799 " \
           "37.1045313583802,12.4310038591088 37.6129499374838,12.5709436377551 38.1263811305197,13.7411564470046 " \
           "38.0349655217954,14.7612492204462 38.1438736028505,15.5203760108138 38.2311550969915)),((9.21001183435627 " \
           "41.2099913600242,9.80997521326498 40.5000088567661,9.66951867029567 39.1773764104718,9.21481774255949 " \
           "39.2404733343001,8.80693566247973 38.9066177434785,8.42830244307711 39.1718470322166,8.38825320805094 " \
           "40.3783108587188,8.15999840661766 40.9500072291638,8.70999067550011 40.8999844427052,9.21001183435627 " \
           "41.2099913600242)),((12.3764852230408 46.7675591090699,13.8064754574216 46.5093061386912,13.6981099789055 " \
           "46.0167780625174,13.9376302425783 45.5910159368647,13.1416064795543 45.7366917994954,12.3285811703063 " \
           "45.3817780625148,12.3838749528586 44.8853742539191,12.2614534847592 44.600482082694,12.5892370947865 " \
           "44.0913658717545,13.5269059587225 43.5877273626379,14.029820997787 42.7610077988325,15.142569614328 " \
           "41.9551396754569,15.9261910336019 41.9613150091157,16.1698970882904 41.7402949082034,15.8893457373778 " \
           "41.5410822617182,16.7850016618606 41.1796056178366,17.5191687354312 40.8771434596322,18.3766874528826 " \
           "40.3556249049427,18.4802470231954 40.1688662786398,18.2933850440281 39.8107744410732,17.7383801612133 " \
           "40.2776710068303,16.8695959815223 40.4422346054639,16.4487431169373 39.7954007024665,17.1714896989715 " \
           "39.4246998154207,17.0528406104293 38.9028712021373,16.6350883317818 38.8435724960824,16.1009607276131 " \
           "37.9858987493342,15.6840869483145 37.908849188787,15.6879626807363 38.2145928004419,15.8919812354247 " \
           "38.7509424911992,16.1093323096443 38.9645470240777,15.7188135108146 39.5440723740149,15.4136125016988 " \
           "40.0483568385352,14.9984957210982 40.1729487167909,14.7032682634148 40.6045502792926,14.0606718278653 " \
           "40.7863479680954,13.6279850602854 41.1882872584617,12.8880819027304 41.2530895045556,12.1066825700449 " \
           "41.7045348170574,11.1919063656142 42.3554253199897,10.5119478695178 42.9314625107472,10.200028924204 " \
           "43.9200068222746,9.70248823409781 44.0362787949313,8.88894616052687 44.3663361679795,8.42856082523858 " \
           "44.2312281357524,7.8507666357832 43.7671479355552,7.43518476729184 43.6938449163492,7.54959638838616 " \
           "44.1279011093848,7.00756229007666 44.2547667506614,6.74995527510171 45.0285179713676,7.09665245934784 " \
           "45.3330988632959,6.80235517744566 45.7085798203287,6.84359297041456 45.9911465521007,7.27385094567668 " \
           "45.7769477402508,7.75599205895983 45.8244900579593,8.31662967289438 46.1636424830909,8.4899524268013 " \
           "46.0051508652517,8.96630577966783 46.0369318711112,9.18288170740311 46.440214748717,9.92283654139035 " \
           "46.3148994004092,10.3633781266787 46.4835712754098,10.4427014502466 46.8935462509974,11.0485559424365 " \
           "46.7513585475464,11.1648279150933 46.9415794948127,12.1530880062431 47.1153931748264,12.3764852230408 " \
           "46.7675591090699))) "
# GET request URL
url = 'https://api.spectator.earth/overpass/?api_key={api_key}&days_after={daysafter}&geometry={geometry}'.format(
    api_key=spectator_api_key, daysafter=1, geometry=geometry)

# Makes a request
response = requests.get(url)
# Retrieves the response
json_response = json.loads(response.text)
# Formats the string
jstring = json.dumps(json_response, indent=4)
print("Data retrieved, waiting...")

# Iterates through all retrieved satellites
for i in range(0, len(json_response["overpasses"])):
    # Retrieves satellite name and date
    satellite_name = str(json_response["overpasses"][i]["satellite"])
    satellite_date = str(json_response["overpasses"][i]["date"])

    # Formats the time-string
    new_date_f = satellite_date.replace('T', ' ')
    new_date = new_date_f.replace('Z', '')
    new_date_d = datetime.strptime(new_date, '%Y-%m-%d %H:%M:%S')
    new_date_d = new_date_d.replace(tzinfo=tz)

    # If satellite hasn't passed yet, add it to the dictionary
    if current_date < new_date_d:
        satellite_dic[new_date_d] = satellite_name

print(satellite_dic)
# An infinite loop to check for flying by satellites
while satellite_dic:
    # Check if the time of the first satellite in the dictionary is equal to the current time
    # or has already passed
    first_date_in_dic = list(satellite_dic.keys())[0]
    print("Current time: " + str(current_date) + "\nNext sat: " + str(first_date_in_dic))

    if current_date >= first_date_in_dic:
        # Send an update to Twitter
        print(satellite_dic[first_date_in_dic] + " is overpassing")
        main_file_exec('"' + satellite_dic[first_date_in_dic] + '" satellite is flying over Italy')
        # Remove the satellite from the dictionary
        satellite_dic.pop(first_date_in_dic)
    else:
        # Update the current time
        current_date = datetime.now(tz)
    # Do this every 60 seconds
    time.sleep(30)
