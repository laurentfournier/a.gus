'''
(c) Emant Pte Ltd Sep 2011
You have a royalty-free right to use, modify, reproduce and distribute
the Sample Application Files (and/or any modified version) in any way
you find useful, provided 

1) that you agree that Emant Pte Ltd has no warranty,  obligations or 
liability for any Sample Application Files.
2) Sample Application Files (and/or any modified version) are used only
on products manufactured or licensed by Emant Pte Ltd 

Emant Pte Ltd provides programming examples for illustration only,
This sample program assumes that you are familiar with the programming
language being demonstrated and the tools used to create and debug
procedures. Emant Pte Ltd support engineers can help explain the
functionality of Emant Pte Ltd software components and associated
commands, but they will not modify these samples to provide added
functionality or construct procedures to meet your specific needs.

for Android/Emulator, Windows, Ubuntu (EMANT380) requires PyBluez
for Windows, Ubuntu (EMANT300) requires pyserial
'''

__version__  = '0.8.1'
__date__     = '$Date: 16 Dec 2011 $'

no_blue = False;
try:
    import bluetooth              
except ImportError:
    no_blue = True;

no_serial = False;
try:
    import serial              
except ImportError:
    no_serial = True;    
      
import math
import time
uuid = "00001101-0000-1000-8000-00805F9B34FB"

class Emant300:
    
    AIN0, AIN1, AIN2, AIN3, AIN4, AIN5, COM, DIODE = (0,1,2,3,4,5,8,15)
    Unipolar, Bipolar = (1,0)
    V2_5, V1_25 = (1,0)
    POC_Count, POC_PWM = (0,1)
    EOT_Timed, EOT_Event = (0,1)
    
#    AIN = (AIN0, AIN1, AIN2, AIN3, AIN4, AIN5, COM, DIODE)
#    POLARITY = (Unipolar, Bipolar)

    
    def __init__(self):
        self._HwId = ""
        self._CommOpen = False
        self._DIO_Config = 8
        self._DIO = 255
        self._Polarity = self.Unipolar
        self._Gain = 0
        self._VRef = self.V2_5
        self._ODAC = 0
        self._ADCON0 = 0x30
        self._ADCON1 = 0x41
        self._Decimation = 0x07F1
        self._ACLK = 0x10
        self._sock = None
        self._MSINT = 100

        self._EventOrTimed = self.EOT_Timed
        self._PWMOrCnt = self.POC_PWM
        
        self._Counter = 0

    def HwId(self):
        return self._HwId

    def Open(self, Comm_Port, reset=True, dev='380'):
        self._CommPort = Comm_Port
        self._device = dev 
        if (self._device=='380'):
            service_matches = bluetooth.find_service( uuid = uuid, address = Comm_Port )
            if len(service_matches) == 0:
                    self._CommOpen = False
                    return self._CommOpen

            first_match = service_matches[0]
            port = first_match["port"]
            name = first_match["name"]
            host = first_match["host"]
            # Create the client socket
            self._sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
            self._sock.connect((host, port))
            self._CommOpen = True

        if (self._device=='300'):
            self._serial = serial.Serial(Comm_Port, 115200, timeout=5)
            self._CommOpen = self._serial.isOpen

        c = '>' + self._checksum('i')
        r = self._TransactCommand(c)
        (st, id) = self._checksum_OK(r)
        self._HwId = id
        if (reset):
            self.Reset()
        return self._CommOpen

    def Close(self):
        if (self._device=='380'):
            self._sock.close()
        if (self._device=='300'):
            self._serial.close()

    # 8 bits of DIO can be configured as Input or Output
    # 1 or Input and 0 for Output
    def ConfigDIO(self, Value):
        if (Value<=255):
            self._DIO_Config = Value
            return True
        else:
            return False

    def ConfigAnalog(self, InputLimit, Polarity, SampleFreq):
        if (self._VRef == self.V2_5):
            reflimit = 2.5
        else:
            reflimit = 1.25

        if (InputLimit > reflimit):
            InputLimit = reflimit
        Gain = int(math.log(reflimit / InputLimit)/math.log(2))
        
        self._ADCON0 = self._ADCON0 & 0xF8
        self._ADCON0 = int(Gain | self._ADCON0)
        self._Gain = Gain

        self._ADCON1 = self._ADCON1 & 0xBF
        self._ADCON1 = int(Polarity << 6) | self._ADCON1
        self._Polarity = Polarity

        temp = (170/SampleFreq) - 1
        if (temp < 1):
            temp = 1

        self._ACLK = int(temp)

        # 345606.25 = 22118800 / 64
        self._Decimation = int(345606.25/((self._ACLK + 1) * SampleFreq))

        # correct for Decimation bug

        if (self._Decimation > 2047):
            self._ACLK = self._ACLK + 1
            self._Decimation = int(345606.25 / ((self._ACLK + 1) * SampleFreq))

        # end of add
        return self.ConfigAnalogAdvance()
        

    # Advance Setting for Analog Input
    def ConfigAnalogAdvance(self):
        c = ("03F" + ("%02x" % self._ODAC).upper()+ \
            ("%02x" % self._ADCON0).upper()+ ("%02x" % self._ADCON1).upper()+ \
            ("%04x" % self._Decimation).upper()+ ("%02x" % self._ACLK).upper())
        actSampFreq = 22118800/((self._ACLK + 1) * self._Decimation * 64)
        return (self._writecmd(c),actSampFreq)

    def ReadAnalogWaveform(self, PIn, NIn, NumberOfSamples):
        """ <summary>
         Read Analog Waveform
         </summary>
        """
        wavefm = []
        ai = (PIn * 16 + NIn) % 256
        c = ">" + self._checksum("v" + ("%02x" % ai).upper() + ("%04x" % NumberOfSamples).upper())
        r = self._TransactCommand(c)
        (resbool, result) = self._checksum_OK(r)
        if resbool:
            i = 0
            while i < NumberOfSamples:
                hexstr = result[i * 4: (i+1) * 4]
                rawdata = int(hexstr,16)
                if (self._Polarity == self.Bipolar):
                    if rawdata > 0x7FFF:
                        rawdata = rawdata - 0x10000
                    rawdata = rawdata * 2
                g = 1 << self._Gain
                rawdata = rawdata / g
                volt = (rawdata * 1.25 * (1 + self._VRef))/0xFFFF
                wavefm.append(volt)
                i += 1
        return wavefm

    def ReadAnalog(self, PIn, NIn):
#        if PIn not in self.AIN: raise ValueError("Not a valid input: %r" % PositiveInput)
#        if NIn not in self.AIN: raise ValueError("Not a valid input: %r" % PositiveInput)

        ai = (PIn * 16 + NIn) % 256
        c = '>' + self._checksum('t' + ("%02x" % ai).upper())
        r = self._TransactCommand(c)
        (resbool, result) = self._checksum_OK(r)
        if resbool:
            rawdata = int(result, 16)
            if (self._Polarity == self.Bipolar):
                if rawdata > 0x7FFFFF:
                    rawdata = rawdata - 0x1000000
                rawdata = rawdata * 2
            g = 1 << self._Gain
            rawdata = rawdata / g
            volt = (rawdata * 1.25 * (1 + self._VRef))/0xFFFFFF
            RawData = rawdata
        else:
            RawData = 0
        return(volt,RawData)

    # Write to IDAC
    def WriteAnalog(self, Value):
        if Value > 1:
            return False
        if Value < 0:
            return False
        temp = int(Value * 255)
        c = ('E01' + ("%02x" % temp).upper())
        return self._writecmd(c)

    def ConfigPWMCounter(self, PWMOrCnt, EventOrTimed=EOT_Timed, MSInt=100, SetCount=0):
        self._MSINT = MSInt
        self._PWMOrCnt = PWMOrCnt
        self._EventOrTimed = EventOrTimed
        temp = PWMOrCnt + EventOrTimed * 2
        if (self._PWMOrCnt == self.POC_Count) and (self._EventOrTimed == self.EOT_Event):
            c = "133" + ("%02x" % self._MSINT).upper() + ("%02x" % temp).upper() + ("%04x" % SetCount).upper()
            return self._writecmd(c)
        else:
            c = "130" + ("%02x" % self._MSINT).upper() + ("%02x" % temp).upper()
            return self._writecmd(c)

    def WritePWM(self, Period, DutyCycle):
        """ <summary>
         Write to PWM
         </summary>
        """
        Per1 = Period * 1.8432
        Dut1 = DutyCycle / 100.0
        PerH = self._DeadTimeComp(Per1 * (1 - Dut1))
        PerL = self._DeadTimeComp(Per1 * Dut1)
        c = ("EF0" + ("%04x" % PerH).upper() + ("%04x" % PerL).upper())
        return self._writecmd(c)

    def ReadCounter(self):
        """ <summary>
         Read 16 bit value from counter
         </summary>
        """
        c = ">" + self._checksum("h")
        r = self._TransactCommand(c)
        (resbool, result) = self._checksum_OK(r)
        if resbool:
            self._Counter = int(result,16)
            if (self._Counter==0):
                Period = 0.0000000001
            else:
                Period = (float(self._MSINT + 1) / self._Counter) / 1000
            return (self._Counter, Period)
        else:
            return (-1, 0)
        
    # Read state from digital bit addressed
    def ReadDigitalBit(self, Address):
        mask = 1
        self.ReadDigitalPort()
        maskresult = self._DIO & (mask << Address)
        return (maskresult <> 0)
        
    # Read 8 bit value from digital port
    def ReadDigitalPort(self):
        c = '>' + self._checksum('d')
        r = self._TransactCommand(c)
        (resbool, result) = self._checksum_OK(r)
        if resbool:
            self._DIO = int(result,16)
            return self._DIO
        else:
            return 1

    # Write to digital bit addressed
    def WriteDigitalBit(self, Address, State):
        mask = 1
        mask = mask << Address
        if State:
            maskresult = self._DIO | mask
        else:
            maskresult = self._DIO & (mask ^ 255)
        return self.WriteDigitalPort(maskresult)

    # Write 8 bit value to digital port
    def WriteDigitalPort(self, Value):
        Value = Value | self._DIO_Config
        c = 'D' + ("%02x" % Value).upper()
        if self._writecmd(c):
            self._DIO = Value
            return True
        else:
            return False

    # Reset the DAQ module
    def Reset(self):
        if (self._writecmd('R')):
            time.sleep(0.5)
            return True
        else:
            return False

    def _TransactCommand(self, sendstring):
        if (self._device=='380'):
            self._sock.send(sendstring)
            return self._bt_receive_data()
        if (self._device=='300'):
            self._serial.write(sendstring)
            return self._serial_receive_data()

    def _serial_receive_data(self):
        buffer = ""
        while 1:
            data = self._serial.read(1)
            buffer = buffer + data
            if data == '\r':
                return buffer

    def _bt_receive_data(self):
        buffer = ""
        while 1:
             data = self._sock.recv(1)
             buffer = buffer + data
             if data == '\r':
                 return buffer

    def _DeadTimeComp(self, RawValue):
        temp = 65535 + 11 - int(RawValue)
        if temp < 0:
            return 0
        elif temp > 65535:
            return 65535
        else:
            return temp

    def _writecmd(self, str_input):
        c = '>' + self._checksum(str_input)
        r = self._TransactCommand(c)
        if r[0:1] == 'A':
            return True
        else:
            return False

    def _checksum(self, str_input):
        _cs = 0
        for i in xrange(len(str_input)):
           ch=str_input[i]
           _cs = (_cs + ord(ch)) % 256
        res = str_input + ("%02x" % _cs).upper()
        return res

    def _checksum_OK(self, str_input):
        str_input = str_input[0:len(str_input)-1]
        str_output = ''
        if str_input[0:1] == 'A':
            str_output = str_input[1:len(str_input)-2]
            chksum = str_input[len(str_input)-2:len(str_input)]
            _cs = 0
            for i in xrange(len(str_output)):
                ch=str_output[i]
                _cs = (_cs + ord(ch)) % 256
            if ("%02x" % _cs).upper() == chksum:
                return (True,str_output)
        return (False,"Err")


