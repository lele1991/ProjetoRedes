uint8_t end_com = 0;
uint32_t inputString[11];
int countInput = 0;
bool stringComplete = false;
unsigned int checksum_calc = 0;

/* Estrutura de dados para o protocolo de comunicação */
typedef struct {
  uint32_t n_req;
  byte  cmd;
  unsigned long  data;
  unsigned int checksum;
} COM;

COM frame;

void setup() {
  Serial.begin(9600);
}

///* Função que calcula o checksum */
//unsigned int check_sum(  ) {
//  unsigned int sum = 0;
//  for (int j = 0; j < 9; j++) {
//    sum += inputString[j];
//  }
//  //  Serial.println(~sum, HEX);
//  return ~sum;
//}

unsigned long temperatura () {
  unsigned long temp = 0x00003010;
  return temp;
}

unsigned long umidade () {
  unsigned long umi = 0x00003011;
  return umi;
}

void loop() {
  if (stringComplete) {
    unsigned long nreq_reciv = 0;
//    byte cdm_ = 0;
    unsigned long data_reciv = 0;
    unsigned int checksum_reciv = 0;

    unsigned long frame_1 = (unsigned long)(inputString[0] );
    unsigned long frame_2 = (unsigned long)(inputString[1] );
    unsigned long frame_3 = (unsigned long)(inputString[2] );
    unsigned long frame_4 = (unsigned long)(inputString[3] );
    nreq_reciv = (frame_1 << 24) | (frame_2 << 16) | (frame_3 << 8) | frame_4;
    
    byte frame_5 = (byte)inputString[4] ;
    
    unsigned long frame_6 = (unsigned long)(inputString[5] );
    unsigned long frame_7 = (unsigned long)(inputString[6] );
    unsigned long frame_8 = (unsigned long)(inputString[7] );
    unsigned long frame_9 = (unsigned long)(inputString[8] );
    data_reciv = (frame_6 << 24) | (frame_7 << 16) | (frame_8 << 8) | frame_9;
    
    unsigned int frame_10 = (unsigned int)(inputString[9] );
    unsigned int frame_11 = (unsigned int)(inputString[10] );

     
    checksum_reciv = (frame_10 << 8) | frame_11;
    checksum_calc = ~(nreq_reciv + frame_5 + data_reciv);
//    Serial.println(checksum_calc, HEX);
    if (checksum_calc == checksum_reciv) {

      frame.n_req = nreq_reciv;

      frame.cmd = 0xff;

      if (inputString[4] == 0x54) {
        frame.data = temperatura();
      } else if (inputString[4] == 0x48) {
        frame.data = umidade();
      } else {
        Serial.println("Este comando não existe");
      }

      unsigned int sum = 0;

      sum = frame.n_req + frame.data + frame.cmd;
      frame.checksum = ~sum;

//      Serial.write(0x4e);

      Serial.write((const uint8_t*)&frame, sizeof(COM));
//      Serial.write(frame.cmd);
//      Serial.write(frame.data);
//      Serial.write(frame.checksum);

    } else {
      Serial.println("Checksum Errado");
    }

    // clear the string:
    countInput = 0;
    stringComplete = false;
  }
}

/* Gerencia a interrupção da porta serial */
void serialEvent() {
  while (Serial.available()) {
    end_com = (uint8_t)Serial.read();
//    Serial.println(end_com, HEX);
    if (end_com == 0x04) {
      stringComplete = true;
    } else {
      inputString[countInput] = end_com;
    }
    countInput++;
  }
}
