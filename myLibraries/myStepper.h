#include <Stepper.h>

class myStepper{



bool isAllowed = false;


int steps;

int delayTime = 15; 
int motorPin = 10;//should be a list for stepper
Stepper myStepper(10,motorPin,10);//steps, pin /


// myStepper.attach(motorPin)

void turnLeft(int degrees){

  for (int pos = degrees; pos >= 0; pos -= 1) { 
    myStepper.step(steps);
    delay(delayTime);
  }

}
void turnRight(int degrees){
  
    for (int pos = (-degrees); pos >= 0; pos += 1) { 
        myStepper.step(steps);
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
    myStepper.//private...
}
void setMax(int degrees){

}

void setSpeed(int speed){
    delayTime=speed/1;

}

}

