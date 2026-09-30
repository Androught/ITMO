#include "main.h"
#include "tm1637.h"

volatile uint32_t tickCount;
char lastKey;
uint32_t lastScanTime;
int firstNumber = 0;
int secondNumber = 0;
int result = 0;

char operation = '\0';

int inputState = 0;

void osSystickHandler(void) {
  tickCount++;
}


void initGPIO() {
  // Включаем тактирование GPIOA и GPIOB
  RCC->AHBENR |= RCC_AHBENR_GPIOAEN | RCC_AHBENR_GPIOBEN;

  // Настраиваем PA5 как выход
  GPIOA->MODER = (GPIOA->MODER & ~(3 << 10)) | (1 << 10);
  GPIOA->OTYPER &= ~(1 << 5);
  GPIOA->OSPEEDR |= (1 << 10);
}

void initUSART2() {
  // Включаем тактирование USART2
  RCC->APB1ENR |= RCC_APB1ENR_USART2EN;

  // Настраиваем PA2 и PA3 в альтернативный режим
  GPIOA->MODER = (GPIOA->MODER & ~(0xF << 4)) | (0xA << 4);
  GPIOA->AFR[0] = (GPIOA->AFR[0] & ~(0xFF << 8)) | (1 << 8) | (1 << 12);

  // Настраиваем USART2
  USART2->BRR = 417; // 48MHz/115200
  USART2->CR1 = USART_CR1_TE | USART_CR1_UE;
}

void initSysTick() {
  SysTick->LOAD = 47999; // 1ms при 48MHz
  SysTick->VAL = 0;
  SysTick->CTRL = (1 << 2) | (1 << 1) | (1 << 0);
}

int _write(int file, uint8_t *ptr, int len) {
  for (int i = 0; i < len; i++) {
    while (!(USART2->ISR & USART_ISR_TXE));
    USART2->TDR = ptr[i];
  }
  return len;
}

void processKey(char key) {

  // Ввод первого числа
  if (inputState == 0) {
    if (key >= '0' && key <= '9') {
      firstNumber = key - '0';
        tm1637_display_number(firstNumber);
        inputState = 1;
        printf("First number: %d\n", firstNumber);
    }
  }
  // Выбор операции
  else if (inputState == 1) {
    if (key == '+' || key == '-' ||
      key == '*' || key == '/') {
      operation = key;
      printf("Operation: %c\n", operation);
      inputState = 2;
    }
  }
  // Ввод второго числа
  else if (inputState == 2) {
    if (key >= '0' && key <= '9') {
      secondNumber = key - '0';
      tm1637_display_number(secondNumber);
      inputState = 3;
      printf("Second number: %d\n", secondNumber);
    }
  }
  // Получение результата
  else if (inputState == 3) {
    if (key == '=') {
      switch (operation) {
        case '+':
          result = firstNumber + secondNumber;
          break;

        case '-':
          result = firstNumber - secondNumber;
          break;

        case '*':
          result = firstNumber * secondNumber;
          break;

        case '/':
          if (secondNumber != 0) {
            result = firstNumber / secondNumber;
          } else {
            printf("Division by zero!\n");
            tm1637_clear();
            inputState = 0;
            return;
          }
          break;
      }
      tm1637_display_number(result);
      printf(
        "%d %c %d = %d\n",
        firstNumber,
        operation,
        secondNumber,
        result
      );
      inputState = 0;
    }
  }
}

int main(void) {
  initGPIO();
  initUSART2();
  initSysTick();

  initKeyboard();
  tm1637_init();

  printf("Calculator started.");
  tm1637_clear();

  while (1) {
    char key = scanKeyboard();
    if (key != '\0') {
      processKey(key);
    }
  }

  return 0;
}