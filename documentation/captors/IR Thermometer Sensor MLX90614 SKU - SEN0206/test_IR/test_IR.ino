/***************************************************
* IR Thermometer Sensor-MLX90614
* ****************************************************
* This example will measure the ambient temperature and object temperature through the I2C bus

* @author jackli(Jack.li@dfrobot.com)
* @version  V1.0
* @date  2016-2-2

* GNU Lesser General Public License.
* See <http://www.gnu.org/licenses/> for details.
* All above must be included in any redistribution
* ****************************************************/


#include <Wire.h>
#include <IR_Thermometer_Sensor_MLX90614.h>

IR_Thermometer_Sensor_MLX90614 MLX90614 = IR_Thermometer_Sensor_MLX90614();

void setup() {
  Serial.begin(9600);
  MLX90614.begin();
}

void loop() {
  Serial.print("Ambient = "); Serial.print(MLX90614.GetAmbientTemp_Celsius());    Serial.print(" *C | ");
  Serial.print("Object  = "); Serial.print(MLX90614.GetObjectTemp_Celsius());     Serial.println(" *C");
  Serial.println();
  delay(500);
}
