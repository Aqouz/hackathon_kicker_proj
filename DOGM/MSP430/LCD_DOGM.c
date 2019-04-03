#include "LCD_DOGM.h"

void spi_send(char command, char daten) {

	if(daten == 0) {
		P1OUT &= ~(BIT5); // RS = LOW, es handelt sich um ein Kommando
	}
	else if(daten == 1) {
		P1OUT |= BIT5; // RS = HIGH, es handelt sich um Daten
	}

	P1OUT &= ~BIT4;        // /ChipSelect enable

	while (!(UCA0IFG&UCTXIFG));           // USCI_A0 TX buffer ready?

	UCA0TXBUF = command;                 // Send next value

	delay_us();

	while (!(UCA0IFG & UCTXIFG));
	//while (UCA0STAT & UCBBUSY);    //wait for TX to finish
	P1OUT |= BIT4;         // /CS disable


}

void dogm_init5V(void)
{
  delay_200ms();                           // 200ms delay

  spi_send(0x38,0);                // switch back to instrcution table 0
  delay_30us();                        // 30us delay

  spi_send(0x39, 0);                // 8-bit modus
  delay_30us();                        // 30us delay

  spi_send(0x1C, 0);            // 2 line LCD
  delay_30us();                        // 30us delay

  spi_send(0x74, 0);            // Contrast Set: C3=1, C2=C1=C0=0
  delay_30us();                        // 30us delay

  spi_send(0x52, 0);            // booster off
  delay_30us();                        // 30us delay

  spi_send(0x69, 0);            // voltage follower and gain
  delay_2ms();                        // 30us delay

  spi_send(0x0F, 0);            // display, cursors and blink ON
  delay_30us();                        // 30us delay

  spi_send(0x01, 0);            // delete display
  delay_50ms();                        // 50ms delay
}

void dogm_init3V(void)
{
  delay_200ms();                           // 200ms delay

  spi_send(0x39,0);                // 8-bit modus
  delay_30us();                        // 30us delay

  spi_send(0x14, 0);                // 2 line LCD
  delay_30us();                        // 30us delay

  spi_send(0x55, 0);            // booster on
  delay_30us();                        // 30us delay

  spi_send(0x6D, 0);            // voltage follower and gain
  delay_30us();                        // 30us delay

  spi_send(0x78, 0);            // Contrast Set: C3=1, C2=C1=C0=0
  delay_30us();                        // 30us delay

  spi_send(0x38, 0);            // switch back to instrcution table 0
  delay_2ms();                        // 30us delay

  spi_send(0x0F, 0);            // display, cursors and blink ON
  delay_30us();                        // 30us delay

  spi_send(0x01, 0);            // delete display, cursor @ home
  delay_50ms();                        // 50ms delay

  spi_send(0x06, 0);            // cursor auto increment
  delay_30us();                        // 30us delay
}

void delay_us(void)
{
  __delay_cycles( 1UL );
}


void delay_30us(void)
{
  __delay_cycles( 50UL );
}


void delay_2ms(void)
{
  __delay_cycles( 2000UL );
}


void delay_50ms(void)
{
  __delay_cycles( 50000UL );
}


void delay_200ms(void)
{
  __delay_cycles( 200000UL );
}

void delay_3s(void)
{
  __delay_cycles( 3000000UL );
}

void delay_100ms(void)
{
  __delay_cycles( 100000UL );
}

void dogm_gotoxy(uint8_t x, uint8_t y)
{
  uint8_t addr;

  addr = (y * 0x40) + x;
  spi_send(0x80 | addr, 0);
}

void dogm_putc(char c)
{
  spi_send(c, 1);
}


// ************************************************************
// Write string to display
// ************************************************************

void dogm_puts(char * str)
{
  while(*str != '\0')
    dogm_putc(*str++);
}

void dogm_lcd_clear(void)
{
	spi_send(0x01, 0);
}


