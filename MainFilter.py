import subprocess
import pymongo
import time
client =pymongo.MongoClient('mongodb+srv://emseccomandcenter:TUXnEN09VNM1drh3@cluster0.psiqanw.mongodb.net/?retryWrites=true&w=majority')
db=client['Telecom']
col =db['telecom_sms']

def database_dump(main_number,main_time,main_sms):
    print("Inter in database function")
    client =pymongo.MongoClient('mongodb+srv://emseccomandcenter:TUXnEN09VNM1drh3@cluster0.psiqanw.mongodb.net/?retryWrites=true&w=majority')
    db=client['Telecom']
    col =db['telecom_sms']
    dict={'number':main_number,'time':main_time,'sms':main_sms}
    col.insert_one(dict)  
    print("Data Inserted!!") 

def Scanning(Command, Type):
    print("Filtering Started...")
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
    
    filename = "ScannedData.txt"

    with open(filename, "w") as file:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        
        main_sms=''
        Year=''
        Month=''
        Day=''
        Hour=''
        Minutes=''
        Seconds=''
        Timezone=''
        main_time=''
       
        for line in iter(process.stdout.readline, b""):
            line = line.decode("utf-8")
            file.write(line)
            Line = line.strip()
            # print(Line)

            try:
                if ((Line.find('Year')) >= 0):
                    Year ='20'+Line.split(':')[1].strip()
                    # print(Year)
                if ((Line.find('Month')) >= 0):
                    Month =Line.split(':')[1].strip()
                    if(int(Month)<=9):
                        Month='0'+Month
                    else:
                        Month=Month  
                    # print(Month)      
                if ((Line.find('Day')) >= 0):
                    Day =Line.split(':')[1].strip()
                    if(int(Day)<=9):
                        Day='0'+Day
                    else:
                        Day=Day
                    # print(Day)      
                if ((Line.find('Hour')) >= 0):
                    Hour =Line.split(':')[1].strip()
                if ((Line.find('Minutes')) >= 0):
                    Minutes =Line.split(':')[1].strip()
                if ((Line.find('Seconds')) >= 0):
                    Seconds =Line.split(':')[1].strip()
                if ((Line.find('Timezone')) >= 0):
                    Timezone =Line.split(':')[1].strip()
                main_time =Year+'-'+Month+'-'+Day+'T'+Hour+':'+Minutes+':'+Seconds+" "+Timezone
                # print(main_time)
            except:pass    
            try:
                if ((Line.find('RP-Originator Address')) >= 0):   
                    main_number=Line.split('-')[2].strip() 
                    if(main_number.find('(')>=0):
                        a=main_number.lstrip('(') 
                        b=a.rstrip(')')
                        main_number=int(b)
                    else:
                        main_number=int(main_number) 
                    # print(main_number)      
            except:pass 
            try:                 
                if ((Line.find('SMS text')) >= 0):   
                    main_sms=Line.split(':')[1].strip() 
                    print(main_sms)
                    print(len(main_sms))
            except:pass        
            print("---------------------------------------------------------------") 
            print(Line)
            print("---------------------------------------------------------------") 

        print(main_sms)
        print(main_number)
        print(main_time)
        print(len(main_sms))
        print(len(main_time))

        time.sleep(1)
        if(len(main_sms)>0 or len(main_time)>0 or main_number>0): 
            time.sleep(1) 
            database_dump(main_number,main_time,main_sms)
        else:
            print("check sms size!!")    

            # client =pymongo.MongoClient('mongodb+srv://emseccomandcenter:TUXnEN09VNM1drh3@cluster0.psiqanw.mongodb.net/?retryWrites=true&w=majority')
            # db=client['Telecom']
            # col =db['telecom_sms']
            # col.insert_one(dict)  
            # print("Data Inserted!!") 
            print("************************************************")

        with open(filename, "w") as file:
               file.write(" ") 

        # process.wait()
  
Command = 2
Type = 2
while(True):
    Scanning(Command, Type)
