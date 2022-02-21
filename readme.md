# Simulate Pub/Sub pattern by TCP Socket with Python

### Run Server
`python server.py`

### Run Client
`python client.py [CLIENT-NAME] [DATA]`

### Data Structure
> command,receiver-name,data

**Example:**

send hello from hossain to amir :)

```python
python server.py
python client.py amir
python client.py hossain "send,amir,hello amir from hossain"
```

