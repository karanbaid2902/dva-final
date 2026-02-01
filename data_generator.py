import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
np.random.seed(42)

def generate_data(n_rows=10000):
    categories = ['Electronics', 'Home & Kitchen', 'Fashion', 'Beauty', 'Sports']
    channels = ['Direct', 'Social Media', 'Email', 'Affiliate']
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    data = []
    start_date = datetime(2023, 1, 1)

    for i in range(n_rows):
        # Create seasonal trends (higher sales in Q4)
        days_offset = np.random.randint(0, 365)
        order_date = start_date + timedelta(days=days_offset)
        month = order_date.month
        
        # Weighted probability for Nov/Dec
        if month in [11, 12]:
            if random.random() > 0.3: continue # Add more density here by skipping less
        
        cat = random.choice(categories)
        price = np.random.uniform(10, 500) if cat != 'Electronics' else np.random.uniform(100, 1500)
        qty = np.random.randint(1, 5)
        
        data.append({
            'Order_ID': f"ORD-{1000+i}",
            'Customer_ID': f"CUST-{np.random.randint(1, 1500)}",
            'Date': order_date,
            'Category': cat,
            'Product': f"{cat} Item {np.random.randint(1, 50)}",
            'Price': price,
            'Quantity': qty,
            'Revenue': price * qty,
            'Region': random.choice(regions),
            'Channel': random.choice(channels),
            'Payment': random.choice(['Credit Card', 'PayPal', 'Crypto', 'Debit Card']),
            'Customer_Age': np.random.randint(18, 75),
            'Rating': np.random.randint(1, 6),
            'Delivery_Days': np.random.randint(1, 10)
        })
    
    df = pd.DataFrame(data)
    df.to_csv('ecommerce_data.csv', index=False)
    print("Synthetic dataset 'ecommerce_data.csv' created successfully!")

if __name__ == "__main__":
    generate_data()