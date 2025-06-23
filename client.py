from bot import BasicBot
import getpass

def main():
    print("=== Binance Futures Testnet Trading Bot ===")
    api_key = input("Enter API Key: ").strip()
    api_secret = getpass.getpass("Enter API Secret: ").strip()

    bot = BasicBot(api_key, api_secret)

    while True:
        print("\nOptions: [market, limit, stop-limit, exit]")
        action = input("Enter order type: ").strip().lower()
        if action == 'exit':
            break

        symbol = input("Symbol (e.g. BTCUSDT): ").upper().strip()
        side = input("Side (buy/sell): ").strip().lower()
        quantity = float(input("Quantity: ").strip())

        if action == 'market':
            order = bot.place_market_order(symbol, side, quantity)
        elif action == 'limit':
            price = input("Limit Price: ").strip()
            order = bot.place_limit_order(symbol, side, quantity, price)
        elif action == 'stop-limit':
            stop_price = input("Stop Price: ").strip()
            limit_price = input("Limit Price: ").strip()
            order = bot.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
        else:
            print("Invalid command")
            continue

        print("Order Response:", order)

if __name__ == "__main__":
    main()
