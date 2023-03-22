//Configuration Sketch - Version 1.01 - www.cheap-thermocam.tk

#include <i2cmaster.h>

void setup()
{
Serial.begin(9600);
Serial.println("This program will change the EEPROM settings of");
Serial.println("your MLX90614-DCI sensor to work best with the");
Serial.println("Cheap-Thermocam. Please make sure you only use");
Serial.println("this with the DCI version, otherwise you will");
Serial.println("destroy your sensor ! PRESS ANY KEY TO CONTINUE");
Serial.println("");
Serial.println("Created by Max Ritter - www.cheap-thermocam.tk");
Serial.println("");
while (Serial.available() == 0) {
}
Serial.println("----------Let's begin!----------");
Serial.println("");
i2c_init();
PORTC = (1 << PORTC4) | (1 << PORTC5); 

int dev = 0x00; 
unsigned int data_l = 0;
unsigned int data_h = 0;
int pec = 0;
unsigned int data_t = 0;
boolean check = true;

//WRITE TO EEPROM, FIRST: ERASE OLD STUFF
Serial.println("*1: Erasing old EEPROM settings");
Serial.println("");
Serial.println("Erasing filter settings..");
i2c_start_wait(dev+I2C_WRITE);
i2c_write(0x25);
i2c_write(0x00); //Erase low byte (write 0)
i2c_write(0x00); //Erase high byte (write 0)
i2c_write(0x83); //Send PEC
//For PEC Calculation have a look at : http://smbus.org/faq/crc8Applet.htm
//In this case the PEC calculates from 250000 (=0x83)
i2c_stop();
delay(5000);

Serial.println("Erasing maximum temperature setting..");
i2c_start_wait(dev+I2C_WRITE);
i2c_write(0x20);
i2c_write(0x00);
i2c_write(0x00);
i2c_write(0x43);
i2c_stop();
delay(5000);

Serial.println("Erasing minimum temperature setting..");
i2c_start_wait(dev+I2C_WRITE);
i2c_write(0x21);
i2c_write(0x00);
i2c_write(0x00);
i2c_write(0x28); 
i2c_stop();
delay(5000);

//WRITE TO EEPROM, THE NEW STUFF!
Serial.println("");
Serial.println("*2: Write new settings to EEPROM");
Serial.println("");
Serial.println("Writing new filter settings..");
i2c_start_wait(dev+I2C_WRITE);
i2c_write(0x25); //Register Address to write to
i2c_write(0x74); //New filter settings (B374)
i2c_write(0xB3);
i2c_write(0x65); //Send PEC
i2c_stop();
delay(5000);

Serial.println("Writing new maximum temperature setting..");
i2c_start_wait(dev+I2C_WRITE);
i2c_write(0x20);
i2c_write(0xFF);
i2c_write(0xFF);
i2c_write(0x67);
i2c_stop();
delay(5000);

Serial.println("Writing new minimum temperature setting..");
i2c_start_wait(dev+I2C_WRITE);
i2c_write(0x21);
i2c_write(0x5B); 
i2c_write(0x4F);
i2c_write(0x59);
i2c_stop();
delay(5000);

//CHECKING IF EVERYTHING IS OK
Serial.println("");
Serial.println("*3: Validating the new settings");
Serial.println("");

Serial.println("Checking filter settings..");
i2c_start_wait(dev+I2C_WRITE);
i2c_write(0x25);
i2c_rep_start(dev+I2C_READ);
data_l = i2c_readAck();
data_h = i2c_readAck();
pec = i2c_readNak();
i2c_stop();
data_t = (((data_h) << 8) + data_l);
if(data_t != 45940){
  check = false;
}
delay(5000);

Serial.println("Checking maximum temperature setting..");
i2c_start_wait(dev+I2C_WRITE);
i2c_write(0x20);
i2c_rep_start(dev+I2C_READ);
data_l = i2c_readAck();
data_h = i2c_readAck();
pec = i2c_readNak();
i2c_stop();
data_t = (((data_h) << 8) + data_l);
if(data_t != 65535){
  check = false;
}
delay(5000);

Serial.println("Checking minimum temperature setting..");
i2c_start_wait(dev+I2C_WRITE);
i2c_write(0x21);
i2c_rep_start(dev+I2C_READ);
data_l = i2c_readAck();
data_h = i2c_readAck();
pec = i2c_readNak();
i2c_stop();
data_t = (((data_h) << 8) + data_l);
if(data_t != 20315){
  check = false;
}
delay(5000);

Serial.println("");
if(check == true){
Serial.println("----------Finish!----------");
}
else{
Serial.println("ERROR ! Not all settings could be written !");  
Serial.println("Re-run this sketch or check the connections !");  
}
}
void loop()
{
}


