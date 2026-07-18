#include "hcsr04.h"

static TIM_HandleTypeDef *hcsr04_htim;
static uint32_t val1 = 0;
static uint32_t val2 = 0;
static uint8_t is_first_captured = 0;
static float final_distance = 0.0f;

void HCSR04_Init(TIM_HandleTypeDef *htim) {
    hcsr04_htim = htim;
    // Start the Input Capture in interrupt mode
    HAL_TIM_IC_Start_IT(hcsr04_htim, TIM_CHANNEL_1);
}

// Simple loop delay for the 10us trigger pulse
static void delay_10us(void) {
    // Approx 10us delay at 100MHz
    for (volatile int i = 0; i < 200; i++) {}
}

void HCSR04_Trigger(void) {
    HAL_GPIO_WritePin(TRIG_GPIO_Port, TRIG_Pin, GPIO_PIN_SET);
    delay_10us();
    HAL_GPIO_WritePin(TRIG_GPIO_Port, TRIG_Pin, GPIO_PIN_RESET);
}

float HCSR04_GetDistance(void) {
    return final_distance;
}

// The core logic: measures the time between the echo's rising and falling edges
void HCSR04_CaptureCallback(TIM_HandleTypeDef *htim) {
    if (htim->Channel == HAL_TIM_ACTIVE_CHANNEL_1) {

        if (is_first_captured == 0) { // Rising edge detected
            val1 = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_1);
            is_first_captured = 1;

            // Change polarity to look for falling edge
            __HAL_TIM_SET_CAPTUREPOLARITY(htim, TIM_CHANNEL_1, TIM_INPUTCHANNELPOLARITY_FALLING);
        }
        else if (is_first_captured == 1) { // Falling edge detected
            val2 = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_1);

            // Calculate pulse width (handling timer overflow)
            uint32_t difference = 0;
            if (val2 >= val1) {
                difference = val2 - val1;
            } else {
                difference = (65535 - val1) + val2;
            }

            // Formula: Distance = (Time * Speed of Sound) / 2
            // Speed of sound = 0.0343 cm/us
            final_distance = difference * 0.01715f;

            is_first_captured = 0;

            // Change polarity back to look for next rising edge
            __HAL_TIM_SET_CAPTUREPOLARITY(htim, TIM_CHANNEL_1, TIM_INPUTCHANNELPOLARITY_RISING);

            // Disable and re-enable interrupt to prep for next trigger
            __HAL_TIM_DISABLE_IT(htim, TIM_IT_CC1);
            __HAL_TIM_ENABLE_IT(htim, TIM_IT_CC1);
        }
    }
}
