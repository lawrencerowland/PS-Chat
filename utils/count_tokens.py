

import os
import json

log_folder = "data"
log_filename = "total_token_logs.json"

def get_current_total_tokens(log_filepath, model_name, token_type='total_tokens'):
    """Fetch the current total tokens for a model and token type."""
    if not os.path.exists(log_filepath):
        return 0

    with open(log_filepath, 'r') as f:
        data = json.load(f)
        return data.get(model_name, {}).get(token_type, 0)

def log_token_details_to_file(input_tokens, output_tokens, model_name):
    """Log token details to a file."""
    log_filepath = os.path.join(log_folder, log_filename)

    current_input_tokens = get_current_total_tokens(log_filepath, model_name, 'input_tokens')
    current_output_tokens = get_current_total_tokens(log_filepath, model_name, 'output_tokens')

    updated_input_tokens = current_input_tokens + input_tokens
    updated_output_tokens = current_output_tokens + output_tokens

    # Read the existing data
    if os.path.exists(log_filepath):
        with open(log_filepath, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    # Update the token count for the given model
    if model_name not in data:
        data[model_name] = {}
    data[model_name]['input_tokens'] = updated_input_tokens
    data[model_name]['output_tokens'] = updated_output_tokens

    # Ensure the directory exists
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Write the updated data back to the file
    with open(log_filepath, 'w') as f:
        json.dump(data, f, indent=4)


    
