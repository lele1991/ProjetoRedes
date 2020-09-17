#include "DHT.h"      

#define DHTPIN A1                         //DHT pino
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

uint8_t end_com = 0;
uint32_t input_data[11];
int count_input = 0;
bool data_complete = false;
unsigned int checksum_calc = 0;

// Definição dos leds de vizualização
int temperature_led = 7;    // Amarelo
int humidity_led = 6;         // Verde 

/* Estrutura de dados para o protocolo de comunicação */
typedef struct {
  uint32_t n_req;
  byte  cmd;
   uint32_t   data;
  unsigned int checksum;
} COM;


uint32_t temperatura () {
//   float temp = 28.9; 
   float temp = dht.readTemperature();
  uint32_t *temperatura = (uint32_t *) &temp; 
  digitalWrite(temperature_led, HIGH);
  digitalWrite(humidity_led, LOW);
  return  *temperatura;
  
}

uint32_t umidade () {
//  float umi = 20.5; 
   float umi = dht.readHumidity(); 
  uint32_t *umidade = (uint32_t *) &umi; 

  digitalWrite(humidity_led, HIGH);
  digitalWrite(temperature_led, LOW);
  return  *umidade;
}

void setup() {
  Serial.begin(9600);
  pinMode(temperature_led, OUTPUT);
  pinMode(humidity_led, OUTPUT);  
  dht.begin();
}


void loop() {
  
  COM frame;
  
  if (data_complete) {
    unsigned long nreq_reciv = 0;
    //    byte cdm_ = 0;
    unsigned long data_reciv = 0;
    unsigned int checksum_reciv = 0;

    unsigned long frame_1 = (unsigned long)(input_data[0] );
    unsigned long frame_2 = (unsigned long)(input_data[1] );
    unsigned long frame_3 = (unsigned long)(input_data[2] );
    unsigned long frame_4 = (unsigned long)(input_data[3] );
    nreq_reciv = (frame_1 << 24) | (frame_2 << 16) | (frame_3 << 8) | frame_4;

    byte frame_5 = (byte)input_data[4] ;

    unsigned long frame_6 = (unsigned long)(input_data[5] );
    unsigned long frame_7 = (unsigned long)(input_data[6] );
    unsigned long frame_8 = (unsigned long)(input_data[7] );
    unsigned long frame_9 = (unsigned long)(input_data[8] );
    data_reciv = (frame_6 << 24) | (frame_7 << 16) | (frame_8 << 8) | frame_9;

    unsigned int frame_10 = (unsigned int)(input_data[9] );
    unsigned int frame_11 = (unsigned int)(input_data[10] );


    checksum_reciv = (frame_10 << 8) | frame_11;
    checksum_calc = ~(nreq_reciv + frame_5 + data_reciv);
    
    //    Serial.println(checksum_calc, HEX);
    if (checksum_calc == checksum_reciv) {

      frame.n_req = nreq_reciv;

      frame.cmd = 0xff;

      if (input_data[4] == 0x54) {
        frame.data = temperatura();
      } else if (input_data[4] == 0x48) {
        frame.data = umidade();
      } else {
        Serial.println("Este comando não existe");
      }

      unsigned int sum = 0;

      sum = frame.n_req + frame.data + frame.cmd;
      frame.checksum = ~sum;
//      //
//            Serial.println(frame.n_req, HEX);
//            Serial.println(frame.cmd, HEX);
//            Serial.println(frame.data, HEX);
//            Serial.println(frame.checksum, HEX);

      //      Serial.write(0x4e);

            Serial.write((const uint8_t*)&frame, sizeof(COM));
      //      Serial.write(frame.cmd);
      //      Serial.write(frame.data);
      //      Serial.write(frame.checksum);

    } else {
      Serial.println("Checksum Errado");
    }

    // clear the string:
    count_input = 0;
    data_complete = false;
  }
}

/* Gerencia a interrupção da porta serial */
void serialEvent() {
  while (Serial.available()) {
    end_com = (uint8_t)Serial.read();
//        Serial.println(end_com, HEX);
    if (end_com == 0x04) {
      data_complete = true;
    } else {
      input_data[count_input] = end_com;
    }
    count_input++;
  }
}
