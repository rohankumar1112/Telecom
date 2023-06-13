import subprocess
import datetime
import time
import os

def capture_packets():
    file_time =(datetime.datetime.now().timestamp())
    
    command_dest = "sudo tshark -i lo -x -Y 'ip.dst==127.0.0.1'"
    command_sms = "sudo tshark -i lo -x -Y 'gsm_sms'"
    command_dest_text = "sudo tshark -i lo -V -Y 'ip.dst==127.0.0.1'"
    command_sms_text = "sudo tshark -i lo -V -Y 'gsm_sms'"
    test_command = "sudo tshark -r 'sample4.pcapng' -V -Y 'gsm_sms'"
    # test_command = "sudo tshark -r 'sample.pcapng' -V -Y 'gsm_sms' | grep -A 1 'TP-User-Data'"
    
    if Command == 1 and Type == 1:
        command = command_dest
    elif Command == 2 and Type == 1:
        command = command_sms
    elif Command == 1 and Type == 2:
        command = command_dest_text
    elif Command == 2 and Type == 2:
        command = command_sms_text
    elif Command == 3 and Type == 2:
        command = test_command
    current_directory = os.getcwd()
    folder_name = 'sms_Packets'
    folder_path = os.path.join(current_directory, folder_name)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    filename = f"sms_{file_time}"
    
    complete_path = os.path.join(folder_path, filename)
        
    with open(complete_path, "w") as file:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        
        for line in iter(process.stdout.readline, b""):
            line = line.decode("utf-8")
            # file.write(line)
            Line = line.strip()
            file.write(Line)
            
        print("New packet captured in :",filename)    


while(True):
    Command = 2
    Type = 2    
    # time.sleep(2)
    capture_packets()    
    



