/*------------------------------------------------------------------------------
  This example illustrates how to use the LIDAR-Lite library to gain quick
  access to the basic functions of LIDAR-Lite via the Raspberry Pi interface.
  Additionally, it provides users of any platform with a template for their
  own application code.
  
  Copyright (c) 2019 Garmin Ltd. or its subsidiaries.
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
------------------------------------------------------------------------------*/

#include <linux/types.h>
#include <cstdio>
#include <csignal>
#include <iostream>

#include <../LIDARLite_RaspberryPi_Library/include/lidarlite_v3.h>

LIDARLite_v3 myLidarLite;

/*
 * ================================================================
 * The set of instructions below illustrates one method of setting
 * an alternate I2C device address in the LIDAR-Lite v3. See the
 * operator manual and C++ libraries for further details.
 * ================================================================
 */


#define i2cSecondaryAddr 0x44  // Set I2C address of LIDAR-Lite v3 to 0x44

void signalHandler(int signum)
{
   printf("Interrupt signal (\"%d\") received.\n", signum);
   exit(signum);  
}

int main()
{
    __u16 distance;
    // Initialize i2c peripheral in the cpu core
    myLidarLite.i2c_init();

    signal(SIGINT, signalHandler);

    myLidarLite.waitForBusy(i2cSecondaryAddr);
    myLidarLite.takeRange(i2cSecondaryAddr);
    distance      = myLidarLite.readDistance(i2cSecondaryAddr);

    printf("%d\n", distance);
}
