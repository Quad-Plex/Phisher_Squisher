# <div align="center"> 🚫Scammer_Spammer🚫

## Phishing sites getting on your nerves? Feed them fake data! Lots of it!

# <div align="center"> About

**🚫Scammer_Spammer🚫** is an easy-to-use program written in Python used to combat phishing scams by feeding them massive amounts of fake logins, thus rendering their valid logins that they phished up near impossible to find nor use, at the same time forcing them to either temporarily close the site or abandon it completely due to the massive amounts of unusable data.

# <div align="center"> Features
- Allows you to feed massive amounts of fake usernames and passwords to phishing sites.
- Uses randomly generated first names, last names, order, numbers and variable length passwords.
- Picks between different email providers to maximize legitimacy. (more can be added)
- Proxies can be used to prevent being IP blocked or to prevent IP leakage.
- Works on sites with HTTPS.
- Blocks redirects.
- **NEW!!** Multi-Threading! Spawn multiple threads performing one request per second each!
- **NEW!!** more colorful output including status code, tracking of num. of sent requests, average requests/second and more
- **NEW!!** Ability to add headers and cookie data

### Planned Features/Ideas
- Easier method of replacing URL/payload/cookie data
- continuous output in the console instead of scrolling output from the threads (would give more info when threads are stuck)
- http-code statistics to keep better track of results
- GUI interface
- saving profiles to re-use certain configurations
- Automatic rate-limiting/multi-threading determined by request throughput


# <div align="center"> Screenshot
![image](https://user-images.githubusercontent.com/39552449/135698024-4fff1846-9c60-4fe6-a463-bc108f93398a.png)
	
# <div align="center"> Usage

**Python 3.5.3 or higher is recommended**

Replace "REPLACE WITH URL" with URL to the login query.

```Python
url = 'REPLACE WITH URL'
```
For the Payload, fill "login" and "password" with the parameters specified in the POST request. You're free to add additional parameters aswell

```Python
payload = {
	'login': generated_email,
	'password': password,
	}
 ```
If proxies need to be used, uncomment this line (deleting the #) and add proxies as needed in line 71.
```Python
#s.proxies = proxies
```

# <div align="center"> Tips
- You must have the names library installed. Either install it in virtualenv or install it on your system by using pip install names (in terminal)
	
- For maximum efficiency, increase the number of threads working until you see '429' (Too Many Requests) appear in the 'Status' output - this means you're already saturating the maximum requests the server allows per single connection
	
- If you receive a 403 (Forbidden) Error this most likely means that either the Admin has manually blocked your IP from accessing their site, or an automatic anti spam detection has tripped. To circumvent this, simply use a VPN connection to appear as a new user to the site.

- Watch this video if you need help on getting the URL and form data. Start watching [here](https://youtu.be/UtNYzv8gLbs?t=40).
# <div align="center"> Inspirations
- Thanks to the original repo by W8TERM3LON [here](https://github.com/W8TERM3LON/Phisher_Squisher).

# <div align="center"> PLEASE DO NOT USE THIS FOR MALICIOUS PURPOSES.
