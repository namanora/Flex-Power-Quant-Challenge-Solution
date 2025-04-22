#!/usr/bin/env python
# coding: utf-8

# # FlexPower Quant Challenge - Task 1

# In[1]:


import sqlite3


# ## Task 1.1

# ### Define total volume functions

# In[ ]:


def compute_total_volume(side: str) -> float:
    """
    Compute total traded volume for a given side.

    Input:
      side: "buy" or "sell" to specify which side of the orderbook to sum.
    Algorithm:
      1) Issue a single SQL query to sum the `quantity` column for rows matching `side`.
      2) Use COALESCE to return 0 if there are no matching rows.
      3) Fetch the result and coerce it to float.
    Returns:
      Total volume (in MW) as a float.
    """
    # Define sql query with placeholder for buy/sell
    query = (
        "SELECT COALESCE(SUM(quantity), 0) AS total_quantity "
        "FROM epex_12_20_12_13 "
        "WHERE side = ?;"
    )
    
    # Connect with SQL database
    with sqlite3.connect("trades.sqlite") as con:
        
        # Create cursor
        cur = con.cursor()
        
        # Execute query with input buy or sell and collect results
        cur.execute(query, (side,))
        result = cur.fetchone()
        
    # Return results as a float or 0 if no orders for buy/sell
    return float(result[0] or 0)

# Both functions act as wrapper to compute total volume

def compute_total_buy_volume() -> float:
    """
    Shortcut for total buy volume.

    Returns:
      Total buy volume (in MW) across all buy trades.
    """
    return compute_total_volume("buy")

def compute_total_sell_volume() -> float:
    """
    Shortcut for total sell volume.

    Returns:
      Total sell volume (in MW) across all sell trades.
    """
    return compute_total_volume("sell")


# ### Test buy and sell volume

# In[4]:


print(f"Total buy volume:  {compute_total_buy_volume()}")
print(f"Total sell volume: {compute_total_sell_volume()}")


# ## Task 1.2

# ### Define PnL function 

# All computations are done in SQL directly for better performance and lower memory usage.

# In[ ]:


def compute_pnl(strategy_id: str) -> float:
    """
    Compute total Profit & Loss for a given strategy in one SQL call.

    Input:
      strategy_id: string identifier of the trading strategy to evaluate.
    Algorithm:
      1) Use a SQL CASE expression to treat sells as +quantity*price and buys as –quantity*price.
      2) SUM over all trades for that strategy and COALESCE to 0 if no trades exist.
      3) Execute the query and fetch the single PnL value.
    Returns:
      Total PnL (in euros) as a float.
    """
    # Define sql query with placeholder for strategy_id
    query = (
        "SELECT COALESCE(SUM( "
        "    CASE "
        "      WHEN side='sell' THEN quantity * price "
        "      WHEN side='buy'  THEN -quantity * price "
        "      ELSE 0 "
        "    END"
        "), 0) AS pnl "
        "FROM epex_12_20_12_13 "
        "WHERE strategy = ?;"
    )
    
    # Connect with SQL database
    with sqlite3.connect("trades.sqlite") as con:
        
        # Create cursor
        cur = con.cursor()
        
        # Execute query with input strategy_id and collect results
        cur.execute(query, (strategy_id,))
        pnl = cur.fetchone()
    
    # Return results as a float or 0 if no entries for strategy_id
    return float(pnl[0] or 0)


# ### Test PnL calculations

# In[6]:


# Calculate PnL for both strategies (and test non-existing)
for i in [1, 2, 3]:
    strategy_name = f"strategy_{i}"
    print(f"PnL {strategy_name}: {compute_pnl(strategy_name)}")


# ## Task 1.3

# Can be found in the app.py
