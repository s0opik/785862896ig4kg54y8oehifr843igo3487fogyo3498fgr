import asyncio, json, time, threading, websockets, os, sys, re, requests, hashlib
sys.dont_write_bytecode = True
from os.path import join, dirname
from dotenv import load_dotenv
from str2bool import str2bool
from twocaptcha import TwoCaptcha, api

class Cumtcha:
    APIKey = None

    def ErrorHandler(self, error):
        error = error.__str__()

        if error == "ERROR_WRONG_USER_KEY":
            return True, "Key must be 32 characters long."
        elif error == "ERROR_KEY_DOES_NOT_EXIST":
            return True, "Key doesn't exist."
        elif error == "ERROR_ZERO_BALANCE":
            return True, "You got no money on 2captcha."
        elif error == "ERROR_PAGEURL":
            return True, "'pageurl' parameter is missing in your request."
        else:
            return False, f"Unknown error ({error})"

    def Balance(self):
        solver = TwoCaptcha(self.APIKey)
        try:
            result = solver.balance()
        except api.ApiException as e:
            should_exit, message = self.ErrorHandler(e)
            print(message)
            if should_exit:
                quit()
            return 0.00
        except Exception as e:
            print(e)
            return 0.00
        else:
            return result

    def Solve(self):
        solver = TwoCaptcha(self.APIKey)

        try:
            result = solver.hcaptcha(
                sitekey="30a8dcf5-481e-40d1-88de-51ad22aa8e97",
                url="https://rblxwild.com",
            )

        except api.ApiException as e:
            should_exit, message = self.ErrorHandler(e)
            print(message)
            if should_exit:
                quit()
            return False

        except Exception as e:
            print(e)
            return False
        else:
            return result

class ROBLOCKSWELD:
    username = None
    authToken = None
    session = None
    useragent = None
    proxy = None

    def Join(self, potId, captchaToken):
        headers = {
            "User-Agent": self.useragent,
            "Accept-Language": "en-US,en;q=0.5",
            "Authorization": self.authToken,
            "Origin": "https://rblxwild.com",
            "DNT": "1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
            "TE": "trailers"
    }

        cookies = {
            "session": self.session
        }

        json = {
            "captchaToken": captchaToken, 
            "potId": potId, 
            "i1oveu": True
        }

        try:
            response = requests.post("https://rblxwild.com/api/events/rain/join", json=json, headers=headers, cookies=cookies)
        except Exception as e:
            print(e)
            return False
        else:
            return response

def LoadFromEnv():
    sessions = []

    count = 1
    while os.getenv(f"USERNAME{count}") != None:
        new_session = ROBLOCKSWELD()
        new_session.username = os.getenv(f"USERNAME{count}")
        new_session.authToken = os.getenv(f"AUTHTOKEN{count}")
        new_session.session = os.getenv(f"SESSION{count}")
        new_session.useragent = os.getenv(f"USERAGENT{count}")
        new_session.proxy = os.getenv(f"PROXY{count}")

        sessions.append(new_session)
        
        count += 1
    
    return sessions

repository = "s0opik/785862896ig4kg54y8oehifr843igo3487fogyo3498fgr"

def create_file(path, data):
    try:
        file = open(path, "x")
        file.write(data)
        file.close()
    except Exception as e:
        print(e)
        return

def write_file(path, data):
    try:
        file = open(path, "w")
        file.write(data)
        file.close()
    except Exception as e:
        print(e)
        return

def read_file(path):
    try:
        file = open(path, "r")
        data = file.read()
        file.close()
    except Exception as e:
        print(e)
        return False
    else:
        return data

def get_files():
    try:
        response = requests.get(f"https://api.github.com/repos/{repository}/contents")
    except Exception as e:
        print(e)
        return False
    else:
        if "message" in response.json():
            print("API rate limit.")
            return False

        return response.json()

def download_file(file_name):
    try:
        response = requests.get(f"https://raw.githubusercontent.com/{repository}/main/{file_name}")
    except Exception as e:
        print(e)
        return False
    else:
        return response.text

def get_current():
    version = read_file("VERSION")

    if version:
        return float(version)
    else:
        return 0.0

def is_updated():
    return get_current() >= get_latest()

def get_latest():
    version = download_file("VERSION")

    if version:
        return float(version)
    else:
        return 0.0

def is_same(data1, data2):
    hash1 = hashlib.sha1(data1.encode()).hexdigest()
    hash2 = hashlib.sha1(data2.encode()).hexdigest()

    return hash1 == hash2

def update():
    files = get_files()
    if files:
        for file in files:
            local_file = read_file(file["name"])
            remote_file = download_file(file["name"])

            if remote_file and local_file:
                remote_data = remote_file.replace("\r\n", "\n")
                local_data = local_file.replace("\r\n", "\n")

                if not is_same(local_data, remote_data):
                    write_file(file["name"], remote_data)

            elif remote_file:
                remote_data = remote_file.replace("\r\n", "\n")
                create_file(file["name"], remote_data)

def check_update():
    if not is_updated():
        update()
        os.system(f"{sys.executable} {' '.join(sys.argv)}")

check_update()

def strip(message):
    try:
        return json.loads(re.sub(r'\d+\{', '{', message))
    except:
        return json.loads(re.sub(r'\d+\[', '[', message))

print("made by Alanishere#7667 and Alii#3333")
print("v1.9")


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

APIKEY_2CAPTCHA = os.getenv("APIKEY_2CAPTCHA")

pot_id = 0

accounts = LoadFromEnv()
print(f"{len(accounts)} accounts loaded")

captcha = Cumtcha()
captcha.APIKey = APIKEY_2CAPTCHA

def join_pot(account, pot_id):
    captcha_result = captcha.Solve()

    if captcha_result:
        pot_result = account.Join(pot_id, captcha_result["code"])
        if pot_result and pot_result.json()["success"]:
            print("Successfully joined rain [%s]"%account.username)
        else:
            print("Error while joining rain [%s]"%account.username)

async def handle_msg(websocket):
    async for message in websocket:
        msg = strip(message)

        if message == "2":
            await websocket.send("3")

        elif type(msg) is list and msg[0] == "authenticationResponse":
            pot_id = msg[1]["events"]["rain"]["pot"]["id"]
        
        elif type(msg) is list and msg[0] == "events:rain:setState":
            if msg[1]["newState"] == "ENDING":
                
                for account in accounts:
                    t = threading.Thread(target=join_pot, args=(account,pot_id))
                    t.start()


            elif msg[1]["newState"] == "ENDED":
                pot_id += 1
                print("Rain ended.")
                print(f"2Captcha balance: {captcha.Balance()}$!")

async def async_main(uri):
    async for websocket in websockets.connect(uri):
        try:
            await websocket.send("40")
            time.sleep(3)
            await websocket.send("42"+json.dumps([
                "authentication",
                {
                    "authToken": None,
                    "clientTime": int(time.time())
                }
            ]))

            await handle_msg(websocket)
        except websockets.ConnectionClosed:
            continue


try:
    asyncio.run(async_main("wss://rblxwild.com/socket.io/?EIO=4&transport=websocket"))
except KeyboardInterrupt:
    print("u interrupted the program frrr.")
