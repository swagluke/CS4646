"""MC2-P1: Market simulator.  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			  	 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			  	 		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
Template code for CS 4646/7646  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			  	 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			  	 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			  	 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			  	 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			  	 		  		  		    	 		 		   		 		  
or edited.  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
We do grant permission to share solutions privately with non-students such  		   	  			  	 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			  	 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			  	 		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
-----do not edit anything above this line---  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
Student Name: Kok Jian Yu (replace with your name)  		   	  			  	 		  		  		    	 		 		   		 		  
GT User ID: jkok7 (replace with your User ID)  		   	  			  	 		  		  		    	 		 		   		 		  
GT ID: 903550380 (replace with your GT ID)  		   	  			  	 		  		  		    	 		 		   		 		  
"""  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
import pandas as pd  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
import os  		   	  			  	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):  		   	  			  	 		  		  		    	 		 		   		 		  
    # this is the function the autograder will call to test your code  		   	  			  	 		  		  		    	 		 		   		 		  
    # NOTE: orders_file may be a string, or it may be a file object. Your  		   	  			  	 		  		  		    	 		 		   		 		  
    # code should work correctly with either input  		   	  			  	 		  		  		    	 		 		   		 		  
    # TODO: Your code here  

    orders = pd.read_csv(orders_file)

    # Get list of dates.
    unique_dates = orders["Date"].unique().tolist()
    unique_dates.sort()
    start_date = dt.datetime.strptime(unique_dates[0], '%Y-%m-%d')  		   	  			  	 		  		  		    	 		 		   		 		  
    end_date = dt.datetime.strptime(unique_dates[-1], '%Y-%m-%d')
    date_list = pd.date_range(start_date, end_date)

    # Get all unique symbols.
    unique_symbols = orders["Symbol"].unique().tolist()  	 		  		  		    	 		 		   		 		  

    # Initialize starting balance and stocks
    balance = start_val
    stock_shares = pd.DataFrame(np.zeros((len(unique_symbols), 1)), index = unique_symbols)
                                                                                                                  
    # Get data from start to end date.	   	  			  	 		  		  		    	 		 		   		 		  
    datas = get_data(unique_symbols, date_list)  		   	  			  	 		  		  		    	 		 		   		 		  
    datas = datas[unique_symbols]  # remove SPY 
    date_list = datas.index 		   	  			  	 		  		  		    	 		 		   		 		 
    # rv = pd.DataFrame(index=datas.index, data=datas.values) 		   	  			  	 		  		  		    	 		 		   		 		  	  	 		  		  		    	 		 		   		 		  
    # Remove unfulfilled orders, orders that are made when market is closed.
    orders = orders[orders["Date"].isin(datas.index.strftime('%Y-%m-%d'))]
    portfolio = pd.DataFrame(np.zeros((len(date_list), 1)), index = date_list)
    
    datas = datas.fillna(method="ffill")
    datas = datas.fillna(method="bfill")
    for day in date_list: 
        current_strtime = day.strftime('%Y-%m-%d') 
        orders_today = orders[orders["Date"] == current_strtime]
        # If there are orders
        if orders_today.shape[0] != 0:
            for i in range(orders_today.shape[0]):
                # get order details
                current_order = orders_today.iloc[i]
                order_type = current_order["Order"]
                order_num_of_shares = current_order["Shares"]
                order_symbol = current_order["Symbol"]
                current_symbol_price = datas.loc[current_strtime, order_symbol]
                order_type_multiplier = 0
                # if sell, add to balance. if buy, reduce from balance
                if order_type == "BUY":
                    order_type_multiplier = -1
                else: 
                    order_type_multiplier = 1
                # execute order 66
                balance += order_type_multiplier * order_num_of_shares * current_symbol_price
                stock_shares.loc[order_symbol] += -1 * order_type_multiplier * order_num_of_shares

                # Minus commission
                balance -= commission

                # Minus impact
                balance -= order_num_of_shares * current_symbol_price * impact



        # Update portfolio with balance and current stock worth
        stock_value = datas.loc[current_strtime, unique_symbols] * stock_shares.transpose()[unique_symbols]
        portfolio.loc[current_strtime] = balance + stock_value.sum(axis=1)
   	   	  			  	 		  		  		    	 		 		   		 		  
    return portfolio  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
def test_code():  		   	  			  	 		  		  		    	 		 		   		 		  
    # this is a helper function you can use to test your code  		   	  			  	 		  		  		    	 		 		   		 		  
    # note that during autograding his function will not be called.  		   	  			  	 		  		  		    	 		 		   		 		  
    # Define input parameters  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
    of = "./orders/orders2.csv"  		   	  			  	 		  		  		    	 		 		   		 		  
    sv = 1000000  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
    # Process orders  		   	  			  	 		  		  		    	 		 		   		 		  
    portvals = compute_portvals(orders_file = of, start_val = sv)  		   	  			  	 		  		  		    	 		 		   		 		  
    if isinstance(portvals, pd.DataFrame):  		   	  			  	 		  		  		    	 		 		   		 		  
        portvals = portvals[portvals.columns[0]] # just get the first column  		   	  			  	 		  		  		    	 		 		   		 		  
    else:  		   	  			  	 		  		  		    	 		 		   		 		  
        "warning, code did not return a DataFrame"  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
    # Get portfolio stats  		   	  			  	 		  		  		    	 		 		   		 		  
    # Here we just fake the data. you should use your code from previous assignments.  		   	  			  	 		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2008,1,1)  		   	  			  	 		  		  		    	 		 		   		 		  
    end_date = dt.datetime(2008,6,1)  		   	  			  	 		  		  		    	 		 		   		 		  
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]  		   	  			  	 		  		  		    	 		 		   		 		  
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                                  
    # Compare portfolio against $SPX  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Date Range: {start_date} to {end_date}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Cumulative Return of Fund: {cum_ret}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Cumulative Return of SPY : {cum_ret_SPY}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Final Portfolio Value: {portvals[-1]}")  		   	  			  	 		  		  		    	 		 		   		 		  


def author():
    return "jkok7"

if __name__ == "__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    test_code()  		   	  			  	 		  		  		    	 		 		   		 		  
