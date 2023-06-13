import subprocess
import asyncio

async def get_all(channel):
	command = f"kal -s {channel}"
	
	filename = "Kalibratefile.txt"
	
	scannedList=[]
	
	with open(filename, "w") as file:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
        
            for line in iter(process.stdout.readline, b""):
                line = line.decode("utf-8")
                file.write(line)
                Line=line.strip()
                print(Line)
                if(Line.find('GSM-900')>0):
                    scannedList=[]
                scannedList.append(Line)  
        	
        	
            process.wait()
            print(scannedList)
            return(scannedList)
	# print("Capture complete. Packets saved to", filename)

async def max_freq(lst):
    frequency_lst=[]
    Power_lst =[]
    for i in lst:
        if(i.find('MHz')>0):
            frequency=float(i.split('(')[1].split('MHz')[0].strip())
            frequency_lst.append(frequency)
            power =float(i.split('power:')[1].strip())
            Power_lst.append(power)

    max_power_index=Power_lst.index((max(Power_lst)))
    print("The maximum power Frequency is: ",frequency_lst[max_power_index]," of power ",max(Power_lst))
    return frequency_lst[max_power_index]

async def livemon(freq1): 
    print("starting Livemon...") 
    freq =freq1
    # gain =int(input("Enter the gain :"))
    gain =40
    
    command = f"grgsm_livemon -f {freq}e6 -g {gain}"
    filename = "captured_packets.txt"

    print("Scanning Started at frequency: ",freq1," Mhz")
    with open(filename, "w") as file:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        for line in iter(process.stdout.readline, b""):
            line = line.decode("utf-8")
            file.write(line)
            print(line.strip()) 

        process.wait()

    print("Capture complete. Packets saved to", filename)

def Scanning(Command,Type):
	
	command_dest ="sudo tshark -i lo -x -Y 'ip.dst==127.0.0.1'"
	command_sms ="sudo tshark -i lo -x -Y 'gsm_sms'"
	command_dest_text ="sudo tshark -i lo -V -Y 'ip.dst==127.0.0.1'"
	command_sms_text ="sudo tshark -i lo -V -Y 'gsm_sms'"
	
	if(Command == 1 and Type==1):
		command =command_dest
	elif(Command==2 and Type ==1):
		command =command_sms	
	elif(Command==1 and Type ==2):
		command =command_dest_text
	elif(Command==2 and Type ==2):
		command =command_sms_text		

	filename = "ScannedData.txt"
	
	with open(filename, "w") as file:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
        
            for line in iter(process.stdout.readline, b""):
                line = line.decode("utf-8")
                file.write(line)
                Line=line.strip()
                print(Line)
            	
            process.wait()

  
async def run_functions(channel):
    ScannedList=await get_all(channel)
    Max_freq =await max_freq(ScannedList)
    await livemon(Max_freq)  

channel=''    
# channel_code=int(input("Enter the channel code (1.GSM900 , 2.GSM1800 , 3.GSM1900)"))
channel_code =1
if(channel_code==1):
    channel ='GSM900'
elif(channel_code==2):
    channel='GSM1800'
elif(channel_code==3):
    channel='GSM1900'
else:
    print("Wrong code...")                

# Scanning(Command =2,Type=2)
asyncio.run(run_functions(channel))

