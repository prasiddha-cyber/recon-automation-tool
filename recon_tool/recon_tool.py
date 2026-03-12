import os
import socket
import random
import string
import requests
import qrcode
import barcode
from barcode.writer import ImageWriter
import phonenumbers
from phonenumbers import geocoder, carrier, timezone


def ip_scanner():
    subnet = input("Enter subnet (e.g., 192.168.1.): ")

    for i in range(1, 255):
        ip = f"{subnet}{i}"

        response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null")

        if response == 0:
            print(f"{ip} is up")


def port_scanner():
    target = input("Enter target IP: ")

    for port in range(1, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        result = sock.connect_ex((target, port))

        if result == 0:
            print(f"Port {port} is open")

        sock.close()


def barcode_generator():
    data = input("Enter data to encode in barcode: ")

    code = barcode.get('code128', data, writer=ImageWriter())

    filename = code.save("barcode")

    print(f"Barcode saved as {filename}.png")


def qr_generator():
    data = input("Enter data to encode in QR Code: ")

    img = qrcode.make(data)

    img.save("qrcode.png")

    print("QR Code saved as qrcode.png")


def password_generator():
    length = int(input("Enter password length: "))

    chars = string.ascii_letters + string.digits + string.punctuation

    password = ''.join(random.choice(chars) for _ in range(length))

    print(f"Generated password: {password}")


def wordlist_generator():
    base = input("Enter base word: ")
    num_range = int(input("How many variations?: "))

    with open("wordlist.txt", "w") as f:
        for i in range(num_range):
            f.write(f"{base}{i}\n")

    print("Wordlist saved as wordlist.txt")


def phone_lookup():
    number = input("Enter phone number with country code: ")

    phone = phonenumbers.parse(number)

    print("Location:", geocoder.description_for_number(phone, 'en'))
    print("Carrier:", carrier.name_for_number(phone, 'en'))
    print("Timezone:", timezone.time_zones_for_number(phone))


def subdomain_checker():
    domain = input("Enter main domain (e.g. example.com): ")

    with open("wordlists/subdomains.txt") as f:
        subdomains = f.read().splitlines()

    for sub in subdomains:
        url = f"http://{sub}.{domain}"

        try:
            res = requests.get(url)

            print(f"Found: {url} (Status: {res.status_code})")

        except requests.ConnectionError:
            pass


def menu():

    print("""
Recon Automation Tool

1. IP Scanner
2. Port Scanner
3. Barcode Generator
4. QR Code Generator
5. Password Generator
6. Wordlist Generator
7. Phone Number Info
8. Subdomain Checker
0. Exit
""")


while True:

    menu()

    choice = input("Select an option: ")

    if choice == '1':
        ip_scanner()

    elif choice == '2':
        port_scanner()

    elif choice == '3':
        barcode_generator()

    elif choice == '4':
        qr_generator()

    elif choice == '5':
        password_generator()

    elif choice == '6':
        wordlist_generator()

    elif choice == '7':
        phone_lookup()

    elif choice == '8':
        subdomain_checker()

    elif choice == '0':
        break
