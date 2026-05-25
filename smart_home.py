import time
import random
import requests
import smtplib
import imaplib
import email
from email.mime.text import MIMEText

WRITE_API_KEY = "YDWP0OZ5EPRIJR29"
READ_API_KEY = "APP_PASSWORD"
CHANNEL_ID = "3353290"

THINGSPEAK_WRITE_URL = "https://api.thingspeak.com/update"
THINGSPEAK_READ_URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"

EMAIL = "Sarazivkovic10042003@gmail.com"
PASSWORD = "xiifxdjwnftgnipu"  

LIGHT_THRESHOLD = 307  # 30% od 1023

light_system = True
fan_system = True
pir_system = True
garage_system = True
emergency_mode = False

light_auto = True
fan_on = False

last_pir = 0
last_emergency = 0
last_pir_mail_time = 0

PIR_MAIL_COOLDOWN = 30

motion_count = 0
garage_open_count = 0


def send_mail(subject, message):
    msg = MIMEText(message, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        print("MAIL POSLAT ✅")
    except Exception as e:
        print("GRESKA PRI SLANJU MAILA:", e)


def process_subject(subject):
    global light_system, fan_system, pir_system, garage_system
    global emergency_mode, light_auto

    subject = subject.strip().upper()

    if subject == "LIGHT ON":
        light_system = True
        light_auto = False
    elif subject == "LIGHT OFF":
        light_system = False
        light_auto = False
    elif subject == "LIGHT AUTO ON":
        light_system = True
        light_auto = True
    elif subject == "LIGHT AUTO OFF":
        light_auto = False
    elif subject == "FAN ON":
        fan_system = True
    elif subject == "FAN OFF":
        fan_system = False
    elif subject == "PIR ON":
        pir_system = True
    elif subject == "PIR OFF":
        pir_system = False
    elif subject == "GARAGE ON":
        garage_system = True
    elif subject == "GARAGE OFF":
        garage_system = False
    elif subject == "EMERGENCY OFF":
        emergency_mode = False
    else:
        return

    print("MAIL KOMANDA:", subject)


def check_email_commands():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")
        if status != "OK":
            mail.logout()
            return

        for num in messages[0].split():
            _, data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])
            subject = msg.get("Subject", "")
            process_subject(subject)

        mail.logout()

    except Exception as e:
        print("GRESKA PRI CITANJU MAILA:", e)


def upload_to_thingspeak(light, temp, pir, distance, fan, emergency):
    payload = {
        "api_key": WRITE_API_KEY,
        "field1": light,
        "field2": temp,
        "field3": pir,
        "field4": distance,
        "field5": fan,
        "field6": emergency,
    }

    try:
        response = requests.post(THINGSPEAK_WRITE_URL, data=payload, timeout=10)
        print("ThingSpeak:", response.status_code)
    except Exception as e:
        print("GRESKA THINGSPEAK:", e)


def send_daily_report_from_thingspeak():
    try:
        params = {
            "api_key": READ_API_KEY,
            "results": 8000
        }

        response = requests.get(THINGSPEAK_READ_URL, params=params, timeout=10)
        data = response.json()
        feeds = data.get("feeds", [])

        temps = []
        lights = []
        daily_motion = 0
        daily_garage = 0

        for feed in feeds:
            if feed.get("field1") is not None:
                lights.append(float(feed["field1"]))

            if feed.get("field2") is not None:
                temps.append(float(feed["field2"]))

            if feed.get("field3") == "1":
                daily_motion += 1

            if feed.get("field4") is not None and float(feed["field4"]) < 10:
                daily_garage += 1

        report = "DNEVNI IZVESTAJ\n\n"

        if temps:
            report += f"Temperatura min: {min(temps)} C\n"
            report += f"Temperatura max: {max(temps)} C\n"
            report += f"Temperatura prosek: {round(sum(temps) / len(temps), 2)} C\n\n"

        if lights:
            report += f"Osvetljenost min: {min(lights)}\n"
            report += f"Osvetljenost max: {max(lights)}\n"
            report += f"Osvetljenost prosek: {round(sum(lights) / len(lights), 2)}\n\n"

        report += f"Ukupan broj otvaranja garaze: {daily_garage}\n"
        report += f"Ukupan broj detektovanih pokreta: {daily_motion}\n"

        send_mail("Dnevni izvestaj Smart Home", report)

    except Exception as e:
        print("GRESKA DNEVNI IZVESTAJ:", e)


for i in range(30):
    check_email_commands()

    light = random.randint(0, 1023)
    temp = round(random.uniform(20, 70), 2)

    pir = 1 if ((pir_system or emergency_mode) and random.random() < 0.4) else 0
    distance = random.randint(2, 50)

    # simulacija emergency dugmeta
    if random.random() < 0.03:
        emergency_mode = True

    if emergency_mode:
        light_output = 0
        fan_on = False
        garage_open = 0
        pir_effective = pir
    else:
        if pir_system and pir == 1:
            light_output = 0
        elif light_system:
            if light_auto:
                light_output = 1 if light < LIGHT_THRESHOLD else 0
            else:
                light_output = 1
        else:
            light_output = 0

        if fan_system:
            if temp > 30:
                fan_on = True
            elif temp < 24:
                fan_on = False
        else:
            fan_on = False

        garage_open = 1 if garage_system and distance < 10 else 0
        pir_effective = pir if pir_system else 0

    fan = 1 if fan_on else 0
    emergency = 1 if emergency_mode else 0

    print(f"\n----- MERENJE {i + 1} -----")
    print("Light:", light)
    print("Light output:", light_output)
    print("Temp:", temp)
    print("PIR:", pir_effective)
    print("Distance:", distance)
    print("Garage open:", garage_open)
    print("Fan:", fan)
    print("Emergency:", emergency)

    upload_to_thingspeak(light, temp, pir_effective, distance, fan, emergency)

    current_time = time.time()

    if pir_effective == 1 and last_pir == 0:
        motion_count += 1
        print("ALARM: pokret")

        if current_time - last_pir_mail_time > PIR_MAIL_COOLDOWN:
            send_mail("ALARM: Pokret", "Detektovan je pokret u pametnom domu.")
            last_pir_mail_time = current_time

    if emergency == 1 and last_emergency == 0:
        print("ALARM: Emergency")
        send_mail("ALARM: Emergency", "Aktiviran je sistem za hitne slucajeve.")

    if garage_open == 1:
        garage_open_count += 1

    last_pir = pir_effective
    last_emergency = emergency

    time.sleep(15)


send_daily_report_from_thingspeak()