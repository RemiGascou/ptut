/***************************************************
* Sensors read to serial JSON
* ****************************************************
* This scripts reads the value of the following sensors and sends it to serial
* in JSON format.

* - Ambient light Sensor
* - Sound Sensor
* - IR Thermometer Sensor

* @author   Remi GASCOU (remi@gascou.net)
* @version  V1.0.1
* @date     2019-11-04

* GNU Lesser General Public License.
* See <http://www.gnu.org/licenses/> for details.
* All above must be included in any redistribution
* ****************************************************/

#include <Wire.h>
#include <IR_Thermometer_Sensor_MLX90614.h>

#define ASK_COMMAND '?'

// Analog Ports (AP) used for sensors
#define LIGHT_SENSOR_AP 0
#define SOUND_SENSOR_AP 1

IR_Thermometer_Sensor_MLX90614 MLX90614 = IR_Thermometer_Sensor_MLX90614();
int sensor_light   = -1;
int sensor_sound   = -1;
float temp_ambient = -1;
float temp_object  = -1;

/**
* This functions generates the JSON string
*/
void print_sensors(int sensor_light, int sensor_sound, float temp_object, float temp_ambient){
    Serial.print("{");
    Serial.print("\"light\":"); Serial.print(sensor_light);
    Serial.print(", ");
    Serial.print("\"sound\":"); Serial.print(sensor_sound);
    Serial.print(", ");
    Serial.print("\"temp\": {\"object\":"); Serial.print(temp_object); Serial.print(", \"ambient\":"); Serial.print(temp_ambient); Serial.print("}");
    Serial.println("}");  // print JSON to serial
}


void setup() {
    // Initiate sensors :
    sensor_light = -1;    // Connect mic sensor to Analog 0
    sensor_sound = -1;    // Connect mic sensor to Analog 0
    temp_ambient = -1;    // Connect IR Thermometer sensor to I2C bus
    temp_object  = -1;
    MLX90614.begin();
    // Initiate Serial connection
    Serial.begin(9600); // open serial port, set the baud rate to 9600 bps
}


// Main loop
void loop() {
    if (Serial.available() > 0){
        if (Serial.read() == ASK_COMMAND) {
            sensor_light = analogRead(LIGHT_SENSOR_AP);
            sensor_sound = analogRead(SOUND_SENSOR_AP);
            temp_object  = MLX90614.GetObjectTemp_Celsius();
            temp_ambient = MLX90614.GetAmbientTemp_Celsius();
            // Export to JSON and send to Serial link
            print_sensors(sensor_light, sensor_sound, temp_object, temp_ambient);
        }
    }
}
