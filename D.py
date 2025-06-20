from machine import ADC, Pin, freq
import urandom, utime, gc
import time

gc.enable()
freq(270000000)

adc = ADC(0)
gpio0 = Pin(0, Pin.IN)
gpio1 = Pin(1, Pin.IN)
gpio2 = Pin(2, Pin.IN)
data_list = []

def convert_adc_to_voltage(adc):
    return adc.read_u16() * (3.3 / 65535)

def read_adc_based_on_gpio(gpio0, gpio1, gpio2):
    
    if gpio0.value() == 0 and gpio1.value() == 0 and gpio2.value() == 0:
        return convert_adc_to_voltage(adc) + 0
    elif gpio0.value() == 0 and gpio1.value() == 0 and gpio2.value() == 1:
        return convert_adc_to_voltage(adc) + 3.18  
    elif gpio0.value() == 0 and gpio1.value() == 1 and gpio2.value() == 0:
        return convert_adc_to_voltage(adc) + 6.4
    elif gpio0.value() == 0 and gpio1.value() == 1 and gpio2.value() == 1:
        return convert_adc_to_voltage(adc) + 9.6
    
    elif gpio0.value() == 1 and gpio1.value() == 0 and gpio2.value() == 0:
        return -convert_adc_to_voltage(adc) - 0
    elif gpio0.value() == 1 and gpio1.value() == 0 and gpio2.value() == 1:
        return -convert_adc_to_voltage(adc) - 3.18
    elif gpio0.value() == 1 and gpio1.value() == 1 and gpio2.value() == 0:
        return -convert_adc_to_voltage(adc) - 6.4
    elif gpio0.value() == 1 and gpio1.value() == 1 and gpio2.value() == 1:
        return -convert_adc_to_voltage(adc) - 9.6

for i in range(4500):
    gpio0_value = gpio0.value()
    gpio1_value = gpio1.value()
    gpio2_value = gpio2.value()    
    time.sleep_us(6)#加入延遲sleep 30 mirco sec
    time_us = time.ticks_us()
    adc_value = read_adc_based_on_gpio(gpio0, gpio1, gpio2)
    data_list.append((adc_value, time_us))
    if i % 20 == 0:  # 每 100 次觸發垃圾回收
        gc.collect()
    
    
filename = "output.csv"

with open(filename, "w") as file:
    file.write("ADC_Value,ADC_Time_us\n")

    for adc_value1, time_us in data_list:
        file.write(f"{adc_value1},{time_us}\n")

print(f"數據保存到 {filename}")
