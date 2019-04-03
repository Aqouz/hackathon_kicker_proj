#ifndef LCD_DOGM_H_
#define LCD_DOGM_H_

#include <MSP430.h>
#include <stdint.h>

void spi_send(char command, char daten);
void dogm_init5V(void);
void dogm_init3V(void);
void delay_us(void);
void delay_30us(void);
void delay_50ms(void);
void delay_2ms(void);
void delay_200ms(void);
void delay_100ms(void);
void delay_3s(void);
void dogm_putc(char);                         // Write character to display
void dogm_puts(char *);                       // Write string to display
void dogm_gotoxy(uint8_t x, uint8_t y);
void dogm_lcd_clear(void);



#endif /* LCD_DOGM_H_ */
