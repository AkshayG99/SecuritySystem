#define echoPin 7
#define trigPin 8
#define ledDistancePin 2
#define speakerPin 3

long duration;
long distance;

void setup() {
  Serial.begin(9600);
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(ledDistancePin, OUTPUT);
  pinMode(speakerPin, OUTPUT);
  pinMode(6, OUTPUT);
  digitalWrite(6, HIGH);
}

void loop() {
  // Trigger the ultrasonic sensor
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the duration of the echo
  duration = pulseIn(echoPin, HIGH);
  
  // Convert the duration to distance in cm
  distance = duration / 58.2;

  // Control LED and speaker based on distance
  if (distance < 10) {
    digitalWrite(ledDistancePin, HIGH); // Turn LED on
    digitalWrite(speakerPin, HIGH);    // Turn speaker on
    Serial.println("1"); // print binary signal
  } else {
    digitalWrite(ledDistancePin, LOW); // Turn LED off
    digitalWrite(speakerPin, LOW);    // Turn speaker off
    Serial.println("0"); // print binary signal
  }

  delay(1000); // Wait for 1 second
}