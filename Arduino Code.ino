#include <RBDdimmer.h> // Library for Light Dimmer Module
#include <LiquidCrystal_I2C.h> // Library for LCD
#include <Wire.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); // I2C address 0x27, 16 column and 2 rows
const int zeroCrossPin 	= 2;
const int acdPin 	= 3;
const int arraySize = 2;
int intData;
float floatData;
int dataArray[arraySize];
int power = 0;
dimmerLamp acd(acdPin);
void setup() {
  // put your setup code here, to run once:
  lcd.backlight();
  Serial.begin(115200);
  lcd.init();
  lcd.display();
  acd.begin(NORMAL_MODE, ON);
  acd.setPower(30);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() == 0) {
    lcd.setCursor(4, 0);
    lcd.print("Standby");
    lcd.setCursor(0, 1);
    lcd.print("Waiting for Data");
  }
  // Read the data from Python
  lcd.clear();
  lcd.setCursor(1, 0);
  lcd.print("Data Received!");
  delay(1000);
  lcd.setCursor(1, 1);
  lcd.print("Processing....");
   
  String data = Serial.readStringUntil('\r');
    
  // Parse the data and extract integer and float values
  char* ptr = strtok(const_cast<char*>(data.c_str()), ",");
    
  if (ptr != NULL) {
      intData = atoi(ptr);  // Convert the first value to integer
      ptr = strtok(NULL, ",");
  }    
  if (ptr != NULL) {
    floatData = atof(ptr);  // Convert the second value to float
  }
  // Store the values in the dataArray
  dataArray[0] = intData;
  dataArray[1] = floatData;
  int pwm = dataArray[0] * 10;
  float amount = dataArray[1];
  delay(2000);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Number of Coin/s");
  delay(500);
  lcd.setCursor(0,1);
  lcd.print("= ");
  lcd.print(dataArray[0]);
  delay(3000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Setting Power at");
  lcd.setCursor(6, 1);
  lcd.print(pwm);
  lcd.print("%");
  delay(3000);
  if (pwm > 90) {
    for (int i = 0; i <=3; i++) {
      for (int min = 30; min <= 80; min += 2) {
      acd.setPower(min);
      delay(30);
  }
      for (int max = 80; max >= 30; max -= 2) {
      acd.setPower(max);
      delay(30);
  }
    }
  } else {
    while (pwm != power) {
    int parse = map(power, 0, 90, 30, 90);
    if (pwm > power) {
      acd.setPower(parse);
      power += 1;
    } else if (pwm < power) {
      acd.setPower(parse);
      power -= 1;
    }
    delay(20);
  }
  }
  lcd.clear();
  lcd.setCursor(6,0);
  lcd.print("Done!");
  delay(3000);
  lcd.clear();
  power = pwm;
}
