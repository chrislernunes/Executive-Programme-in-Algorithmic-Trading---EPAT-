
# If you get nsepy module not found error. 
# Uncomment below Python code to install it

# !pip install nsepy

# import get_history function from nsepy
from nsepy import get_history


# Define a function to fecth historical data
def get_stock_data(inst_name, start_date, end_date):
    try:
        # Fetch the data
        data = get_history(symbol=inst_name,
                                   start=start_date,
                                   end=end_date)            
        # Return Open, High, Low, Close, and Volume columns
        return data[['Open','High','Low','Close','Volume']]    
                
    except Exception as e:
        # Show exception if the data retrieval fails
        print ("Failed to get stock data for " % inst_name % e)    
        
def get_option_data(inst_name, start_date, end_date, option_type, 
                     strike_price, expiry_date):
    try:
        # Fetch the data
        return get_history(symbol=inst_name,
                    start=start_date,
                    end=end_date,
                    option_type=option_type,
                    strike_price=strike_price,
                    expiry_date=expiry_date) 
                
    except Exception as e:
        # Show exception if the data retrieval fails
        print ("Failed to get options data for " % inst_name % e)       
