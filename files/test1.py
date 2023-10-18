def process_items(items):
    processed_items = []
    for index, item in enumerate(items):
        processed_item = f"Processing item {index}: {item}"
        processed_items.append(processed_item)
    return processed_items

items = ['apple', 'banana', 'orange']
result = process_items(items)
print(result)