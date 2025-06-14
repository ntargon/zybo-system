/******************************************************************************
* Copyright (C) 2023 Advanced Micro Devices, Inc. All Rights Reserved.
* SPDX-License-Identifier: MIT
******************************************************************************/
/*
 * helloworld.c: simple test application
 *
 * This application configures UART 16550 to baud rate 9600.
 * PS7 UART (Zynq) is not initialized by this application, since
 * bootrom/bsp configures it to baud rate 115200
 *
 * ------------------------------------------------
 * | UART TYPE   BAUD RATE                        |
 * ------------------------------------------------
 *   uartns550   9600
 *   uartlite    Configurable only in HW design
 *   ps7_uart    115200 (configured by bootrom/bsp)
 */

#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "platform.h"
#include "xil_printf.h"

int main()
{
    init_platform();

    print("UART Echo Application\n\r");
    print("Type characters to see them echoed back.\n\r");
    print("Use <CR> as delimiter.\n\r");

    char buf[256] = {0}; // Buffer to hold input characters
    uint32_t index = 0;

    while (1) {
        // Read character from UART
        char c = inbyte();

        if (index > sizeof(buf) - 1) {
            // skip if buffer is full
            c = '\r'; // Use carriage return to indicate buffer overflow
        }
        buf[index++] = c;

        // If character is CR, add newline
        if (c == '\r') {
            buf[index++] = '\n';
            buf[index++] = '\0'; // Null-terminate the string
            // Echo the input back
            print(buf); // Print the buffer content

            index = 0; // Reset index for next line
            memset(buf, 0, sizeof(buf)); // Clear buffer
        }
    }

    // Note: This will never be reached due to infinite loop
    cleanup_platform();
    return 0;
}
