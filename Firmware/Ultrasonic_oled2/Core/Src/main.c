/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body (Non-Blocking Robo Guardian)
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include "hcsr04.h"       // Changed to custom library
#include "ssd1306.h"
#include "ssd1306_fonts.h"
#include "ds18b20.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */
typedef enum {
    MODE_SAFE,
    MODE_HAZARD,
    MODE_EMERGENCY
} SystemMode_t;
/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
#define GAS_SENSOR_Pin     GPIO_PIN_5
#define GAS_SENSOR_Port    GPIOA

#define LED_GREEN_Pin      GPIO_PIN_12
#define LED_YELLOW_Pin     GPIO_PIN_13
#define LED_RED_Pin        GPIO_PIN_14
#define BUZZER_Pin         GPIO_PIN_15
#define OUTPUT_PORT        GPIOB

#define TEMP_THRESHOLD     45.0f // Set your temperature threshold here
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
I2C_HandleTypeDef hi2c1;

TIM_HandleTypeDef htim2;

UART_HandleTypeDef huart1;

/* USER CODE BEGIN PV */
uint16_t SysTicks = 0;
float Distance = 0.0;
float Temperature = 0.0;
char MSG[75] = {0}; // Increased size for UART packet

SystemMode_t CurrentMode = MODE_SAFE;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_TIM2_Init(void);
static void MX_USART1_UART_Init(void);
static void MX_I2C1_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */
  // Non-blocking state machine timers
  uint32_t last_sonar_trigger = 0;
  uint32_t last_oled_time = 0;
  uint32_t ds18b20_timer = 0;
  uint8_t  ds18b20_state = 0; // 0 = request conversion, 1 = wait/read

  uint32_t buzzer_timer = 0;
  uint32_t buzzer_interval = 0;
  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/
  HAL_Init();
  SystemClock_Config();
  MX_GPIO_Init();
  MX_TIM2_Init();
  MX_USART1_UART_Init();
  MX_I2C1_Init();

  /* USER CODE BEGIN 2 */
  // Initialize the custom hardware-timer HC-SR04 library
  HCSR04_Init(&htim2);

  ssd1306_Init();
  delay_us_dwt_init(); // Initialize DWT timer for OneWire communication

  sprintf(MSG, "Your AI-Powered Robo Guardian Online\r\n");
  HAL_UART_Transmit(&huart1, (uint8_t*)MSG, strlen(MSG), 100);

  ssd1306_Fill(Black);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
      uint32_t current_time = HAL_GetTick();

      // ==========================================================
      // 1. NON-BLOCKING ULTRASONIC SENSOR (Trigger Every 100ms)
      // ==========================================================
      if (current_time - last_sonar_trigger >= 100) {
          HCSR04_Trigger();
          last_sonar_trigger = current_time;
      }

      // ==========================================================
      // 2. NON-BLOCKING DS18B20 TEMPERATURE SENSOR
      // ==========================================================
      if (ds18b20_state == 0) {
          onewire_reset();
          onewire_Write(0xCC);
          onewire_Write(0x44);
          ds18b20_timer = current_time;
          ds18b20_state = 1;
      }
      else if (ds18b20_state == 1 && (current_time - ds18b20_timer >= 750)) {
          onewire_reset();
          onewire_Write(0xCC);
          onewire_Write(0xBE);

          uint8_t temp_lsb = onewire_Read();
          uint8_t temp_msb = onewire_Read();
          int16_t raw_temp = (temp_msb << 8) | temp_lsb;
          Temperature = (float)raw_temp / 16.0;

          ds18b20_state = 0;
      }

      // ==========================================================
      // 3. SENSOR EVALUATION & MODE LOGIC
      // ==========================================================
      bool gas_alert = (HAL_GPIO_ReadPin(GAS_SENSOR_Port, GAS_SENSOR_Pin) == GPIO_PIN_RESET);
      bool temp_alert = (Temperature >= TEMP_THRESHOLD);

      if (gas_alert && temp_alert) {
          CurrentMode = MODE_EMERGENCY;
      } else if (gas_alert || temp_alert) {
          CurrentMode = MODE_HAZARD;
      } else {
          CurrentMode = MODE_SAFE;
      }

      // ==========================================================
      // 4. HARDWARE ACTUATION (LEDs & Buzzer)
      // ==========================================================
      HAL_GPIO_WritePin(OUTPUT_PORT, LED_GREEN_Pin,  (CurrentMode == MODE_SAFE)      ? GPIO_PIN_SET : GPIO_PIN_RESET);
      HAL_GPIO_WritePin(OUTPUT_PORT, LED_YELLOW_Pin, (CurrentMode == MODE_HAZARD)    ? GPIO_PIN_SET : GPIO_PIN_RESET);
      HAL_GPIO_WritePin(OUTPUT_PORT, LED_RED_Pin,    (CurrentMode == MODE_EMERGENCY) ? GPIO_PIN_SET : GPIO_PIN_RESET);

      if (CurrentMode == MODE_EMERGENCY) {
          buzzer_interval = 100;
      } else if (CurrentMode == MODE_HAZARD) {
          buzzer_interval = 500;
      } else {
          buzzer_interval = 0;
          HAL_GPIO_WritePin(OUTPUT_PORT, BUZZER_Pin, GPIO_PIN_RESET);
      }

      if (buzzer_interval > 0) {
          if (current_time - buzzer_timer >= buzzer_interval) {
              buzzer_timer = current_time;
              HAL_GPIO_TogglePin(OUTPUT_PORT, BUZZER_Pin);
          }
      }

      // ==========================================================
      // 5. OLED DISPLAY & UART PACKET UPDATE (Every 250ms)
      // ==========================================================
      if (current_time - last_oled_time >= 250) {

          Distance = HCSR04_GetDistance(); // Fetch the latest background calculation

          // --- UART TRANSMISSION ---
          const char* mode_str = (CurrentMode == MODE_SAFE) ? "SAFE" : ((CurrentMode == MODE_HAZARD) ? "HAZARD" : "EMERGENCY");
          const char* gas_str = gas_alert ? "ALERT" : "OK";

          sprintf(MSG, "[DIST:%d|TEMP:%.1f|GAS:%s|MODE:%s]\r\n", (int)Distance, Temperature, gas_str, mode_str);
          HAL_UART_Transmit(&huart1, (uint8_t*)MSG, strlen(MSG), 10);

          // --- OLED UPDATE ---
          ssd1306_Fill(Black);

          sprintf(MSG, "Dist: %d cm", (int)Distance);
          ssd1306_SetCursor(0, 0);
          ssd1306_WriteString(MSG, Font_7x10, White);

          sprintf(MSG, "Temp: %.1f C", Temperature);
          ssd1306_SetCursor(0, 12);
          ssd1306_WriteString(MSG, Font_7x10, White);

          sprintf(MSG, "Gas : %s", gas_str);
          ssd1306_SetCursor(0, 24);
          ssd1306_WriteString(MSG, Font_7x10, White);

          ssd1306_SetCursor(0, 42);
          if (CurrentMode == MODE_SAFE) {
              ssd1306_WriteString("SAFE", Font_11x18, White);
          } else if (CurrentMode == MODE_HAZARD) {
              ssd1306_WriteString("HAZARD", Font_11x18, White);
          } else {
              ssd1306_WriteString("EMERGENCY", Font_11x18, White);
          }

          ssd1306_UpdateScreen();
          last_oled_time = current_time;
      }
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 12;
  RCC_OscInitStruct.PLL.PLLN = 96;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 4;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_3) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief I2C1 Initialization Function
  */
static void MX_I2C1_Init(void)
{
  hi2c1.Instance = I2C1;
  hi2c1.Init.ClockSpeed = 400000;
  hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
  hi2c1.Init.OwnAddress1 = 0;
  hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  hi2c1.Init.OwnAddress2 = 0;
  hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hi2c1) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief TIM2 Initialization Function
  */
static void MX_TIM2_Init(void)
{
  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_IC_InitTypeDef sConfigIC = {0};

  htim2.Instance = TIM2;
  htim2.Init.Prescaler = 100-1;
  htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim2.Init.Period = 65535;
  htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim2) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim2, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_IC_Init(&htim2) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim2, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigIC.ICPolarity = TIM_INPUTCHANNELPOLARITY_RISING;
  sConfigIC.ICSelection = TIM_ICSELECTION_DIRECTTI;
  sConfigIC.ICPrescaler = TIM_ICPSC_DIV1;
  sConfigIC.ICFilter = 0;
  if (HAL_TIM_IC_ConfigChannel(&htim2, &sConfigIC, TIM_CHANNEL_1) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief USART1 Initialization Function
  */
static void MX_USART1_UART_Init(void)
{
  huart1.Instance = USART1;
  huart1.Init.BaudRate = 115200;
  huart1.Init.WordLength = UART_WORDLENGTH_8B;
  huart1.Init.StopBits = UART_STOPBITS_1;
  huart1.Init.Parity = UART_PARITY_NONE;
  huart1.Init.Mode = UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart1.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart1) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief GPIO Initialization Function
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(ONEWIRE_GPIO_Port, ONEWIRE_Pin, GPIO_PIN_SET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, LED_GREEN_Pin|LED_YELLOW_Pin|LED_RED_Pin|BUZZER_Pin
                          |TRIG_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : ONEWIRE_Pin */
  GPIO_InitStruct.Pin = ONEWIRE_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
  HAL_GPIO_Init(ONEWIRE_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : GAS_SENSOR_Pin */
  GPIO_InitStruct.Pin = GAS_SENSOR_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(GAS_SENSOR_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : LED_GREEN_Pin LED_YELLOW_Pin LED_RED_Pin BUZZER_Pin */
  GPIO_InitStruct.Pin = LED_GREEN_Pin|LED_YELLOW_Pin|LED_RED_Pin|BUZZER_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pin : TRIG_Pin */
  GPIO_InitStruct.Pin = TRIG_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
  HAL_GPIO_Init(TRIG_GPIO_Port, &GPIO_InitStruct);
}

/* USER CODE BEGIN 4 */

// Custom Input Capture Callback for the HC-SR04
void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim)
{
    HCSR04_CaptureCallback(htim);
}

// You can safely remove the SysTick and Overflow callbacks here,
// as the custom library handles it all internally now.

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  */
void Error_Handler(void)
{
  __disable_irq();
  while (1)
  {
  }
}

#ifdef  USE_FULL_ASSERT
void assert_failed(uint8_t *file, uint32_t line)
{
}
#endif /* USE_FULL_ASSERT */
