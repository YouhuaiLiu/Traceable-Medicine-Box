from gpio import *
from time import *
from email import *

customWrite(1, 0)
# Get medicine box status

def onEmailReceive(sender, subject, body):
    print("Received from: " + sender)
    print("Subject: " + subject)
    print("Body: " + body)

def onEmailSend(status):
    print("send status: " + str(status))

def main():
    box_status = 0
    EmailClient.setup(
        "medicine_box@hospital.com",
        "hospital.com",
        "medicine_box",
        "123"
    )
    EmailClient.onReceive(onEmailReceive)
    EmailClient.onSend(onEmailSend)

    global count
    count = 0
    

    while True:
        if count == 0:
            sleep(2)  # 6 hours
            print("first cycle")
        elif count == 1:
            sleep(2)  # 7 hours
            print("second cycle")
        elif count == 2:
            sleep(2)  # ~6 hours
            print("third cycle")

        customWrite(1, 1)  # Hypothetical function to turn on indicator
        box_status = digitalRead(0)

        timer = 0
        while timer <= 12 and box_status == 0:
            box_status = digitalRead(0)
            if box_status != 0:
                print("box opened")
                customWrite(1, 0)  # Hypothetical turn off indicator
                EmailClient.send("medicine_management@hospital.com", "Medicine History", "Patient has taken medicine")
                print(12 - timer)
                sleep(12 - timer)
                timer = 0
                count += 1

            elif timer <= 12:
                if timer == 12:
                    print("box not opened")
                    EmailClient.send("medicine_management@hospital.com", "Medicine History", "Patient has not taken medicine")
                    customWrite(1, 0)
                    count += 1
                sleep(1)
                timer += 1
                print(timer)
                print(count)
            
                

        if count == 3:  # This should be 3 because count starts from 0 and there are 3 time intervals
            sleep(1)  # ~5 hours
            count = 0  # Reset count after completing the cycle

if __name__ == "__main__":
    main()
