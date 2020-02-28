class Led
{
private:
    byte pin;

public:
    Led(byte pin)
    {
        this->pin = pin;
        init();
    }
    void init()
    {
        pinMode(pin, OUTPUT);
        off();
    }
    void on()
    {
        digitalWrite(pin, HIGH);
    }
    void off()
    {
        digitalWrite(pin, LOW);
    }
};

int distanceThreshold = 0;

int cm = 0;

int inches = 0;

long readUltrasonicDistance(int triggerPin, int echoPin)
{
    pinMode(triggerPin, OUTPUT);
    digitalWrite(triggerPin, LOW);
    delayMicroseconds(2);
    digitalWrite(triggerPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(triggerPin, LOW);
    pinMode(echoPin, INPUT);
    return pulseIn(echoPin, HIGH);
}

Led led0 = Led(2);
Led led1 = Led(3);
Led led2 = Led(4);

void setup()
{
    Serial.begin(9600);
}

void loop()
{
    distanceThreshold = 300;
    cm = 0.01723 * readUltrasonicDistance(7, 6);
    inches = (cm / 2.54);
    Serial.print(cm);
    Serial.print("cm, ");
    Serial.print(inches);
    Serial.println("in");
    if (cm > distanceThreshold)
    {

        led0.off();
        led1.off();
        led2.off();
    }
    if (cm <= distanceThreshold && cm > distanceThreshold - 100)
    {
        led0.on();
        led1.off();
        led2.off();
    }
    if (cm <= distanceThreshold - 100 && cm > distanceThreshold - 250)
    {
        led0.on();
        led1.on();
        led2.off();
    }
    if (cm <= distanceThreshold - 250 && cm > distanceThreshold - 350)
    {
        led0.on();
        led1.on();
        led2.on();
    }
    if (cm <= distanceThreshold - 350)
    {
        led0.on();
        led1.on();
        led2.on();
    }
    delay(100);
}