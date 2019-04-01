void setup() {
  pinMode(10,INPUT);
  pinMode(11,INPUT);

}

void loop() {
  Serial.begin(9600);
  
  Serial.println(analogRead(A1));
  delay(10);
  Serial.end();
  delay(10);
}
