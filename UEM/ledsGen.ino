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
Led leds[5] = {7, 6, 5, 4, 3};
void setup() {}
void loop()
{
    for (int i = 0; i <= 4; i++)
    {
        leds[i].on();
        delay(300);
        leds[i].off();
        delay(300);
    }
}