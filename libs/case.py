# VERSION 1 using RPi plus AB Electronics ADC v1.0 Board with RS components Stock#647-9991 Thermistor
# jojopi volt_to_ohm() and equation with unmofified ABCD parameters (worked fine on my thermister)
def ohm_to_celsius(x):
  A               = 0.00116597
  B               = 0.000220635
  C               = 1.81284e-06
  D               = 2.73396e-09
  r = math.log(x)
  return 1.0 / (A + B*r + C*r**2 + D*r**3) - 273.15

# calculate the resistence of the thermistor and compensate for voltage divider in the ADC aboard
def volt_to_ohm(V):
  Rd = 10000
  Rd_effective = (Rd * 16800.0) / (Rd + 16800.0)
  Rth = (5.0 - V) / V * Rd_effective
  return Rth

# read CHANNEL 1 on the ADC board
ADC1=getadcreading(adc_address1, adc_channel1)
ohm=volt_to_ohm(ADC1)
result=ohm_to_celsius(ohm)
print (result)

#---------------------------------------------------------------------------
#---------------------------------------------------------------------------

# VERSION 2 using RPi plus AB Electronics ADC v1.0 Board with RS components Stock#647-9991 Thermistor
# jojopi volt_to_ohm() with my Steinhart equation

def volt_to_ohm(V):
  Rd = 10000
  Rd_effective = (Rd * 16800.0) / (Rd + 16800.0)
  Rth = (5.0 - V) / V * Rd_effective
  return Rth

# read CHANNEL 1 on the ADC board
ADC1=getadcreading(adc_address1, adc_channel1)
ohm=volt_to_ohm(ADC1)

# ABC variables specifically for that thermistor
A=0.001125884
B=0.000235530
C=0.000000075

Temp= 1 / (A + B * math.log(ohm) + C * pow(math.log(ohm), 3))
Temp=Temp-273.15
print (Temp)

#---------------------------------------------------------------------------
#---------------------------------------------------------------------------

def volt_to_ohm(V, V_dummy = 0):
  Rd = 10000
  Rd_effective = (Rd * 16800.0) / (Rd + 16800.0)
  if V_dummy == 0:
    V5 = 5.0
  else:
    V5 = V_dummy * (Rd_effective + 10000) / Rd_effective
  Rth = (V5 - V) / V * Rd_effective
  return Rth
