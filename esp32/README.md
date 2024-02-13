# Set your wifi

Edit file `wifi_pass.h` with your real wifi SSID and password.

# Build

Use Arduino IDE to flash the code. Select `ESP32 dev module` as your target board.

# Protocol

The board will connect to wifi, open a tcp socket port (default 80) and read bytes from socket upon a connection.

Network paket format: HEADER (4 bytes) + PBM (80196 bytes)

HEADER is one of ansi strings: EID0 (black upper), EID1 (black bottom), EID2 (red uppper), EID3 (red bottom).

PBM bytes is half of an image you want to draw.

EID9 means clear screen.
