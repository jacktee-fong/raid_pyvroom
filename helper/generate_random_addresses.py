import pandas as pd
import random
from pathlib import Path
import yaml
from helper.onemap import OneMapQuery


def generate_random_addresses(num_addresses: int = 30) -> None:
    """
    Generate random addresses using postal codes from postal_dict.yaml
    and save them to an Excel file
    """
    # Initialize OneMapQuery
    om = OneMapQuery()
    om.get_onemap_token()
    
    # Load postal codes from yaml file
    store_path = Path("store")
    with open(store_path/'postal_dict.yaml', 'r') as yaml_file:
        postal_dict = yaml.load(yaml_file, Loader=yaml.Loader)
    
    # Get list of postal codes (excluding None values)
    postal_codes = [k for k in postal_dict.keys() if isinstance(k, (str, int))]
    
    # Randomly select postal codes
    selected_codes = random.sample(postal_codes, num_addresses)
    
    # Generate addresses
    addresses = []
    for i, postal in enumerate(selected_codes, 1):
        address = om.get_address_by_postal(str(postal))
        if address:
            addresses.append({
                'job_id': i,
                'address': address
            })
    
    # Create DataFrame
    df = pd.DataFrame(addresses)
    
    # Create directory if it doesn't exist
    output_dir = store_path/'data'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save to Excel
    df.to_excel(output_dir/'travelling_salesman.xlsx', index=False)


if __name__ == "__main__":
    generate_random_addresses() 