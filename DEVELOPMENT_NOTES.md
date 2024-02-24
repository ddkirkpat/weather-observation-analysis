# Development Notes 
This project is created as a take home interview project to evaluate candidates on their ability to interact with external APIs and process the resulting data. The challenge is standardized across all applicants to ensure an unbiased comparison.

## Problem Statement and Objective:
Your task is to use the NWS (National Weather Service) API to gather weather observations for the closest station to a given location (e.g., city or zip code) and
display relevant weather metrics from the available historical data.

### Requirements:
1. Query the NWS API to identify the closest weather station to a given location.
2. Fetch the available historical weather observations from this station.
3. Extract daily high and low temperatures from these observations.
4. Display the high and low temperatures for each day from the fetched data.

Try to timebox to 2 hours or less

While you may use libraries for API calls, try to limit external dependencies for data processing. If you're using an uncommon language or library, please
provide brief documentation or comments explaining your choice and its usage.

### Acceptance Criteria:
Efficient interaction with the NWS API.
Clear and concise code.
Proper error handling, especially for potential issues like API rate limits or data inconsistencies.
Provide unit tests that ensure the effective operation of your code and highlight its testability.

### Note:
You can use the following programming languages for this challenge: C#, Java, JavaScript/TypeScript, or Python. Ensure that your solution is easily runnable
by our team. If any specific setup or environment is needed, please provide detailed instructions.

Responses may be submitted as a link to a GitHub repository or as a zip file containing your code.

### Links:
[NWS (National Weather Service) API](https://www.weather.gov/documentation/services-web-api)

## Proposed Solution and Development Log
The following is an attempt to explain the critical thinking processes that I engaged to attempt a working program within the alotted time (~2 hours or less).

### Breaking down the problem
First, I needed to determine the most efficient method to quick learn and assess the [NWS (National Weather Service) API](https://www.weather.gov/documentation/services-web-api). I decided to lean into the requirements in reverse order. This would optimize my effort to ascertain and assemble what API inputs I would need at each data parsing step, while also allowing me to define functionality of each python function. Further, this analysis pattern would inclusively optimize my design to minimize my API calls. Finally, this design pattern would reduce my time spent recursively iterating my data structures. This approach resulted in the subtasks listed below.

1. I could get temperatures and associated timestamps from the observationStations endpoint using the Gridpoint schema, https://api.weather.gov/gridpoints/<gridId>/<gridX>,<gridY>/stations
2. I could get gridId, gridX, and gridY values from the points endpoint using the Point schema, https://api.weather.gov/points/<latitude>,<longitude>
3. I would need to get latitude and longitude from a geocoding API as the NWS API did support that functionality. I considered the [openGSA location-public API](https://open.gsa.gov/api/location-public-api/#look-up-cities), but it has very strict authorization key requirements that I did not have time to figure out. I chose the US Census API because it was freely available and did not require authentication keys for my level of requests.  However, in order to meet the requirement of inputing either the city or zipcode; it became clear that I would need a custom local parser for that. I decided to set that strict requirement aside till later based on time constraints.The easiest solution to a working geocoding function was to force input to use the /onelineaddress search type on [Census Geocoding Services API](https://www.census.gov/data/developers/data-sets/Geocoding-services.html_).
4. Now, I could get latitude and longitude from the geocoder endpoint using the `/locations` return type and `/onelineaddress` search type, https://geocoding.geo.census.gov/geocoder/locations/onelineaddress/{'address': <oneline US address>,'benchmark': 'Public_AR_Current','format': 'json'}
5. Now, I had all my data collection APIs in order.
6. I started to now build my functions one by one, verifying that my variables were correct for my fixed /onelineaddress input, parsing incoming json responses as requoired to destill my needed input values.
7. Once, I was finished with API response parsing within the final function, I needed to now prepare the acquired data for required display. I considered using pandas for the manipulating the data, but I wanted to adhere to the requirement to limit external dependencies for data processing. So, I chose to stick with default dictionaries to allow me to define the nested data dictionaries facilitating avoiding KeyErrors from empty dictionary keys. Also, the use of lambdas with the flout([inf,-inf]) facilitated bounded contexts for high and low value fields within the nested dictionary.
8. All primary functionality complete; it was time to focus on displaying the high and low temperatures for each day from the fetched data. Already at the two hour mark, I decided that I needed to simplify the code and decided to utilize the `tabulate` module. Adding headers using tabulate() the applicaiton was fully functional.
9. At this point, I added try exception statements to wrap API requests and data parsing for errors handling. While really basic at this point, I figured that I could customize the exception errors after studying the API more outside of the initial assignment.
10. Lastly, I cleaned up the pyenv virtualenv, exporting the required pip modules with `pip freeze > requirements.txt`.
11. Next, I setup the GitHub repository, committing code and then pushing up to main branch. I then created a dev branch and sandbox branch. I setup main branch as protected to create a simple github flow to utilize to submit any further changes into main via pull requests. Found a bunch of typos and such, performing general cleanup.
12. Next, I set to task to create pytest unit tests for each of the main program functions, creating mocks to facilitate both valid and invalid checks. In one of my unit tests, I ran into an interesting UnboundLocalError. If I moved the functions return state insidetry except statements, then the invalid test would pass. I determined that I needed to change the jltest to look for the API 400 error. 
13. Due to time constraints, I created a repositroy issue for this unit test bugfix for pathcing later.