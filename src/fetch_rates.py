import requests

API_KEY = "f56245b208d6cd2a3f5e8899"  
BASE_CURRENCY = "USD"

url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{BASE_CURRENCY}"

response = requests.get(url)
data = response.json()

print("Status:", data["result"])
print("Base Currency:", data["base_code"])
print("Date:", data["time_last_update_utc"])
print("\nSample rates:")

# just print a few currencies
currencies = ["PKR", "EUR", "GBP", "AED", "SAR"]
for currency in currencies:
    print(f"  1 USD = {data['conversion_rates'][currency]} {currency}")