#include <Servo.h>

class ServoControl
{
private:
    Servo servo;
    byte pin;
    byte pot;

public:
    ServoControl(byte pin, byte pot)
    {
        this->pin = pin;
        this->pot = pot;
        servo.attach(pin);
    }
    void follow()
    {
        servo.write(map(analogRead(pot), 0, 1023, 0, 180));
    }
};
ServoControl servos[3] = {ServoControl(2, 0), ServoControl(3, 1), ServoControl(4, 1)};
void setup() {}
void loop()
{
    for (int i = 0; i <= 2; i++)
    {
        servos[i].follow();
    }
}
