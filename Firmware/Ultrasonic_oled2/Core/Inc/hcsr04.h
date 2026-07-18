#ifndef HCSR04_H
#define HCSR04_H

#include "main.h"

// Initialize the sensor (Starts the timer)
void HCSR04_Init(TIM_HandleTypeDef *htim);

// Send the 10 microsecond trigger pulse
void HCSR04_Trigger(void);

// Read the last calculated distance in centimeters
float HCSR04_GetDistance(void);

// This must be called inside HAL_TIM_IC_CaptureCallback in main.c
void HCSR04_CaptureCallback(TIM_HandleTypeDef *htim);

#endif /* HCSR04_H */
