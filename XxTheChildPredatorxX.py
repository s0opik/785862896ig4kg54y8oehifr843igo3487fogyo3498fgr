import sys, os, time, requests, hashlib
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
        new_session = RBLXWild()
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
