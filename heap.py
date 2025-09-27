import heapq

class MemoryManager:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = [None] * capacity  # simulate raw memory
        self.free_list = [(0, capacity)] # (start, size)
        self.allocations = {}           # pointer -> (size, value)

    def malloc(self, size, value):
        for i, (start, free_size) in enumerate(self.free_list):
            if free_size >= size:
                # Allocate block
                ptr = start
                self.allocations[ptr] = (size, value)

                # Update free list
                if free_size == size:
                    self.free_list.pop(i)
                else:
                    self.free_list[i] = (start + size, free_size - size)

                # Store value in "memory"
                for j in range(ptr, ptr + size):
                    self.memory[j] = value

                return ptr
        raise MemoryError("Out of memory!")

    def free(self, ptr):
        if ptr not in self.allocations:
            raise ValueError("Invalid or double free detected")

        size, value = self.allocations.pop(ptr)

        # Clear memory
        for j in range(ptr, ptr + size):
            self.memory[j] = None

        # Insert block back into free list
        self.free_list.append((ptr, size))
        self.free_list = self._merge_free_blocks()

    def _merge_free_blocks(self):
        merged = []
        for start, size in sorted(self.free_list):
            if merged and merged[-1][0] + merged[-1][1] == start:
                merged[-1] = (merged[-1][0], merged[-1][1] + size)
            else:
                merged.append((start, size))
        return merged

    def __repr__(self):
        return f"Free blocks: {self.free_list}, Allocations: {self.allocations}"


class HeapWithMemory:
    def __init__(self, capacity):
        self.manager = MemoryManager(capacity)
        self.heap = []  # stores (priority, pointer)

    def push(self, priority, value, size=1):
        ptr = self.manager.malloc(size, value)
        heapq.heappush(self.heap, (priority, ptr))

    def pop(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        priority, ptr = heapq.heappop(self.heap)
        size, value = self.manager.allocations.get(ptr, (None, None))
        self.manager.free(ptr)
        return priority, value

    def peek(self):
        if not self.heap:
            return None
        priority, ptr = self.heap[0]
        size, value = self.manager.allocations.get(ptr, (None, None))
        return priority, value

    def __repr__(self):
        return f"Heap: {[(p, self.manager.allocations[i][1]) for p, i in self.heap]}"


# Example Usage

heap = HeapWithMemory(capacity=20)

# Insert tasks with memory allocation
heap.push(2, "Task A", size=5)
heap.push(1, "Task B", size=3)
heap.push(3, "Task C", size=4)

print(heap)
# Heap: [(1, 'Task B'), (2, 'Task A'), (3, 'Task C')]

print(heap.manager)
# Free blocks: [(12, 8)], Allocations: {0: (5, 'Task A'), 5: (3, 'Task B'), 8: (4, 'Task C')}

print("Peek:", heap.peek())
# Peek: (1, 'Task B')

print("Pop:", heap.pop())
# Pop: (1, 'Task B')

print(heap.manager)
# Free blocks: [(5, 3), (12, 8)], Allocations: {0: (5, 'Task A'), 8: (4, 'Task C')}
