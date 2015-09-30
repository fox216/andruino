/*--------------------------------------------------------------------------------------------
Andruino - Software interface for serial control of the Arduino

Note: Updated addressing scheme to remove leading zeros





----------------------------------------------------------------------------------------------
*/

#define MAX_MESSAGE_SIZE 3
#define INIT_BLINK_DELAY 150
#define TOGGLE_BLINK 50
#define RUN_BLINK_DELAY 10
#define StatusLed 13
#define Statustw 12
#define NumOfPorts 4
#define NumOfRegisters 3
#define DDR 0
#define PORT 1
#define PIN 2
#define REG_B 1
#define REG_C 2
#define REG_D 3

int BlinkCount = 0;
int commandBuffer[2];
int *CMD;
byte regMap[NumOfPorts][NumOfRegisters]; 
volatile int led_status_state = LOW;
volatile int pintw = HIGH;


 

struct {
	unsigned int low : 4; //bits 0-3
	unsigned int high: 4; //bits 4-7 
} addr;

union xAddr {
	struct {
		unsigned int low: 4;
		unsigned int high: 4;
	} byteMap;
	xAddr(byte thisByte) {
		// addr.high = (serialByte & 0xF0) >> 4;
                //// Mas low bits and shift high position
                // addr.low = serialByte & 0x0F;
		byteMap.low = thisByte & 0x0F; 
		byteMap.high = (thisByte & 0xF0) >> 4;
	} byte getByte;

};


union regAddr {
	regAddr(byte hiNbl, byte lowNbl) {
		data = lowNbl;
		data |= hiNbl << 4;
	}	
	byte data;
};


enum {
	// Define the ascii charaters used in the program
	// 
	CMD_START = 0x23, // # - start processing
	CMD_READ = 0x72, // r - read
	CMD_WRITE = 0x77, // w - write
	CMD_SAVE = 0x73, // s -  save
	
};

void toggleLed() {
	led_status_state = !led_status_state;
	digitalWrite(StatusLed, led_status_state);
}
void toggletw() {
	pintw = !pintw;
	digitalWrite(Statustw, pintw);
}

void setIOMap() {
	/************************************
	Scan All regsters, Store result in bin map	

	*************************************/	
	// read ddr ports, add map to array
	// TODO: Change this method to memory address instead of Adruino name. 
	// 	Would setup support for multiple controller types 
	regMap[REG_B][DDR] = DDRB;
	regMap[REG_B][PORT] = PORTB;
	regMap[REG_B][PIN] = PINB;
	// Scan Output States
	regMap[REG_C][DDR] = DDRC;
	regMap[REG_C][PORT] = PORTC;
	regMap[REG_C][PIN] = PINC;
	// Scan Input states
	regMap[REG_D][DDR] = DDRD;
	regMap[REG_D][PORT] = PORTD;
	regMap[REG_D][PIN] = PIND;

}

void sendIOMap() {
	// Read Map configuration
	setIOMap();
	// send map for each port
	Serial.print("{");
	for (int port =1; port < NumOfPorts; port++ ) {
		if (port != 1) {
			Serial.print(",");
		}
		for (int reg=0; reg < NumOfRegisters; reg++ ) {
			// walk through array and return map to calling application
			regAddr convertAddr(port ,reg);
		        Serial.print(convertAddr.data, HEX);
			Serial.print(":");
			Serial.print(regMap[port][reg], HEX);
			// TODO: Update parsing to include 
			if (reg != NumOfRegisters -1 ) {
				Serial.print(",");
			}
		}
	}
	Serial.println("}");

}


int getSerialByte() {
	// Set return value to 0 this is ASCII NULL Character
	// System will not attempt to process this 
	
	int serialByte = 0;
	// Check to make certain the byte has not been 
	// removed from the queue.
	if (Serial.available() > 0 ) {
		serialByte = Serial.read();
		// Set high and low nibbles
		// Mask only high bytes then shift to lowest position
		addr.high = (serialByte & 0xF0) >> 4;
		// Mas low bits and shift high position
		addr.low = serialByte & 0x0F;
		//addr = serialByte;
		return serialByte;
	} else {
		// if the serial port is empty when requested 
		return -1; 
	}
	//	return serialByte;
}

void wait_for_host(){
	// Initial state when device is powered on. 
		// Initialize state. 
	// Wait for the controlling software to start
	pinMode(StatusLed, OUTPUT);
	int result;
	Serial.flush();
	while(1) {
		toggleLed();
		//result = 		
		if (Serial.available() > 0) {
			// Wait for web controller to initialize the system 
			// Device will exit this state once a '#' character is sent.
			if (getSerialByte() == CMD_START) {
				// Send # character to break out of loop
				digitalWrite(StatusLed, LOW);
				return;
			}
		}
		delay(INIT_BLINK_DELAY);
	}
}


int processWriteRequest(int Addr, int Data) {
	// Process the address listing and update avr
	// Define bit map for ports
	// B = 0x3F (00111111)
	// C = 0x00 (00000000)
	// D = 0xFC (11111100)
	int ioMask[NumOfPorts] = {0x00, 0x3F, 0x00, 0xFC};
	int tempMask = 0x00;
	//Get Register Address
	xAddr conv(Addr);
	// Register Addressing
	// High Nibble = Port ( 0 =B ,1 =C ,or 2 =D)
	// Low Nibble = Register Type (0=DDR, 1=PORT, 2=PIN [Can not Write TO PIN])
	if (conv.byteMap.high == 1) {
		// Process Port B
		// Apply Port B Mask
		tempMask = ioMask[conv.byteMap.high] & Data;
		if (conv.byteMap.low == 0) {
			// Configure Direction of IO Pins
			DDRB = tempMask;	
		} else if (conv.byteMap.low == 1) {
			// Set state of a pin
			PORTB = tempMask;
		} else {
			// TODO add serial error
			Serial.println("Error[21]: illegal operation");
		}
	} else if (conv.byteMap.high == 3) {
		// Process Port D
		// Apply Port D Mask
		tempMask = ioMask[conv.byteMap.high] & Data;
		if (conv.byteMap.low == 0) {
			// Configure Direction of IO Pins
			DDRD = tempMask;	
		} else if (conv.byteMap.low == 1) {
			// Set state of a pin
			PORTD = tempMask;
		} else {
			// TODO add serial error
			Serial.println("Error[21]: illegal operation");
		}

	} else {
		// Nothing Good happened return error code
		return -1;
	}		
	
	


}


void setup() {
	Serial.begin(115200);
	delay(100);
	//DDRB = 0x2d;
	wait_for_host();
	Serial.println("Starting...");
	// Clear ddr registers
	DDRB = 0x00;
}

void serialParser() {
	// parse incomming data
	//If there is data available on the serial port	
	int currentByte;
	bool expectingCommand = false;
	int returnVal;
	while (Serial.available() != 0) {
		// Read all bytes off the serial queue
		// Save the current byte
		currentByte = getSerialByte();
		/*
		// print Debug message
		Serial.print("-Got > ");
		Serial.println(currentByte, HEX);
		Serial.print("High (");
		Serial.print(addr.high, HEX);
		Serial.print(") Low (");
		Serial.print(addr.low, HEX);
		Serial.println(")");
		
		xAddr conv(currentByte);
		Serial.print("test [");
		Serial.print(conv.getByte, HEX);
		
		Serial.print("] - H: ");
		Serial.print(conv.byteMap.high, HEX);
		Serial.print(" - L: ");
		Serial.print(conv.byteMap.low, HEX);
		Serial.println(" end ");
		*/
		// Determine if the byte is a command or command sequence		
		if (currentByte == CMD_READ ) {
			// Display map 'M' key
			sendIOMap();			
		} else if (currentByte == CMD_WRITE) {
			int registerAddressByte = getSerialByte();
			int registerData = getSerialByte();		
			// if there is nothing on the serial port
			// getSerialByte  will return -1.
			// Verify valid data before continuing...
			if ((registerAddressByte != -1 ) && (registerData != -1) ) {
				// call process data funtion...
				
				// debug message
				//Serial.println("Got Valid Command");
				xAddr conv(registerAddressByte);

				//if ((conv.byteMap.high  == 0) || (conv.byteMap.high == 2)) {
				if ((conv.byteMap.high  == 1) || (conv.byteMap.high == 3)) {
					// verify requested address is within valid range
					if ( conv.byteMap.low != 2 ) { 
						returnVal = processWriteRequest(registerAddressByte, registerData);
			
					} else {
						
						Serial.println("Error[16]: Invalid request Can not write to PIN Register");
					}
				} else {
					Serial.println("Error[15]: Address Out of Range");
				}
								
				
			} else {
				// return an error to the application 
				// 
				Serial.println("{BadData}");
			}

		}  
	}
}

void loop() {
	
	// ---------------------------------------------------------
	// System should only be interrupted 
	// When a serial command is received.
	// ---------------------------------------------------------
	//Read Serial Queue Depth
	// If data is available and over depth limit
	// Read data, determine if it is a valid command to process
	// ---------------------------------------------------------
	if (Serial.available() > 0 ) {
		serialParser();
	}
	/*
	if (BlinkCount >= TOGGLE_BLINK ) {
		BlinkCount =0;
		toggleLed();
		toggletw();
	}
	BlinkCount++;
	*/
	delay(RUN_BLINK_DELAY);

}

