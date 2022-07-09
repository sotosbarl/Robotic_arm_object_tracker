#include <Servo.h>
Servo low_servo;  // create servo object to control a servo
Servo up_servo;  // create servo object to control a servo
Servo base_servo;  // create servo object to control a servo
Servo dredge_servo;
int pos_low = 150; 
int pos_up = 40; 
int pos_base = 120; 
int var_low;
int var_up;
int var_base;
bool flag1;
bool flag2;
bool flag3;
int count=0;
int pos_dredge=120;
int a;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);

 up_servo.attach(7);
   pos_up=up_servo.read();
   base_servo.attach(8);
   pos_base=base_servo.read();
   low_servo.attach(6);
  pos_low=low_servo.read();

while ((pos_up!=40)&&(pos_low!=170)&&(pos_base!=120)){
 if(pos_up<40) {
      pos_up+=1;
    up_servo.write(pos_up);
    delay(20);}
    if(pos_up>40 ){
    
      pos_up-=1;
    up_servo.write(pos_up);
    delay(20);}

  
 base_servo.attach(8);
   pos_base=base_servo.read();

 if(pos_base<120) {
      pos_base+=1;
    base_servo.write(pos_base);
    delay(20);}
    if(pos_base>120 ){
    
      pos_base-=1;
    base_servo.write(pos_base);
    delay(20);}
  
  low_servo.attach(6);
  pos_low=low_servo.read();
  if(pos_low<170) {
      pos_low+=1;
    low_servo.write(pos_low);
    delay(20);}
    if(pos_low>170 ){
    
      pos_low-=1;
    low_servo.write(pos_low);
    delay(20);}

}

  dredge_servo.attach(9);
  dredge_servo.write(160);

  
  flag1=0;
  flag2=0;
  flag3=0;
  }

void loop() {
  // put your main code here, to run repeatedly:
while (Serial.available()>0){
  
  a=Serial.readString().toInt();
  if (a==666) {
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);
    break;
  }
  if(a>1000 && a<10000) {
   //this is angle theta 
   var_low=a-1000;
   flag1==1;
  }
  
  if(a>10000) {
   //this is angle phi (up_servo)
   var_up=a-10000;
    flag2==1;
  }
  if(a>100000) {
   //this is angle phi (up_servo)
   var_base=a-100000;
    flag3==1;
  }
   pos_up=up_servo.read();
   pos_base=base_servo.read();
  pos_low=low_servo.read();
  

 while((pos_up!=var_up || pos_up<150 || pos_up>10)&&(pos_base!=var_base || pos_base>10 || pos_base<170)&&(pos_low!=var_low ||pos_low>50 || pos_low<170) && flag1 && flag2 && flag3){

  //UPPER SERVO
 if(pos_up<var_up && (pos_up<150) ) {
      pos_up+=1;
    up_servo.write(pos_up);
    delay(20);}
 if(pos_up>var_up && (pos_up>10)){
    
      pos_up-=1;
    up_servo.write(pos_up);
    delay(20);}
//LOW SERVO

     if(pos_low<var_low && (pos_low<170) ) {
      pos_low+=1;
    low_servo.write(pos_low);
    delay(20);}
 if(pos_low>var_low && (pos_low>50)){
    
      pos_low-=1;
    low_servo.write(pos_low);
    delay(20);}

//BASE SERVO

     if(pos_base<var_base && (pos_base<170)) {
      pos_low+=1;
    base_servo.write(pos_base);
    delay(20);}
 if(pos_base>var_base && (pos_base>50)){
    
      pos_base-=1;
    base_servo.write(pos_base);
    delay(20);}

 if(!((pos_up!=var_up || pos_up<150 || pos_up>10)&&(pos_base!=var_base || pos_base>10 || pos_base<170)&&(pos_low!=var_low ||pos_low>50 || pos_low<170) && !flag1 && !flag2 && !flag3)) {
      flag1=0;
      flag2=0;
      flag3=0;
      
    }
}
}


 } 
