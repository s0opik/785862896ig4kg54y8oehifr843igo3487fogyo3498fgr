import os, time, requests
from twocaptcha import TwoCaptcha, api

class Captcha:
    APIKey = None

    def ErrorHandler(self, error):
        error = error.__str__()

        if error == "ERROR_WRONG_USER_KEY":
            return True, "You've provided key parameter value in incorrect format, it should contain 32 symbols."
        elif error == "ERROR_KEY_DOES_NOT_EXIST":
            return True, "The key you've provided does not exists."
        elif error == "ERROR_ZERO_BALANCE":
            return True, "You don't have funds on your account."
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

class RBLXWild:
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
