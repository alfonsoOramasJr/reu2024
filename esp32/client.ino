#include <WiFi.h>
#include <WiFiMulti.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <semphr.h>

// Constants
const int ADC_PIN0 = 1; // GPIO 1
const int ADC_PIN1 = 2; // GPIO 2
const int ARRAY_SIZE = 1000;
const int COLLECTION_DELAY = 0; // In milliseconds
const int SEND_DELAY = 0; // In milliseconds

// Buffers
int bufferA[ARRAY_SIZE];
int bufferB[ARRAY_SIZE];
int bufferIndexA = 0;
int bufferIndexB = 0;

// Index variable
char indexVar = 'A';

// Semaphores
SemaphoreHandle_t indexMutex;
SemaphoreHandle_t bufferMutexA;
SemaphoreHandle_t bufferMutexB;

// WiFi and server information
WiFiMulti wifiMulti;
WiFiClient client;

const char* ssid = "computer";
const char* password = "Lightknot9";
const char* server = "192.168.8.129";
const int port = 5000;

void setup() {
  Serial.begin(115200);
  indexMutex = xSemaphoreCreateMutex();
  bufferMutexA = xSemaphoreCreateMutex();
  bufferMutexB = xSemaphoreCreateMutex();

  // Connecting to WiFi
  Serial.println("Connecting to WiFi.");
  wifiMulti.addAP(ssid, password);

  while (wifiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("\nConnected to WiFi!");

  // Connecting to server
  connectToServer();

  xTaskCreatePinnedToCore(
    dataCollectionTask,
    "DataCollection",
    10000,
    NULL,
    1, // Higher priority.
    NULL,
    1 // Core.
  );

  xTaskCreatePinnedToCore(
    sendDataTask,
    "SendData",
    10000,
    NULL,
    10, // Lower priority.
    NULL,
    0 // Core.
  );
}

void loop() {
  // Empty loop, everything is done in tasks
}

void connectToServer() {
  Serial.println("Connecting to server...");
  while (!client.connect(server, port)) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("\nConnected to server!");
}

void dataCollectionTask(void* parameter) {
  const bool DEBUG = false;

  while (true) {
    if (xSemaphoreTake(indexMutex, portMAX_DELAY) == pdTRUE) {
      char currentIndex = indexVar;
      xSemaphoreGive(indexMutex);

      SemaphoreHandle_t currentBufferMutex = (currentIndex == 'A') ? bufferMutexA : bufferMutexB;
      int* currentBuffer = (currentIndex == 'A') ? bufferA : bufferB;
      int& currentBufferIndex = (currentIndex == 'A') ? bufferIndexA : bufferIndexB;

      if (xSemaphoreTake(currentBufferMutex, portMAX_DELAY) == pdTRUE) {
        for (int i = 0; i < ARRAY_SIZE; i++) {
          int analogValue = (i % 2 == 0) ? analogRead(ADC_PIN0) : analogRead(ADC_PIN1);
          currentBuffer[currentBufferIndex++] = analogValue;
          vTaskDelay(COLLECTION_DELAY / portTICK_PERIOD_MS);
        }
        xSemaphoreGive(currentBufferMutex);

        if (xSemaphoreTake(indexMutex, portMAX_DELAY) == pdTRUE) {
          indexVar = (currentIndex == 'A') ? 'B' : 'A';
          xSemaphoreGive(indexMutex);
        }
      }
    }
    //vTaskDelay(10 / portTICK_PERIOD_MS);
  }
}

void sendDataTask(void* parameter) {
  const bool DEBUG = false;

  while (true) {
    if (!client.connected()) {
      connectToServer();
    }

    if (xSemaphoreTake(bufferMutexA, portMAX_DELAY) == pdTRUE) {
      if (bufferIndexA > 0) {
        client.write((uint8_t*)bufferA, bufferIndexA * sizeof(int));
        bufferIndexA = 0;
      }
      xSemaphoreGive(bufferMutexA);
    }

    if (xSemaphoreTake(bufferMutexB, portMAX_DELAY) == pdTRUE) {
      if (bufferIndexB > 0) {
        client.write((uint8_t*)bufferB, bufferIndexB * sizeof(int));
        bufferIndexB = 0;
      }
      xSemaphoreGive(bufferMutexB);
    }

    vTaskDelay(SEND_DELAY / portTICK_PERIOD_MS);
  }
}
