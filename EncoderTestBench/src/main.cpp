#include <SPI.h>  // include the new SPI library:
//command frame 1par+1R/W+14register
//registers
#define NOP 0x0000
#define ERRFL 0x0001
#define PROG 0x0003
#define DIAAGC 0x3FFC
#define MAG 0X3FFD
#define ANGLEUNC 0x3FFE
#define ANGLECOM 0x3FFF


// using two incompatible SPI devices, A and B
const int cs = 10;
// set up the speed, mode and endianness of each device
SPISettings settings(500000, MSBFIRST, SPI_MODE1); //0.5MHz,MSB,CPHA=0,CPOL=0

void setup() {
  // set the Slave Select Pins as outputs:
  pinMode (cs, OUTPUT);
  // initialize SPI:
  SPI.begin(); 
}

uint16_t nop, pos_temp, error, cmd, pos, diag;

void loop(){
  SPI.beginTransaction(settings);
  //transaction 1 read position
  cmd = (0b11<<14) | ANGLECOM;
  digitalWrite (cs, LOW);
  nop = SPI.transfer16(cmd);
  digitalWrite(cs, HIGH);
  delayNanoseconds(400);
  //transaction 2 read error register
  cmd = (0b01<<14) | ERRFL;
  digitalWrite(cs, LOW);
  pos_temp = SPI.transfer16(cmd);
  digitalWrite(cs, HIGH);
  delayNanoseconds(400);
  //transaction 3, read NOP
  cmd = (0b11<<14) | DIAAGC;
  digitalWrite(cs, LOW);
  error = SPI.transfer16(cmd);
  digitalWrite(cs, HIGH);
  delayNanoseconds(400);
  //transaction 3, read NOP
  cmd = (0b11<<14) | NOP;
  digitalWrite(cs, LOW);
  diag = SPI.transfer16(cmd);
  digitalWrite(cs, HIGH);
  SPI.endTransaction();
  //pos = (pos_temp<<2)>>2;
  Serial.print("Position:");
  Serial.println(pos_temp&0b11111111111111);
  Serial.print("Error:");
  Serial.println(error);
  //Serial.print("Diagnostic:");
  //Serial.println(diag&0b11111111);
  delay(1000);
}