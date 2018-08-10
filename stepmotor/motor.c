#include <stdio.h>
#include <stdlib.h>

#include <wiringPi.h>
#include <wiringPiSPI.h>

#define L6470_SPI_CHANNEL 0

// Function protoltype
void L6470_write(unsigned char data);
void L6470_init(void);
void L6470_run(long speed);
void L6470_softstop();
void L6470_softhiz();

int main(int argc, char **argv)
{
  int i;
  long speed = 0;
  printf("***** start spi test program *****\n");
  
  // Start SPI channel 0 at 1MHz
  if (wiringPiSPISetup(L6470_SPI_CHANNEL, 1000000) < 0)
    {
      printf("SPI Setup failed: \n");
    }

  // L6470 init function
  L6470_init();
  
  while(1)
    {
      for (i = 0; i < 10; i++)
	{
	  speed += 2000; //Until 30000  
	  L6470_run(speed);
	  printf("*** Speed %d ***\n", speed);
	  delay(1000);
	}

      for (i = 0; i < 10; i++)
	{
	  speed -= 2000; 
	  L6470_run(speed);
	  printf("*** Speed %d ***\n", speed);
	  delay(1000);
	}
      
      L6470_softstop();
      L6470_softhiz();
      return 0;
    }

  return 0;
}

void L6470_write(unsigned char data)
{
  wiringPiSPIDataRW(L6470_SPI_CHANNEL, &data, 1);
}

void L6470_init()
{
  // set MAX_SPEED
  /// Register address
  L6470_write(0x07);
  // Max rotation speed (10bit) init value: 0x41
  L6470_write(0x00);
  L6470_write(0x41);
  
  // Set KVAL_HOLD
  /// Register address
  L6470_write(0x09);
  // モータ定速回転中の電圧設定(8bit)
  L6470_write(0xFF);

  // Set KVAL_RUN
  /// Register address
  L6470_write(0x0A);
  // モータ定速回転中の電圧設定(8bit)
  L6470_write(0xFF);

  // Set KVAL_ACC
  /// Register address
  L6470_write(0x0B);
  // モータ加速中の電圧設定(8bit)
  L6470_write(0xFF);
  
  // Set KVAL_DEC
  /// Register address
  L6470_write(0x0C);
  // モータ減速中の電圧設定(8bit)　初期値 0x8A
  L6470_write(0x40);

  // Set OCD_TH
  /// Register address
  L6470_write(0x13);
  // オーバーカレントスレッショルド設定(4bit)
  L6470_write(0x0F);

  // Set STALL_TH
  /// Register address
  L6470_write(0x14);
  // ストール電流スレッショルド設定(4bit)
  L6470_write(0x7F);

}

void L6470_run(long speed)
{
  unsigned short dir;
  unsigned long spd;
  unsigned char spd_h;
  unsigned char spd_m;
  unsigned char spd_l;

  // Direction searching
  if (speed < 0)
    {
      dir = 0x50;
      spd = -1 * speed;
    }
  else 
    {
      dir = 0x51;
      spd = speed;
    }

  // Create sending byte data 
  spd_h = (unsigned char)((0x0F0000 & spd) >> 16);
  spd_m = (unsigned char)((0x00FF00 & spd) >> 8);
  spd_l = (unsigned char)(0x00FF & spd);

  // Send command (register address)
  L6470_write(dir);
  // Send data;
  L6470_write(spd_h);
  L6470_write(spd_m);
  L6470_write(spd_l);
}

void L6470_softstop()
{
  unsigned short dir;
  printf("***** SoftStop. *****\n");
  dir = 0xB0;
  // Send command (address)
  L6470_write(dir);
  delay(1000);
}

void L6470_softhiz()
{
  unsigned short dir;
  printf("***** Softhiz. *****\n");
  dir = 0xA8;
  // Send command (address)
  L6470_write(dir);
  delay(1000);
}
