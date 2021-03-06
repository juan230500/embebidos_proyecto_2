txt ="""/* 
 * "Small Hello World" example. 
 * 
 * This example prints 'Hello from Nios II' to the STDOUT stream. It runs on
 * the Nios II 'standard', 'full_featured', 'fast', and 'low_cost' example 
 * designs. It requires a STDOUT  device in your system's hardware. 
 *
 * The purpose of this example is to demonstrate the smallest possible Hello 
 * World application, using the Nios II HAL library.  The memory footprint
 * of this hosted application is ~332 bytes by default using the standard 
 * reference design.  For a more fully featured Hello World application
 * example, see the example titled "Hello World".
 *
 * The memory footprint of this example has been reduced by making the
 * following changes to the normal "Hello World" example.
 * Check in the Nios II Software Developers Manual for a more complete 
 * description.
 * 
 * In the SW Application project (small_hello_world):
 *
 *  - In the C/C++ Build page
 * 
 *    - Set the Optimization Level to -Os
 * 
 * In System Library project (small_hello_world_syslib):
 *  - In the C/C++ Build page
 * 
 *    - Set the Optimization Level to -Os
 * 
 *    - Define the preprocessor option ALT_NO_INSTRUCTION_EMULATION 
 *      This removes software exception handling, which means that you cannot 
 *      run code compiled for Nios II cpu with a hardware multiplier on a core 
 *      without a the multiply unit. Check the Nios II Software Developers 
 *      Manual for more details.
 *
 *  - In the System Library page:
 *    - Set Periodic system timer and Timestamp timer to none
 *      This prevents the automatic inclusion of the timer driver.
 *
 *    - Set Max file descriptors to 4
 *      This reduces the size of the file handle pool.
 *
 *    - Check Main function does not exit
 *    - Uncheck Clean exit (flush buffers)
 *      This removes the unneeded call to exit when main returns, since it
 *      won't.
 *
 *    - Check Don't use C++
 *      This builds without the C++ support code.
 *
 *    - Check Small C library
 *      This uses a reduced functionality C library, which lacks  
 *      support for buffering, file IO, floating point and getch(), etc. 
 *      Check the Nios II Software Developers Manual for a complete list.
 *
 *    - Check Reduced device drivers
 *      This uses reduced functionality drivers if they're available. For the
 *      standard design this means you get polled UART and JTAG UART drivers,
 *      no support for the LCD driver and you lose the ability to program 
 *      CFI compliant flash devices.
 *
 *    - Check Access device drivers directly
 *      This bypasses the device file system to access device drivers directly.
 *      This eliminates the space required for the device file system services.
 *      It also provides a HAL version of libc services that access the drivers
 *      directly, further reducing space. Only a limited number of libc
 *      functions are available in this configuration.
 *
 *    - Use ALT versions of stdio routines:
 *
 *           Function                  Description
 *        ===============  =====================================
 *        alt_printf       Only supports %s, %x, and %c ( < 1 Kbyte)
 *        alt_putstr       Smaller overhead than puts with direct drivers
 *                         Note this function doesn't add a newline.
 *        alt_putchar      Smaller overhead than putchar with direct drivers
 *        alt_getchar      Smaller overhead than getchar with direct drivers
 *
 */

#include "sys/alt_irq.h"
#include "altera_avalon_pio_regs.h"
#include "altera_avalon_timer_regs.h"
#include "altera_avalon_uart_regs.h"

#define ALTCPUFREQ 50000000

#define TIMERMODE 0x4000
#define TIMERIRQ 1

#define BTMODE 0x5060
#define BTMODEIRQ 2
#define BTMODEIRQID 0

#define BTINC 0x5080
#define BTINCIRQ 4
#define BTINCIRQID 0

#define BTSEL 0x5070
#define BTSELIRQ 3
#define BTSELIRQID 0

#define UARTBAUD 115200
#define UART 0x50a0
#define UARTIRQ 0
#define UARTIRQID 0

volatile int buttonModeEdgeCapturer;
volatile int buttonIncEdgeCaputer;
volatile int buttonSelEdgeCaputer;

volatile unsigned char* ramPtr = (unsigned char *) 0x0000;
volatile unsigned char* pointerSelector;
volatile unsigned char* secPointer;
volatile unsigned char* minPointer;
volatile unsigned char* hourPointer;
volatile unsigned char* configurationPointer;
volatile unsigned char* pointerAlarmForSeg;
volatile unsigned char* alarmPointerMin;
volatile unsigned char* alarmPointerHour;
volatile unsigned char* ticTicPointer;
volatile unsigned char* uartSeg0Ptr;
volatile unsigned char* uartSeg1Ptr;
volatile unsigned char* uartMin0Ptr;
volatile unsigned char* uartMin1Ptr;
volatile unsigned char* uartHour0Ptr;
volatile unsigned char* uartHour1Ptr;
volatile unsigned char* UARTCounterPointer;
volatile unsigned char* UARTActualValue;

volatile unsigned char* sec0Pointer = (unsigned char *) 0x5000;
volatile unsigned char* sec1Pointer = (unsigned char *) 0x5010;
volatile unsigned char* segM0Pointer = (unsigned char *) 0x5020;
volatile unsigned char* segM1Pointer = (unsigned char *) 0x5030;
volatile unsigned char* segH0Pointer = (unsigned char *) 0x5040;
volatile unsigned char* segH1Pointer = (unsigned char *) 0x5050;

volatile unsigned char* ledPointer = (unsigned char *) 0x5090;

void interruptorBeginner();
void timerManagerFunction();
void alarmFunction();
void UARTManagerFunction();
void changeGeneralMode();
void changeGeneralModeOfTimer();
void TimeCounterFunction();
void changeTimerFunction();

void seeTimerNumber();
void seeAlarmInt();
void int7Seg(int num,volatile  unsigned char* seg7);

int main() {

  *sec0Pointer = 0;
  *sec1Pointer = 0;
  *segM0Pointer = 0;
  *segM1Pointer = 0;
  *segH0Pointer = 0;
  *segH1Pointer = 0;

  pointerSelector = ramPtr + 1;
  secPointer = ramPtr + 2;
  minPointer = ramPtr + 3;
  hourPointer = ramPtr + 4;
  configurationPointer = ramPtr + 5;
  pointerAlarmForSeg  = ramPtr + 6;
  alarmPointerMin = ramPtr + 7;
  alarmPointerHour = ramPtr + 8;
  ticTicPointer = ramPtr + 9;
  uartSeg0Ptr = ramPtr + 10;
  uartSeg1Ptr = ramPtr + 11;
  uartMin0Ptr = ramPtr + 12;
  uartMin1Ptr = ramPtr + 13;
  uartHour0Ptr = ramPtr + 14;
  uartHour1Ptr = ramPtr + 15;
  UARTCounterPointer = ramPtr + 16;
  UARTActualValue = ramPtr + 17;

  *pointerAlarmForSeg = 0;
  *alarmPointerMin = 0;
  *alarmPointerHour = 12;

  *uartSeg0Ptr = 0;
  *uartSeg1Ptr = 0;
  *uartMin0Ptr = 0;
  *uartMin1Ptr = 0;
  *uartHour0Ptr = 0;
  *uartHour1Ptr = 0;
  *UARTCounterPointer = 0;

  *UARTActualValue = 0;

  *pointerSelector = 0;

  *secPointer = 0;
  *minPointer = 0;
  *hourPointer = 0;

  *configurationPointer = 0;

  *ticTicPointer = 0;

  *ledPointer = 0b00000001;

  interruptorBeginner();

  while (1);

  return 0;

}

void seeTimerNumber() {

  int7Seg(*secPointer % 10, sec0Pointer);
  int7Seg(*secPointer / 10, sec1Pointer);

  int7Seg(*minPointer % 10, segM0Pointer);
  int7Seg(*minPointer / 10, segM1Pointer);

  int7Seg(*hourPointer % 10, segH0Pointer);
  int7Seg(*hourPointer / 10, segH1Pointer);

  return;
}

void seeAlarmInt() {

  int7Seg(*pointerAlarmForSeg % 10, sec0Pointer);
  int7Seg(*pointerAlarmForSeg / 10, sec1Pointer);

  int7Seg(*alarmPointerMin % 10, segM0Pointer);
  int7Seg(*alarmPointerMin / 10, segM1Pointer);

  int7Seg(*alarmPointerHour % 10, segH0Pointer);
  int7Seg(*alarmPointerHour / 10, segH1Pointer);

  return;

}

void int7Seg(int trigger, volatile unsigned char* segmento) {
    if(trigger == 0){
      *segmento = 0b1000000;
    }

    if(trigger == 1){
      *segmento = 0b1111001;
    }

    if(trigger == 2){
      *segmento = 0b0100100;
    }

    if(trigger == 3){
      *segmento = 0b0110000;
    }

    if(trigger == 4){
      *segmento = 0b0011001;
    }

    if(trigger == 5){
      *segmento = 0b0010010;
    }

    if(trigger == 6){
      *segmento = 0b0000010;
    }

    if(trigger == 7){
      *segmento = 0b1111000;
    }

    if( trigger == 8){
      *segmento = 0b0000000;
    }

    if(trigger == 9){
      *segmento = 0b0011000;
    }
}


void interruptorBeginner() {

  IOWR_ALTERA_AVALON_UART_DIVISOR(UART, (ALTCPUFREQ / UARTBAUD) + 1);
	IOWR_ALTERA_AVALON_UART_CONTROL(UART, ALTERA_AVALON_UART_CONTROL_RRDY_MSK);

  alt_ic_isr_register(UARTIRQID, UARTIRQ, UARTManagerFunction, 0, 0);
	alt_ic_irq_enable(UARTIRQID, UARTIRQ);

	alt_irq_register(TIMERIRQ, 0, timerManagerFunction);

	IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMERMODE,
		  ALTERA_AVALON_TIMER_CONTROL_CONT_MSK
		| ALTERA_AVALON_TIMER_CONTROL_START_MSK
		| ALTERA_AVALON_TIMER_CONTROL_ITO_MSK);

  void* buttonModeEdgeCapturerPointer = (void *) &buttonModeEdgeCapturer;
  void* buttonIncEdgeCaputerPointer = (void *) &buttonIncEdgeCaputer;
  void* buttonSelEdgeCaputerPointer = (void *) &buttonSelEdgeCaputer;

  IOWR_ALTERA_AVALON_PIO_IRQ_MASK(BTMODE, 0xf);
  IOWR_ALTERA_AVALON_PIO_IRQ_MASK(BTINC, 0xf);
  IOWR_ALTERA_AVALON_PIO_IRQ_MASK(BTSEL, 0xf);

  IOWR_ALTERA_AVALON_PIO_EDGE_CAP(BTMODE, 0x0);
  IOWR_ALTERA_AVALON_PIO_EDGE_CAP(BTINC, 0x0);
  IOWR_ALTERA_AVALON_PIO_EDGE_CAP(BTSEL, 0x0);

  alt_ic_isr_register(BTMODEIRQID,
                      BTMODEIRQ, changeGeneralMode,
                      buttonModeEdgeCapturerPointer, 0x0);

  alt_ic_isr_register(BTINCIRQID,
                      BTINCIRQ, changeTimerFunction,
                      buttonIncEdgeCaputerPointer, 0x0);

  alt_ic_isr_register(BTSELIRQID,
                      BTSELIRQ, changeGeneralModeOfTimer,
                      buttonSelEdgeCaputerPointer, 0x0);

  return;

}

void timerManagerFunction() {

  IOWR_ALTERA_AVALON_TIMER_STATUS(TIMERMODE, 0);

  if (*pointerSelector == 0) {
    TimeCounterFunction();
    seeTimerNumber();
    alarmFunction();
  }

  if (*pointerSelector == 2) {
    TimeCounterFunction();
  }

  return;

}

void alarmFunction() {

  if (*secPointer == *pointerAlarmForSeg && *minPointer == *alarmPointerMin && *hourPointer == *alarmPointerHour) {
    *ticTicPointer = 10;
    *ledPointer = 0b11111111;
  }
  else if (*ticTicPointer != 0) {
    *ledPointer = ~*ledPointer;
    *ticTicPointer -= 1;
  }
  else if (*ticTicPointer <= 0) {
    *ledPointer = 0b00000001;
  }

  return;

}

void UARTManagerFunction() {

  *UARTActualValue = IORD_ALTERA_AVALON_UART_RXDATA(UART);

  IOWR_ALTERA_AVALON_UART_STATUS(UART, 0);

  IOWR_ALTERA_AVALON_UART_TXDATA(UART, *UARTActualValue);

  if (*UARTCounterPointer == 0) {
    *uartHour1Ptr = *UARTActualValue;
  }
  else if(*UARTCounterPointer == 1){
    *uartHour0Ptr = *UARTActualValue;
  }
  else if(*UARTCounterPointer == 2){
    *uartMin1Ptr = *UARTActualValue;
  }
  else if(*UARTCounterPointer == 3){
    *uartMin0Ptr = *UARTActualValue;
  }
  else if(*UARTCounterPointer == 4){
    *uartSeg1Ptr = *UARTActualValue;
  }
  else if(*UARTCounterPointer == 5){
    *uartSeg0Ptr = *UARTActualValue;
  }


  *UARTCounterPointer += 1;

  if (*UARTActualValue == 'A') {

    *alarmPointerHour = ((*uartHour1Ptr - 48) * 10) + (*uartHour0Ptr - 48);
    *alarmPointerMin = ((*uartMin1Ptr - 48) * 10) + (*uartMin0Ptr - 48);
    *pointerAlarmForSeg = ((*uartSeg1Ptr - 48) * 10) + (*uartSeg0Ptr - 48);

    *UARTCounterPointer = 0;

  }

  if (*UARTActualValue == 'C') {

    *hourPointer = ((*uartHour1Ptr - 48) * 10) + (*uartHour0Ptr - 48);
    *minPointer = ((*uartMin1Ptr - 48) * 10) + (*uartMin0Ptr - 48);
    *secPointer = ((*uartSeg1Ptr - 48) * 10) + (*uartSeg0Ptr - 48);

    *UARTCounterPointer = 0;

  }
}


void changeGeneralMode() {

  IOWR_ALTERA_AVALON_PIO_EDGE_CAP(BTMODE, 0);
	IOWR_ALTERA_AVALON_PIO_IRQ_MASK(BTMODE, 0xf);

  *pointerSelector += 1;
  *configurationPointer = 0;

  if (*pointerSelector == 1) {
      *ledPointer = 0b00100010;
  }
  else if(*pointerSelector == 2){
      *ledPointer = 0b00100100;
      seeAlarmInt();
  }

  else if(*pointerSelector == 3){
      *ledPointer = 0b00000001;
      *pointerSelector = 0;
      seeTimerNumber();
  }
  }


void changeGeneralModeOfTimer() {

  IOWR_ALTERA_AVALON_PIO_EDGE_CAP(BTSEL, 0);
	IOWR_ALTERA_AVALON_PIO_IRQ_MASK(BTSEL, 0xf);

  if (*pointerSelector == 1 || *pointerSelector == 2) {
    *configurationPointer += 1;

      if(*configurationPointer == 1){
        *ledPointer = 0b00000110 & *ledPointer;
        *ledPointer = 0b01000000 | *ledPointer;
      }

      else if(*configurationPointer == 2){
        *ledPointer = 0b00000110 & *ledPointer;
        *ledPointer = 0b10000000 | *ledPointer;
      }

      else if(*configurationPointer == 3){
        *ledPointer = 0b00000110 & *ledPointer;
        *ledPointer = 0b00100000 | *ledPointer;
        *configurationPointer = 0;

    }
  }

}

void changeTimerFunction() {

  IOWR_ALTERA_AVALON_PIO_EDGE_CAP(BTINC, 0);
	IOWR_ALTERA_AVALON_PIO_IRQ_MASK(BTINC, 0xf);

  if (*pointerSelector == 1) {
    switch (*configurationPointer) {
      case 0:
        if (*secPointer == 59)
            *secPointer = 0;

        else
            *secPointer += 1;

        break;

      case 1:
        if (*minPointer == 59)
            *minPointer = 0;

        else
            *minPointer += 1;

        break;

      case 2:
        if (*hourPointer == 23)
            *hourPointer = 0;

        else
            *hourPointer += 1;

        break;
    }

    seeTimerNumber();
  }

  if (*pointerSelector == 2) {
    switch (*configurationPointer) {
      case 0:
        if (*pointerAlarmForSeg == 59)
            *pointerAlarmForSeg = 0;

        else
            *pointerAlarmForSeg += 1;

        break;

      case 1:
        if (*alarmPointerMin == 59)
            *alarmPointerMin = 0;

        else
            *alarmPointerMin += 1;

        break;

      case 2:
        if (*alarmPointerHour == 23)
            *alarmPointerHour = 0;

        else
            *alarmPointerHour += 1;

        break;
    }

    seeAlarmInt();
  }

  return;

}

void TimeCounterFunction() {

  *secPointer += 1;

  if (*secPointer == 60) {
    *minPointer += 1;
    *secPointer = 0;
  }
  if (*minPointer == 60) {
    *hourPointer += 1;
    *minPointer = 0;
  }
  if (*hourPointer == 24) {
    *hourPointer = 0;
    *minPointer = 0;
    *secPointer = 0;
  }

  return;

}

"""

txt = [x for x in txt.split("\n") if x.strip()!=""]
print(len(txt))