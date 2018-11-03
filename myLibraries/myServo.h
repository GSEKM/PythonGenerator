#include <Servo.h>
class myServo{

bool isAllowed = false;

int delayTime = 15; 
int motorPin = 10;
Servo myServo;
// myServo.attach(motorPin)
void turnLeft(int degrees){
  for (int pos = degrees; pos >= 0; pos -= 1) { 
    myServo.write(pos);
    delay(delayTime);
  }
}
void turnRight(int degrees){
    for (int pos = (-degrees); pos >= 0; pos += 1) { 
        myServo.write(pos);
        delay(delayTime);
    }

}
void keepTurningLeft(){//time?
    isAllowed=true;
    while(isAllowed){
        pos+=1;
        delay(delayTime)
    }

}
void keepTurningRight(){
    isAllowed=true;
    while(isAllowed){
        pos-=1;
        delay(delayTime)
    }
    
    
}
void stop(){
    isAllowed=false;
}

void setMin(int degrees){
    myServo.//private...
}
void setMax(int degrees){

}

void setSpeed(int speed){
    delayTime=speed/1;
}

}

