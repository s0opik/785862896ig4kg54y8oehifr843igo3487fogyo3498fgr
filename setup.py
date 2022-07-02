import os, sys

print("Creating .env file..")

try:
    env_file = open(".env", "x")
except:
    env_file = open(".env", "w")

env_file.write(
"""# 2captcha
APIKEY_2CAPTCHA=your2captchaapikey (go to https://2captcha.com )

# Accounts
USERNAME1=roblockusername
AUTHTOKEN1=authtoken (go to https://rblxwild.com log in click ctrl+shift+i click the applications tab select local storage click rblxwild then click authtoken and copy stuff)
SESSION1=session ((go to https://rblxwild.com log in click ctrl+shift+i click the applications tab select cookies click rblxwild then click session and copy stuff)
USERAGENT1=useragent (get yo useragent here https://www.whatismybrowser.com/detect/what-is-my-user-agent/ and copy it)
PROXY1=proxy (idk get it yourself)

# Delete everything down there if you only use 1 account (This script supports multiple accounts. Max I tested is 3)
USERNAME1=roblockusername
AUTHTOKEN1=authtoken (go to https://rblxwild.com log in click ctrl+shift+i click the applications tab select local storage click rblxwild then click authtoken and copy stuff)
SESSION1=session ((go to https://rblxwild.com log in click ctrl+shift+i click the applications tab select cookies click rblxwild then click session and copy stuff)
USERAGENT1=useragent (get yo useragent here https://www.whatismybrowser.com/detect/what-is-my-user-agent/ and copy it)
PROXY1=proxy (idk get it yourself)
""")

env_file.close()
print("Successfully created .env file!")

print("Installing requirements..")
os.system(f"{sys.executable} -m pip install -r requirements.txt")
print("Successfully installed requirements!")

print("Ready!")