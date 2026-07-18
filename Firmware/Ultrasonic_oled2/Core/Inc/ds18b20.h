/* ds18b20.h */
#ifndef LIBRERIAS_DS18B20_H_
#define LIBRERIAS_DS18B20_H_
#include "main.h"
#include "stm32f4xx_hal.h" // Changed from f1xx to f4xx

// Delay functions
#define delay_us delay_us_dwt

void delay_us_dwt(uint32_t us);
void delay_us_dwt_init(void);

// DS18B20 functions
float DS18b20_temp(void);

// OneWire functions
uint8_t onewire_reset(void);
void onewire_Write(uint8_t dato);
uint8_t onewire_Read(void);

// GPIO functions
void Output_Pin(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin);
void Input_Pin(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin);

#endif /* LIBRERIAS_DS18B20_H_ */
