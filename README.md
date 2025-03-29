# Comprehensive Guide to FIX Protocol and SoupBinTCP (OUCH)

## **Introduction**
This guide explains the **FIX (Financial Information Exchange) protocol** and **SoupBinTCP (OUCH protocol)** used in financial markets. It covers **message structures, parsing methods, real-world usage, and key differences** with examples.

---

## **1. FIX Protocol Overview**
FIX is a **text-based** protocol used for communication in financial markets. It is commonly used for **order routing, execution reports, and market data exchange** between brokers, exchanges, and traders.

### **FIX Message Structure**
FIX messages consist of **Tag=Value pairs**, separated by the **SOH (Start of Header) delimiter** (`\x01`). Example:

```
8=FIX.4.2|9=112|35=D|49=SENDER|56=TARGET|34=1|52=20240329-12:34:56.789|11=123456|55=AAPL|54=1|38=100|40=2|10=128|
```
(Here, `|` represents `\x01` for readability)

#### **Key Fields in a FIX Order Message:**
| Tag | Field Name       | Example Value   | Description                        |
|-----|----------------|----------------|------------------------------------|
| 8   | BeginString    | FIX.4.2         | FIX Protocol Version              |
| 9   | BodyLength     | 112             | Message length                    |
| 35  | MsgType        | D               | New Order Single                  |
| 49  | SenderCompID   | SENDER          | Sender’s identifier               |
| 56  | TargetCompID   | TARGET          | Receiver’s identifier             |
| 34  | MsgSeqNum      | 1               | Message sequence number           |
| 52  | SendingTime    | 20240329-12:34  | Timestamp                         |
| 11  | ClOrdID        | 123456          | Client Order ID                   |
| 55  | Symbol         | AAPL            | Stock ticker                      |
| 54  | Side           | 1               | 1 = Buy, 2 = Sell                 |
| 38  | OrderQty       | 100             | Number of shares                  |
| 40  | OrdType        | 2               | 2 = Limit Order                   |
| 10  | Checksum       | 128             | Ensures message integrity         |

### **Parsing a FIX Message in Python**
```python
import re

def parse_fix_message(fix_message, delimiter='\x01'):
    """Parses a FIX message into a dictionary."""
    fields = fix_message.strip().split(delimiter)
    return {field.split('=')[0]: field.split('=')[1] for field in fields if '=' in field}

# Example FIX message
fix_msg = "8=FIX.4.2\x019=112\x0135=D\x0149=SENDER\x0156=TARGET\x0134=1\x0152=20240329-12:34\x0111=123456\x0155=AAPL\x0154=1\x0138=100\x0140=2\x0110=128\x01"

parsed_message = parse_fix_message(fix_msg)
print(parsed_message)
```

### **Why FIX is Slower?**
- **Requires parsing (splitting text)**
- **Larger message size** (ASCII format, includes tag numbers)
- **More flexible but more overhead**

---

## **2. SoupBinTCP and OUCH Protocol Overview**
SoupBinTCP is **Nasdaq’s binary protocol** for session management, while OUCH is used for **order entry and execution messages**.

### **OUCH New Order Message Structure**
Unlike FIX, **OUCH messages are binary and have a fixed size**, meaning fields are always at the same position in the message.

| Field            | Size (Bytes) | Example Value    | Description                       |
|-----------------|-------------|-----------------|-----------------------------------|
| Message Type    | 1           | ‘O’ (0x4F)      | New Order                        |
| Order Token     | 14          | ABC12345678901  | Unique Order ID                  |
| Buy/Sell        | 1           | ‘B’ (0x42)      | ‘B’ = Buy, ‘S’ = Sell            |
| Shares         | 4           | 100 (0x00000064)| Number of shares                 |
| Stock Symbol    | 8           | AAPL            | Ticker symbol (padded)           |
| Price           | 4           | 15000 (0x00003A98) | Price in 10,000ths of a dollar |

### **Binary Conversion in Python**
#### **Packing Data into Binary**
```python
import struct

message_type = b'O'
order_token = b'ABC12345678901'
buy_sell = b'B'
shares = struct.pack(">I", 100) # Big-endian format
stock_symbol = b'AAPL    '
price = struct.pack(">I", 15000)

binary_message = message_type + order_token + buy_sell + shares + stock_symbol + price
print(binary_message)
```

#### **Unpacking Binary Data**
```python
unpacked_data = struct.unpack(">c14sc4s8s4s", binary_message)

message_type = unpacked_data[0].decode()
order_token = unpacked_data[1].decode().strip()
buy_sell = unpacked_data[2].decode()
shares = int.from_bytes(unpacked_data[3], "big")
stock_symbol = unpacked_data[4].decode().strip()
price = int.from_bytes(unpacked_data[5], "big")

print(f"Type: {message_type}, Order Token: {order_token}, Side: {buy_sell}, Shares: {shares}, Symbol: {stock_symbol}, Price: {price}")
```

### **Why OUCH is Faster than FIX?**
- **No parsing needed** → Data is directly extracted at fixed byte positions.
- **Compact binary format** → Saves bandwidth.
- **No need for delimiters** → No string operations.

---

## **3. FIX vs. OUCH (Comprehensive Comparison)**
| Feature           | FIX Protocol                | OUCH via SoupBinTCP       |
|------------------|---------------------------|---------------------------|
| Format           | **Text-based (ASCII)**     | **Binary (fixed-length)** |
| Parsing          | **Splitting & mapping tags** | **Direct byte extraction** |
| Message Size     | **Larger**                 | **Smaller & compact**      |
| Speed           | **Slower**                 | **Faster**                 |
| Flexibility      | **Highly flexible**        | **Rigid, fixed structure** |
| Overhead         | **Higher due to text parsing** | **Lower, direct byte reads** |
| Use Case         | **General financial messaging** | **High-frequency trading (HFT)** |

---

## **4. Questions & Answers (Q&A)**
### **Q1: Why is FIX parsing slower than OUCH?**
✔ Because FIX messages require text parsing, splitting, and mapping tags, whereas OUCH messages use fixed binary fields that can be read directly.

### **Q2: How does SoupBinTCP improve speed?**
✔ It uses a compact binary format with fixed field positions, avoiding delimiter-based parsing.

### **Q3: Can FIX and OUCH work together?**
✔ Yes! Some firms use **FIX for client connectivity** and **convert it to OUCH** for ultra-fast order execution.

---

## **Conclusion**
- **FIX is flexible but slower** due to text-based parsing.
- **OUCH via SoupBinTCP is ultra-fast** and ideal for **high-frequency trading (HFT)**.
- Understanding both is essential for building efficient trading systems!

🚀 **Next Steps**: Implement a **FIX-to-OUCH bridge**

