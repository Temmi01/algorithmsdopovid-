class Item:
  def __init__(self, id, itemName, price):
    self.id = id
    self.itemName = itemName
    self.price = price
    self.isDeleted = 0
  
class HashTable:
  def __init__(self, size=10):
    self.size = size
    self.table = [None] * size
    self.usedSlots = 0
    self.actUsedSlots = 0
    self.resizeCount = 1

  def hash(self, key : str) -> int:
    hash = murmurOAAT(key, len(key)) % self.size

    return hash

  def secondaryHash(self, key : str, attempt : int) -> int:
    hash = (murmurOAAT(key, len(key)) + attempt * FNV(key, len(key))) % self.size 

    return hash

  def insert(self, key, item : Item) -> bool:
    self.resize()

    i = self.hash(key)
    attempt = 0

    while True:
      if self.table[i] is not None:
        if self.table[i].id == key:
          print("The element with such ID already exist.")
          return False

      if self.table[i] is None:
        self.table[i] = item
        self.usedSlots += 1
        self.actUsedSlots += 1
        
        return True
      
      attempt += 1
      if attempt >= self.size:
        print("Hash table is full. Cannot insert.")
        return False
      i = self.secondaryHash(key, attempt)

  def resize(self):
    if self.actUsedSlots >= (0.5 * self.size):
      self.resizeCount *= 2
      self.size = self.size * self.resizeCount

      self.usedSlots = 0
      self.actUsedSlots = 0

      newTable = [None] * self.size

      for i in range(int(self.size/self.resizeCount)):
        if self.table[i] is not None and self.table[i].isDeleted != 1:
          newItem = self.table[i]
          index = self.hash(newItem.itemName)
          attempt = 0

          while True:
            if newTable[index] is None:
              newTable[index] = newItem
              self.actUsedSlots += 1
              self.usedSlots += 1
              break
            attempt += 1
            index = self.secondaryHash(newItem.itemName, attempt)
      
      self.table = newTable

  def get(self, key) -> Item:
    index = self.hash(key)
    attempt = 0

    for _ in range(self.size):
      if self.table[index] is None:
        return None
      
      if self.table[index].isDeleted == 1:
        attempt += 1
        index = self.secondaryHash(key, attempt)
        continue

      if self.table[index].id == key:
        return self.table[index]
      
    return None

  def delete(self, key):
    index = self.hash(key)
    attempt = 0

    for _ in range(self.size):
      if self.table[index] is None:
        return None
      
      if self.table[index].isDeleted == 1:
        attempt += 1
        index = self.secondaryHash(key, attempt)
        continue

      if self.table[index].id == key:
        self.table[index].isDeleted = 1
        self.table[index].itemName = "deleted"
        self.table[index].id = "deleted"

        self.usedSlots -= 1

        return self.table[index]
      
    return None
  
def murmurOAAT(key : str, h : int) -> int:
  for c in key:
    h ^= ord(c)
    h = (h * 0x5bd1e995) & 0xFFFFFFFF  
    h ^= h >> 15
  return h

def FNV(key : str, h : int) -> int:
  h ^= 2166136261

  for byte in key.encode('utf-8'): 
    h ^= byte
    h = (h * 16777619) & 0xFFFFFFFF 

  return h

def insertFromInput():
  try:
    id = str(input("Type in ID of new item: "))
    itemName = str(input("Type in the name of new item: "))
    price = float(input("Type in the price of new item: "))
    if price <= 0:
      print("Price should be greater than 0.")
      return
  except ValueError:
    print("Invalid input.")
    return
  
  newItem = Item(id, itemName, price)
  hashTable.insert(id, newItem)

def printTable():
  print("Index\t\tID\t\tName\t\tPrice")
  for i, item in enumerate(hashTable.table, 1):
    if item is None:
      print(f"{i}\t\t---\t\t---\t\t---")
    elif item.isDeleted:
      print(f"{i}\t<deleted>")
    else:
      print(f"{i}\t\t{item.id}\t\t{item.itemName}\t\t{item.price}")

def findId():
  try:
    id = str(input("Type in ID of item you want to find: "))
  except ValueError:
    print("Invalid input. ")
    return
  
  foundItem = hashTable.get(id)
  if foundItem is not None:
    print(f"Item found!\n Name: {foundItem.itemName}, price: {foundItem.price}")
  else:
    print("Item not found.\n")

def deleteId():
  try:
    id = str(input("Type in ID of item you want to find: "))
  except ValueError:
    print("Invalid input. ")
    return
  
  foundItem = hashTable.delete(id)
  if foundItem is not None:
    print(f"Item deleted.\n")
  else:
    print("There is no item with such ID. Maybe you made a typo?\n")

if __name__ == "__main__":
  hashTable = HashTable()
  print(hashTable.secondaryHash("1", 1))

  while True:
    print("""
1. Insert new item.
2. Print the table.
3. Find item by ID.
4. Delete item by ID.
0. Exit
""")

    try:
      choice = int(input("Enter your choice: "))
    except ValueError:
      print("Invalid input.\n")

    if choice == 1:
      insertFromInput()
    
    elif choice == 2:
      printTable()

    elif choice == 3:
      findId()

    elif choice == 4:
      deleteId()

    elif choice == 0:
      print("Program is stopped.")
      exit()

    else:
      print("Invalid input.\n")