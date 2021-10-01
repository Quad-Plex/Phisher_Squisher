# <div align="center"> 🚫Phish🚫

## Phishing sites getting on your nerves? Feed them fake data! Lots of it!

# <div align="center"> About

**🚫Phish🚫** is a easy to use program written in Python used to combat phishing scams by feeding them massive amounts of fake logins, thus rendering their valid logins that they phished up near impossible to find nor use, at the same time forcing them to either temporarily close the site or abandon it completely due to the massive amounts of unusable data.

# <div align="center"> Features
- Allows you to feed massive amounts of fake usernames and passwords to phishing sites.
- Uses randomly generated first names, last names, order, numbers and variable length passwords.
- Picks between 9 different email providers to maximize legitimacy. (more can be added)
- Other parameters can also be included such as screen size and window resolution to further confuse up the scammers.
- Proxies can be used to prevent being IP blocked or to prevent IP leakage.
- Works on sites with HTTPS.
- Blocks redirects.
- **NEW!!** Multi-Threading! Spawn multiple threads with an http.post request every 1 second by typing '+' and pressing Enter
- **NEW!** more colorful output including status code and tracking of num. of sent requests

# <div align="center"> Screenshot
![image](https://user-images.githubusercontent.com/39552449/135675406-7c8eabae-33d9-4fe0-bcca-4571c8745161.png)
	
# <div align="center"> Usage

# Python

**Python 3.5.3 or higher is recommended**

Navigate to line 31, and replace "REPLACE WITH URL" with URL to the login query.

```Python
    url = 'REPLACE WITH URL'
```
Navigate to lines 84-86 and replace "login" and "password" with the parameters specified in the POST request. You're free to add additional parameters aswell

```Python
    req=s.post(url, allow_redirects=False, verify=False, data={
		'login': username,
		'password': password,
	})
 ```
If proxies need to be used, uncomment line 25 (deleting the #) and add proxies as needed lines 17.
```Python
#s.proxies = proxies
```

# <div align="center"> Tips
- You must have the names library installed. Either install it in virtualenv or install it on your system by using pip install names (in terminal)

- Watch this video if you need help on getting the URL and form data. Start watching [here](https://youtu.be/UtNYzv8gLbs?t=40).
# <div align="center"> Inspirations
- Thanks to the original repo by W8TERM3LON [here](https://github.com/W8TERM3LON/Phisher_Squisher).

# <div align="center"> PLEASE DO NOT USE THIS FOR MALICIOUS PURPOSES.
