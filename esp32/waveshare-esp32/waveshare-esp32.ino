/* 
 *  Based on epd12in48B-demo example by Waveshare
 *  
 */
 
#include "DEV_Config.h"
#include "utility/EPD_12in48b.h"
#include "GUI_Paint.h"
#include <WiFi.h>

// hack for "Brownout detector was triggered"
// uncomment if you are using unstable esp32
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

#define ONBOARD_LED  2

#define EIDW 1304
#define EIDH 984
#define WIFISSID "mynetwork"
#define WIFIPSK  "12345678"

WiFiServer server(80);
int Version = 1; // needed for EPD

void blink_led()
{
    delay(1000);
    digitalWrite(ONBOARD_LED,HIGH);
    delay(100);
    digitalWrite(ONBOARD_LED,LOW);
}

void show_ip(char *ip)
{
    unsigned char *buf;
    int expectedImageSize = EIDW * (EIDH / 2) / 8;
    buf = (unsigned char *)malloc(expectedImageSize);

    Paint_NewImage(buf, EIDW, (EIDH / 2), 0, WHITE);
    Paint_Clear(WHITE);
    Paint_DrawString_EN(350, 70, ip, &Font24, WHITE, BLACK);
    EPD_12in48B_SendBlack1(buf);
    EPD_12in48B_TurnOnDisplay();
    free(buf);
}

void paint(unsigned char *buf, int side)
{
  printf("NewImage \r\n");
  
  if(side)
    EPD_12in48B_SendBlack2(buf);
  else
    EPD_12in48B_SendBlack1(buf);
  
  EPD_12in48B_TurnOnDisplay();
}

bool isValidPacket(unsigned char *p)
{
  if (p[0] == 'E' && p[1] == 'I' && p[2] == 'D')
    return true;
  return false;
}

void clearscreen()
{
  printf("Clear \r\n");
  EPD_12in48B_Clear();
}

void setup()
{
  for(int i=0;i<3;i++)
    blink_led();
  
  printf("Init \r\n");
  DEV_Delay_ms(500);
  DEV_ModuleInit();
  DEV_TestLED();
  EPD_12in48B_Init();

  // hack for "Brownout detector was triggered"
  // uncomment if you are using unstable esp32
  printf("Disable brownout detector \r\n");
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
  
  printf("Connect wifi \r\n");
  WiFi.begin(WIFISSID, WIFIPSK);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
    blink_led();
  }

  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();

  printf("Clear \r\n");
  EPD_12in48B_Clear();

  show_ip((char*)WiFi.localIP().toString().c_str());
  Serial.println("Setup done");
}


void loop()
{
  unsigned char *buf;
  unsigned char header[4];
  int expectedImageSize = EIDW * (EIDH / 2) / 8;
  int expectedPacketSize = sizeof(header) + expectedImageSize;
    
  WiFiClient client = server.available();
  if (client)
  {                            
    Serial.println("New Client");
    int count = 0;

    buf = (unsigned char *)malloc(expectedImageSize);
    if (buf == NULL)
    {
      Serial.println("Cannot allocate memory for receive buffer");
      return;
    }
    
    while (client.connected())
    {
      if (client.available())
      {
        while(true)
        {
          int c = client.read();
          if (c == -1)
            break;
          if (count < sizeof(header))
            header[count] = c;
          else
            buf[count - sizeof(header)] = c;
          count++;

          if (count%1000 == 0)
             Serial.println(count);
          
          if (count >= expectedPacketSize)
            break;
          
        } // end of byte reading loop
        
        if (count >= expectedPacketSize)
        {
            Serial.println("Got max packet bytes");
            break;
        }
      }
    }
    Serial.println("Disonnected at:");
    Serial.println(count);
    if (count >= expectedPacketSize && isValidPacket(header))
    {
      int side = (header[3] - '0');
      Serial.println("Paint image");
      paint((unsigned char*)buf, side);
    }
    
    free(buf);
    buf = NULL;
  }
}
