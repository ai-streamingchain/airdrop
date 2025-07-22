import requests
import json
from dotenv import load_dotenv
import os

def download_contract_abi(contract_address, api_key):
    """
    Download contract ABI from Etherscan
    """
    # Etherscan API endpoint
    url = f"https://api.etherscan.io/api"
    
    # Parameters for the API request
    params = {
        "module": "contract",
        "action": "getabi",
        "address": contract_address,
        "apikey": api_key
    }
    
    try:
        # Make the API request
        response = requests.get(url, params=params)
        data = response.json()
        
        if data["status"] == "1" and data["message"] == "OK":
            # Parse the ABI from the response
            abi = json.loads(data["result"])
            
            # Save ABI to file
            filename = f"abi_{contract_address}.json"
            with open(filename, "w") as f:
                json.dump(abi, f, indent=4)
            
            print(f"Successfully downloaded ABI to {filename}")
            return filename
        else:
            print(f"Error: {data['message']}")
            return None
            
    except Exception as e:
        print(f"Error downloading ABI: {str(e)}")
        return None

def main():
    # Load environment variables
    load_dotenv()
    
    # Get Etherscan API key from .env file
    api_key = os.getenv("ETHERSCAN_API_KEY")
    if not api_key:
        print("Error: ETHERSCAN_API_KEY not found in .env file")
        print("Please add ETHERSCAN_API_KEY=<your_api_key> to your .env file")
        return
    
    # Get contract address from user
    contract_address = os.getenv("FARM_CONTRACT_ADDRESS")
    
    if not contract_address:
        print("Error: Contract address is required")
        return
    
    # Download the ABI
    download_contract_abi(contract_address, api_key)

if __name__ == "__main__":
    main() 