class Queue:
    def __init__(self, capacity, items):
        if len(items) > capacity:
            raise IndexError('entered items are more than the capacity')

        self.capacity = capacity
        self.items = items

    def enqueue(self, item):
        if self.is_full():
            print('The queue is full!')
            return False

        self.items.append(item)
        return True

    def dequeue(self):
        if self.is_empty():
            return False

        return self.items.pop(0)

    def is_full(self):
        if len(self) == self.capacity:
            return True

        return False

    def is_empty(self):
        if len(self):
            return False

        return True

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return f"Queue(capacity={self.capacity}, items={len(self)})"



if __name__ == "__main__":
    queue = Queue(5, [1, 7, 8])
    print(queue, queue.items)

    print('enqueue <2>')
    queue.enqueue(2)

    print('enqueue <20>')
    queue.enqueue(20)

    print('enqueue <200>')
    queue.enqueue(200)
    print(queue, queue.items)
