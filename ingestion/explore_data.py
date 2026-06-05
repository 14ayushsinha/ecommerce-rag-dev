from load_data import load_flipkart_dataset

dataset = load_flipkart_dataset()

df = dataset['train'].to_pandas()

print("Columns:")
print(df.columns)

print("\nShape:")
print(df.shape)

print("\nSample Records:")
print(df.head)

print(df.info())

print(df[['retail_price', 'discounted_price']])

print(df['retail_price'].isna().sum())
print(df['discounted_price'].isna().sum())

print(df.columns.tolist())

print("\nProduct Category Tree:")
print(df['product_category_tree'].iloc[0])

print("\nProduct Specs:")
print(df['product_specifications'].iloc[0])

print(df['product_rating'].value_counts().head(20))

print(df['overall_rating'].value_counts().head(20))

print(df["product_rating"] == df["overall_rating"]).all()

print(df['description'].iloc[0])

print(df['description'].iloc[100])

print(df['product_category_tree'].nunique())

print(f"\n{df['brand'].nunique()}")

print(df['product_category_tree'].head(10).tolist())

print(df.isnull().sum())

