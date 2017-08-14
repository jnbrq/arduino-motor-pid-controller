#define MEASUREMENT_PIN   2
#define MOTOR_PIN         9
#define BAUD_RATE         9600

class PID {
public:
  PID() {
    first_ = true;
    ki_ = 0;
    kp_ = 0.1f;
    kd_ = 0;
  }

  float Set(float kp, float ki, float kd) {
    ki_ = ki;
    kp_ = kp;
    kd_ = kd;
  }

  void Reset() {
    first_ = true;
    ki_ = 0;
    kp_ = 1;
    kd_ = 0;
  }

  float Get(float &kp, float &ki, float &kd) {
    ki = ki_;
    kp = kp_;
    kd = kd_;
  }

  float Calc(float y) 
  {
    if (first_) 
    {
      i_ = 0;
      old_ = y;
      first_ = false;
      return kp_ * y;
    }
    else 
    {
      float d = (y-old_);
      i_ += y;
      old_ = y;
      return ki_ * i_ + kd_ * d + kp_ * y;
    }
  }
private:
  float ki_, kp_, kd_;
  float i_;
  float old_;
  bool first_;
};

PID pid;
float desiredFreq = 300.0f;
float freq;
float error;
float PWM = 127.0f;
long t = 0;

String s1,s2,s3,s4;
int c;
void setup() 
{
  Serial.begin(BAUD_RATE);
  pinMode(MEASUREMENT_PIN, INPUT);
  pinMode(MOTOR_PIN, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(MEASUREMENT_PIN), myInterrupt, RISING);
  analogWrite(MOTOR_PIN, PWM);  // make it around 450 Hz
  delay(3000);
}

void loop() 
{
  /* for update process */
  if (Serial.available() > 0) 
  {
    c = Serial.read();
    if (c == 'X') 
    {
      s1 = Serial.readStringUntil(',');
      s2 = Serial.readStringUntil(',');
      s3 = Serial.readStringUntil(',');
      s4 = Serial.readStringUntil('\n');
      /*Serial.println(s1.toFloat());
      Serial.println(s2.toFloat());
      Serial.println(s3.toFloat());*/
      /* kp, ki, kd */
      pid.Set(s1.toFloat(), s2.toFloat(), s3.toFloat());
      desiredFreq = s4.toFloat();
    }
    if (c == 'R') 
    {
      pid.Reset();
      PWM = 127.0f;
      analogWrite(MOTOR_PIN, PWM);  // make it around 450 Hz
      delay(3000);
    }
  }

  error =  desiredFreq - freq;
  PWM += pid.Calc(error);
  PWM = constrain(PWM, 0, 255);
  Serial.print(micros()); Serial.print(",");
  Serial.print(error); Serial.print(",");
  Serial.print(freq); Serial.print(",");
  Serial.print(PWM); Serial.println();
  analogWrite(MOTOR_PIN, PWM);
  delay(25);
}

void myInterrupt() {
  if (t == 0) {
    t = micros();
  }
  else {
    long t2 = micros();
    freq = 1.0E6/(t2-t);
    t = t2;
  }
}


