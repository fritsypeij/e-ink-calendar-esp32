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

#include "config.h"


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
    if (count >= expectedPacketSize && isValidPacket(header) || isClear(header))
    {
      int side = (header[3] - '0');
      Serial.println("Paint image");
      paint((unsigned char*)buf, side);
    }
    else
      Serial.println("Received junk");
    
    free(buf);
    buf = NULL;
  }
}
