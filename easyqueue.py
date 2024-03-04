from easycrawl import EasyQueue, md5

data = {"str": "Hello World", "int": 666}
hash = md5(data["str"])  ## we use md5 value as unique identify, you can choose any one you like

easyQueue = EasyQueue(name="anyname")

easyQueue.push(hash, data)   ## push a data into queue
print("size:", easyQueue.size())  ## size of the queue
print("has:", easyQueue.has(hash))  ## whether queue has this data, whose unique identify is "hash"
print("visited:", easyQueue.visited(hash))  ## whether queue has visited this data (no matter it is in queue for now)
print("Advantage usage# setVisitedData:", easyQueue.setVisitedData(hash, data={"status": "in queue"}))  ## we can store some additional data in the visiting tree.
print("Advantage usage# info:", easyQueue.info(hash))  ## we can store some additional data in the visiting tree.
print(easyQueue.pop())  ## pop the top value: hash, data

'''
size: 1
has: True
visited: True
Advantage usage# setVisitedData: None
Advantage usage# info: {'push': 1, 'pop': 0, 'data': {'status': 'in queue'}}
('b10a8db164e0754105b7a99be72e3fe5', {'str': 'Hello World', 'int': 666})
'''