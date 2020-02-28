int led0 = 7;
int led1 = 6;
int led2 = 5;
int led3 = 4;
int led4 = 3;

void setup()
{
    pinMode(led0, OUTPUT);
    pinMode(led1, OUTPUT);
    pinMode(led2, OUTPUT);
    pinMode(led3, OUTPUT);
    pinMode(led4, OUTPUT);
}

void loop()
{
    digitalWrite(led0, HIGH);
    delay(100);
    digitalWrite(led0, LOW);
    delay(100);

    digitalWrite(led1, HIGH);
    delay(100);
    digitalWrite(led1, LOW);
    delay(100);

    digitalWrite(led2, HIGH);
    delay(100);
    digitalWrite(led2, LOW);
    delay(100);

    digitalWrite(led3, HIGH);
    delay(100);
    digitalWrite(led3, LOW);
    delay(100);

    digitalWrite(led4, HIGH);
    delay(100);
    digitalWrite(led4, LOW);
    delay(100);
}
