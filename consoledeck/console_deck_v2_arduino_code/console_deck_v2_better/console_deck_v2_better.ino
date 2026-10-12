#define CLK 5
#define DT 4
#define SW 3

const int buttonPins[] = {6, 2, A3, 9, 10, 11, 12, A0, A1, 8}; // last = MEDIA

int counter = 0;
int currentStateCLK;
int lastStateCLK;

unsigned long lastEncoderTime = 0;
const int encoderDelay = 2; // helps smooth encoder

void setup() {

  Serial.begin(9600);

  pinMode(CLK, INPUT);
  pinMode(DT, INPUT);
  pinMode(SW, INPUT_PULLUP);

  lastStateCLK = digitalRead(CLK);

  for (int i = 0; i < 10; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
  }
}

void loop() {

  // ----- ROTARY ENCODER -----
  currentStateCLK = digitalRead(CLK);

  if (currentStateCLK != lastStateCLK && millis() - lastEncoderTime > encoderDelay) {

    if (digitalRead(DT) != currentStateCLK) {
      counter++;
    } else {
      counter--;
    }

    Serial.print("VOLUME_");
    Serial.println(counter);

    lastEncoderTime = millis();
  }

  lastStateCLK = currentStateCLK;

  // ----- ENCODER PRESS = MUTE -----
  if (digitalRead(SW) == LOW) {
    Serial.println("MUTE");
    delay(200);
  }

  // ----- USER BUTTONS -----
  for (int i = 0; i < 10; i++) {

    if (digitalRead(buttonPins[i]) == LOW) {

      if (i < 9) {
        Serial.print("BUTTON_");
        Serial.println(i + 1);
      } else {
        Serial.println("MEDIA");
      }

      delay(200);
    }
  }
}