import requests
import configparser

# Handle config file for API key
def read_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

# Return supported currency codes
# Check if on program currency codes are the same as from api
# If not, append to on program codes then return the updated list
def supported_codes(data, updated_list):
    new_codes = []
    currency_codes = get_currency_codes(data)
    for code in currency_codes:
        if code not in updated_list:
            new_codes.append(code)
            print(f"Update : Support for {code} has been added. ")
            
    updated_list.extend(code for code in new_codes if code is not updated_list)
        
    return sorted(updated_list)
    
# Get currency data from api related to the base currency
def fetch_currency_data(api_key, base_currency):
    params = {"apikey": api_key, "base_currency": base_currency}
    
    try:
        response = requests.get("https://api.freecurrencyapi.com/v1/latest", params=params)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            print(f"Request failed with error: {response.status_code}")
            return None
    except Exception as e:
        print("Failed to connected with database. Check your internet connection!")
        return None

# Get keys (currency codes) from dictionary *To be removed
def get_currency_codes(currency_data):
    return currency_data.keys()

# Handle user responses
def user_input(message, valid_inputs):
    while True:
        user_input = input(message).upper()
        if user_input == "0":
            return None
        elif user_input in valid_inputs:
            return user_input
        else:
            print("Invalid input. Please try again.")

def main():
    currency_codes_updated = [
    'AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP',
    'HKD', 'HRK', 'HUF', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MXN',
    'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RON', 'RUB', 'SEK', 'SGD', 'THB',
    'TRY', 'USD']
    
    config = read_config()
    api_key = config['api']['key']
    
    while True:
        currency_codes_joined = " - ".join(currency_codes_updated)
        print(f"\nAvailable counter currencies:\n{currency_codes_joined} \n")
            
        base_currency = user_input("Enter base currency (0 to quit): ", currency_codes_updated)
        if base_currency is None: # Terminate loop if None, see user_input*
            break
        
        currency_data = fetch_currency_data(api_key, base_currency)
        if currency_data:
            currency_codes = supported_codes(currency_data, currency_codes_updated)
            
            while True:
                counter_currency = user_input("Enter counter currency (0 to go back): ", currency_codes)
                if counter_currency is None:
                    break
                
                try:
                    base_amount = float(input(f"Enter amount to convert ({base_currency} to {counter_currency}): "))
                    conversion_rate = currency_data[counter_currency]
                    converted_amount = base_amount * conversion_rate
                    print(f"{base_amount} {base_currency} to {counter_currency} => {round(converted_amount, 2)} {counter_currency}")
                except ValueError:
                    print("Invalid amount. Please enter a valid number.")
        else:
            break

if __name__ == "__main__":
    main()