import asyncio, json, time, threading, websockets, os, sys, re
sys.dont_write_bytecode = True
from os.path import join, dirname
from dotenv import load_dotenv
from str2bool import str2bool
from XxTheChildPredatorxX import Captcha, RBLXWild, LoadFromEnv, check_update

check_update()

def strip(message):
    try:
        return json.loads(re.sub(r'\d+\{', '{', message))
    except:
        return json.loads(re.sub(r'\d+\[', '[', message))

print("made by Alanishere#7667 and Alii#3333")
print("v1.7")


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

APIKEY_2CAPTCHA = os.getenv("APIKEY_2CAPTCHA")

pot_id = 0

accounts = LoadFromEnv()
print(f"{len(accounts)} accounts loaded")

captcha = Captcha()
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
                print("Rain ended!")
                print(f"2Captcha bal: {captcha.Balance()}$!")

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
    print("u inerrupted the program frrr")
