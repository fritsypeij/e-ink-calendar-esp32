#include "wifi_pass.h"

#define ONBOARD_LED  2
#define EIDW 1304
#define EIDH 984

WiFiServer server(80);
int Version = 2; // needed for EPD

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

bool isValidPacket(unsigned char *p)
{
  return (p[0] == 'E' && p[1] == 'I' && p[2] == 'D');
}

bool isClear(unsigned char *p)
{
  return (isValidPacket(p) && p[3] == '9');
}

void clearscreen()
{
  printf("Clear \r\n");
  EPD_12in48B_Clear();
}


/*
0 - black1
1 - black2
2 - red1
3 - red2
9 - clear
 */
void paint(unsigned char *buf, int side)
{
  printf("NewImage \r\n");

  switch(side)
  {
    case 0:
      EPD_12in48B_SendBlack1(buf);
      break;
    case 1:
      EPD_12in48B_SendBlack2(buf);
      break;
    case 2:
      EPD_12in48B_SendRed1(buf);
      break;
    case 3:
      EPD_12in48B_SendRed2(buf);
      EPD_12in48B_TurnOnDisplay();
      break;
    case 9:
      clearscreen();
      break;
    default:
      printf("Unknown side \r\n");
      return;
  }

}
