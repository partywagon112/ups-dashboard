import subprocess
import time


SAMPLE = "b'\nThe UPS information shows as following:\n\n\tProperties:\n\t\tModel Name................... VP700ELCD\n\t\tFirmware Number.............. BF01911B5Q1.x\n\t\tRating Voltage............... 230 V\n\t\tRating Power................. 390 Watt\n\n\tCurrent UPS status:\n\t\tState........................ Normal\n\t\tPower Supply by.............. Utility Power\n\t\tUtility Voltage.............. 234 V\n\t\tOutput Voltage............... 234 V\n\t\tBattery Capacity............. 100 %\n\t\tRemaining Runtime............ 70 min.\n\t\tLoad......................... 50 Watt(13 %)\n\t\tLine Interaction............. None\n\t\tTest Result.................. Passed at 2022/10/31 08:14:17\n\t\tLast Power Event............. None\n\n'"

PROPERTIES_PARAMETERS = {
    "Model Name": "",
    "Firmware Number": "",
    "Rating Voltage": "",
    "Rating Power": ""
}

CONFIG_PARAMETERS = {
    "Alarm",
    "Hibernate",
    "Cloud"
}

STATUS_PARAMETERS = {
    "Time": "",
    "State": "",
    "Power Supply by": "",
    "Utility Voltage": "",
    "Output Voltage": "",
    "Battery Capacity": "",
    "Remaining Runtime": "",
    "Load": "",
    "Line Interaction": "",
    "Test Result": "",
    "Last Power Event": "",
}

class UPS():
    def __init__(self, max_logs:int = 1000):

        self.model_name = ""
        self.firware_number = ""
        self.rating_voltage = ""
        self.rating_power = ""

        self.log = [None]*max_logs

    def parse_fields(self, text):
        lines = text.split('\n')

        fields = []

        for line in lines:
            # if len(line) > 1 and line[-1] == '.':
                
            new_line = line.split('.')
            while '' in new_line: new_line.remove('')
            
            if len(new_line) == 2:
                parameter = new_line[0].replace('\t', '')
                data = new_line[1][1:]
                
                fields.append((parameter, data))
        return fields

    def read_status(self):
        # this will need sudo.
        command = ['sudo', 'pwrstat', '-status']

        # https://stackoverflow.com/questions/8217613/how-to-get-data-from-command-line-from-within-a-python-program
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        text = p.stdout.read()
        retcode = p.wait()

        new_log = STATUS_PARAMETERS
        new_log["Time"] = time.time()

        for field in self.parse_fields(text):
            if field[0] in STATUS_PARAMETERS:
                new_log[field[0]] = field[1]
        self.log.insert(0, new_log)
        self.log.pop()

ups = UPS()
ups.read_status()