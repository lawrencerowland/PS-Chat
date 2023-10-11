



from utils.count_tokens import *

log_folder = "./data"
log_filename = "total_token_logs.json"

if __name__ =="__main__":
    log_file_path = os.path.join(log_folder, log_filename)

    with open(log_file_path, 'r') as file:
        token_usage = json.load(file)


    model_price = {
        "gpt-4":{
            "input_tokens":0.06,
            "output_tokens":0.12,
        },
        "gpt-3.5-turbo-16k":{
            "input_tokens":0.003,
            "output_tokens":0.004,
        }
    }
    total_cost = 0
    for model, details in token_usage.items():
        input_token_cost = details["input_tokens"] * model_price[model]["input_tokens"] /1000   
        output_token_cost = details["output_tokens"] * model_price[model]["output_tokens"] /1000
        model_total_cost = input_token_cost + output_token_cost
        
        total_cost += model_total_cost

    print(f"Total cost: ${total_cost:.2f}")

