import requests

# List of ticker symbols
tickers = ['GS', 'WFC', 'AXP', 'JPM', 'C', 'MS', 'COF', 'SCHW', 'V', 'MA']
year = 2024
quarter = 2

# Your API key
api_key = '9Lv7d69FTjknhnI81k7jaw==r3yMKviRQgYzD740'

# Dictionary to store responses
responses = {}

# Loop through each ticker
for ticker in tickers:
    api_url = f'https://api.api-ninjas.com/v1/earningstranscript?ticker={ticker}&year={year}&quarter={quarter}'
    response = requests.get(api_url, headers={'X-Api-Key': api_key})

    if response.status_code == requests.codes.ok:
        # Save response text to a .txt file
        with open(f"{ticker}_transcript.txt", "w", encoding="utf-8") as file:
            file.write(response.text)

        responses[ticker] = {
            "status": "success",
            "data": response.text
        }
        print(f"Transcript for {ticker} successfully retrieved and saved.")
    else:
        responses[ticker] = {
            "status": "error",
            "status_code": response.status_code,
            "error_message": response.text
        }
        print(f"Error for {ticker}: {response.status_code}, {response.text}")

# Print the full responses dictionary
print(responses)
