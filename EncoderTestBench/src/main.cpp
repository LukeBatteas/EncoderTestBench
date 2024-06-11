#include <SPI.h>  // include the new SPI library:
#define cmd 0x00
#define read_pos 0x00
#define set_zero 0x70
#define reset 0x60

// using two incompatible SPI devices, A and B
const int cs = 10;
// set up the speed, mode and endianness of each device
SPISettings settings(500000, MSBFIRST, SPI_MODE0); //0.5MHz,MSB,CPHA=0,CPOL=0

void setup() {
  // set the Slave Select Pins as outputs:
  pinMode (cs, OUTPUT);
  // initialize SPI:
  SPI.begin(); 
}

uint8_t data1, data2;
uint16_t pos,pos_temp;

void loop(){
  // read three bytes from device A
  SPI.beginTransaction(settings);
  digitalWrite (cs, LOW);
  // reading only, so data sent does not matter
  data1 = SPI.transfer(cmd);
  delayMicroseconds(3);
  data2 = SPI.transfer(read_pos);
  delayMicroseconds(3);
  digitalWrite (cs, HIGH);
  SPI.endTransaction();
  // Serial.print("Data1:");
  // Serial.println(data1);
  // Serial.print("Data2:");
  // Serial.println(data2);
  pos_temp = (data1<<8)|data2;
  pos = (pos_temp & 0b0011111111111100) >> 2;
  Serial.print("Encoder Reading: ");
  Serial.println(pos);
  delay(10);
}
 