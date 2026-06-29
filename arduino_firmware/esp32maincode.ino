// --- LEFT SIDE DRIVER PINS ---
#define LEFT_EN  5  
#define LEFT_IN1 4  
#define LEFT_IN2 7  

// --- RIGHT SIDE DRIVER PINS ---
#define RIGHT_EN  6 
#define RIGHT_IN1 8 
#define RIGHT_IN2 9 

// --- SPEED SETTINGS ---
int driveSpeed = 255; // Speed for moving forward/backward
int turnSpeed = 180;  // CRANKED TO MAX (255) to stop motor whine and force the spin!

void setup() {
  Serial.begin(115200);

  // Set all motor pins as outputs
  pinMode(LEFT_IN1, OUTPUT);
  pinMode(LEFT_IN2, OUTPUT);
  pinMode(LEFT_EN, OUTPUT);
  
  pinMode(RIGHT_IN1, OUTPUT);
  pinMode(RIGHT_IN2, OUTPUT);
  pinMode(RIGHT_EN, OUTPUT);

  // Ensure motors are stopped at boot
  stopMotors();
}

void loop() {
  // Listen for commands from the Raspberry Pi
  if (Serial.available() > 0) {
    char command = Serial.read(); 
    
    if (command == 'F') {
      moveForward();
    } 
    else if (command == 'B') {
      moveBackward();
    }
    else if (command == 'L') {
      turnLeft();
    }
    else if (command == 'R') {
      turnRight();
    }
    else if (command == 'S') {
      stopMotors();
    }
  }
}

// --- MOVEMENT FUNCTIONS ---
void moveForward() {
  digitalWrite(LEFT_IN1, HIGH); digitalWrite(LEFT_IN2, LOW);
  analogWrite(LEFT_EN, driveSpeed);
  
  digitalWrite(RIGHT_IN1, HIGH); digitalWrite(RIGHT_IN2, LOW);
  analogWrite(RIGHT_EN, driveSpeed);
}

void moveBackward() {
  digitalWrite(LEFT_IN1, LOW); digitalWrite(LEFT_IN2, HIGH);
  analogWrite(LEFT_EN, driveSpeed);
  
  digitalWrite(RIGHT_IN1, LOW); digitalWrite(RIGHT_IN2, HIGH);
  analogWrite(RIGHT_EN, driveSpeed);
}

void turnLeft() {
  // Left wheels backward, Right wheels forward
  digitalWrite(LEFT_IN1, LOW); digitalWrite(LEFT_IN2, HIGH);
  analogWrite(LEFT_EN, turnSpeed);
  
  digitalWrite(RIGHT_IN1, HIGH); digitalWrite(RIGHT_IN2, LOW);
  analogWrite(RIGHT_EN, turnSpeed);
}

void turnRight() {
  // Left wheels forward, Right wheels backward
  digitalWrite(LEFT_IN1, HIGH); digitalWrite(LEFT_IN2, LOW);
  analogWrite(LEFT_EN, turnSpeed);
  
  digitalWrite(RIGHT_IN1, LOW); digitalWrite(RIGHT_IN2, HIGH);
  analogWrite(RIGHT_EN, turnSpeed);
}

void stopMotors() {
  digitalWrite(LEFT_IN1, LOW); digitalWrite(LEFT_IN2, LOW);
  analogWrite(LEFT_EN, 0);
  
  digitalWrite(RIGHT_IN1, LOW); digitalWrite(RIGHT_IN2, LOW);
  analogWrite(RIGHT_EN, 0);
}