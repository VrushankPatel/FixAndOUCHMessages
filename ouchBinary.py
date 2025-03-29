import struct

# Define values
message_type = b'O'  # 1 byte
order_token = b'ABC12345678901'  # 14 bytes
buy_sell = b'B'  # 1 byte
shares = struct.pack(">I", 100)  # 4 bytes, Big-endian
stock_symbol = b'AAPL    '  # 8 bytes (padded)
price = struct.pack(">I", 15000)  # 4 bytes, Big-endian ($150.00)

# Create binary message
binary_message = message_type + order_token + buy_sell + shares + stock_symbol + price
print(binary_message)


# Unpacking message
unpacked_data = struct.unpack(">c14sc4s8s4s", binary_message)

# Convert fields to readable format
message_type = unpacked_data[0].decode()
print(f"Message Type: {message_type}")

order_token = unpacked_data[1].decode().strip()
print(f"Order Token: {order_token}")

buy_sell = unpacked_data[2].decode()
print(f"Buy/Sell: {buy_sell}")

shares = int.from_bytes(unpacked_data[3], "big")
print(f"Shares: {shares}")

stock_symbol = unpacked_data[4].decode().strip()
print(f"Stock Symbol: {stock_symbol}")

price = int.from_bytes(unpacked_data[5], "big")
print(f"Price: {price / 100:.2f}")

print(f"Type: {message_type}, Order Token: {order_token}, Side: {buy_sell}, Shares: {shares}, Symbol: {stock_symbol}, Price: {price}")
