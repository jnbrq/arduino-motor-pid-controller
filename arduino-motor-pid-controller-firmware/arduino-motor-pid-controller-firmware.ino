#define MEASUREMENT_PIN     2
#define MOTOR_PIN           9
#define BAUD_RATE           115200

class PID {
public:
    
    
    float ki, kp, kd;
    
    
    PID() {
        first_ = true;
        
        
        ki = 0.1f;
        kp = 0;
        kd = 0;
    }
    
    
    float Set(float kp_, float ki_, float kd_) {
        ki = ki_;
        kp = kp_;
        kd = kd_;
    }
    
    void Zero() {
        first_ = true;
    }
    
    
    float Calc(float e )
    {
        if (first_)
        {
            i_ = 0;             
            old_ = e;           
            first_ = false;     
            return kp * e;     
        }
        else 
        {
            float d = (e-old_); 
            i_ += e;            
            i_ = constrain(i_, -40000, 40000);
                
            old_ = e;   
            return ki * i_ + kd * d + kp * e;
                
        }
    }
private:
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
    attachInterrupt(
        digitalPinToInterrupt(MEASUREMENT_PIN),
        freq_interrupt,
        RISING);
    
    analogWrite(MOTOR_PIN, PWM);    
    delay(3000);                    
}

void loop() 
{
    /* the protocol for working with serial port
     *
     * this sketch has the ability to update PID coefficients from serial port
     * this protocol defines how to do it.
     *
     * if the first character on serial buffer is:
     *  1- X
     *      the computer wants to update PID coefficients and setpoint,
     *      coefficients are sent immediately after X, as comma separated 
     *      values, in Kp,Ki,Kd,setpoint order. The command should terminate
     *      with new-line character.
     *  2- R
     *      the computer wants to reset PID object, and put the motor to
     *      a fixed value. Doesn't need to end with new-line character.
     *  3- other
     *      ignored.
     *
     */
    
    if (Serial.available() > 0)
    {
        c = Serial.read();          
        if (c == 'X')               
        {
            s1 = Serial.readStringUntil(',');   
            s2 = Serial.readStringUntil(',');   
            s3 = Serial.readStringUntil(',');
            s4 = Serial.readStringUntil('\n');
            pid.Set(s1.toFloat(), s2.toFloat(), s3.toFloat());
                
            desiredFreq = s4.toFloat();
                
        }
        else if (c == 'R')          
        {
            pid.Zero();                     
            PWM = 127.0f;                   
            analogWrite(MOTOR_PIN, PWM);    
            delay(3000);                    
        }
    }

    error =    desiredFreq - freq;  
    PWM = pid.Calc(error);          
    PWM = constrain(PWM, 0, 255);   
    
    
    Serial.print(micros()); Serial.print(",");  
    Serial.print(error); Serial.print(",");     
    Serial.print(freq); Serial.print(",");      
    Serial.print(PWM); Serial.println();        
    
    analogWrite(MOTOR_PIN, PWM);    
    
    delay(25);  
}


void freq_interrupt() {
    if (t == 0) {
        t = micros();
    }
    else {
        long t2 = micros();
        freq = 1.0E6/(t2-t);
        t = t2;
    }
}
