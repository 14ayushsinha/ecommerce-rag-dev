from datasets import load_dataset

def load_flipkart_dataset():
    dataset = load_dataset("jason1966/PromptCloudHQ_flipkart-products")
    return dataset