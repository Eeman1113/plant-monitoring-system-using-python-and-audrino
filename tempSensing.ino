#include <dht.h>  


#define dht_apin A0 // Analog Pin sensor is connected to
 
dht DHT;
 
void setup(){
 
  Serial.begin(9600);
  delay(500);//Delay to let system boot
  //Serial.println("DHT11 Humidity & temperature Sensor\n\n");
  delay(1000);//Wait before accessing Sensor
 
}//end "setup()"
 
void loop(){
  //Start of Program 
 
    DHT.read11(dht_apin);
    
    //Serial.print("Current humidity = ");
    
    float humidity = analogRead(DHT.humidity);

    humidity = (humidity/4);
    
    
    float dataToSend = float(humidity);

    Serial.print(dataToSend);
    Serial.print(" , ");
    
    /*Serial.print("temperature = "); 
    Serial.println("C  ");*/

    Serial.println(DHT.temperature);
    
    delay(60000);//Wait 60 seconds before accessing sensor again.
 
  //Fastest should be once every two seconds.
 
}// end loop(
