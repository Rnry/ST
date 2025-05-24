'''Eating philosophers problem'''
import threading
import time
import random
# Task 2: number of philosophers 5->7
NUM_PHILOSOPHERS = 7
# Deadlocks do not occur either way
# (after changing the number of philosophers to 6, 7 and 10)
forks = [threading.Semaphore(1) for _ in range(NUM_PHILOSOPHERS)]

eaten_philosophers = set()

thinking_times = {i: 0 for i in range(NUM_PHILOSOPHERS)}
eating_times = {i: 0 for i in range(NUM_PHILOSOPHERS)}
thinking_counts = {i: 0 for i in range(NUM_PHILOSOPHERS)}
eating_counts = {i: 0 for i in range(NUM_PHILOSOPHERS)}


def philosopher(id):
    '''Give forks to philosophers in specific conditions'''
    global eaten_philosophers
    global thinking_times
    global eating_times
    global thinking_counts
    global eating_counts

    while True:
        # Task 4: creating a priority system.
        while id in eaten_philosophers and len(eaten_philosophers) < NUM_PHILOSOPHERS:
            time.sleep(0.1)

        think_start = time.time()
        print(f"Philosopher {id} is thinking")
        time.sleep(random.uniform(0.1, 0.5))
        think_end = time.time()

        # Task 5 :calculating thinking time
        thinking_times[id] += (think_end - think_start)
        thinking_counts[id] += 1

        first = id
        second = (id + 1) % NUM_PHILOSOPHERS
        if id == NUM_PHILOSOPHERS - 1:
            first, second = second, first

        forks[first].acquire()
        forks[second].acquire()

        # Task 3: adding random delays.
        time.sleep(random.uniform(0.1, 0.5))

        eat_start = time.time()
        print(f"Philosopher {id} is eating")
        time.sleep(random.uniform(0.1, 0.3))
        # Task 3: adding random delays.
        time.sleep(random.uniform(0.1, 0.5))
        # Task 3: If delays cause some philosophers to be blocked for too long
        # while others keep finishing cycles quickly, starvation can happen.
        forks[second].release()
        forks[first].release()
        eat_end = time.time()

        # Task 5: calculating eating time
        eating_times[id] += (eat_end - eat_start)
        eating_counts[id] += 1

        print(f"Philosopher {id} has finished eating")

        # Task 4: with this approach the ones who have already eaten
        # will gain a delay therefore giving the opportunity for others to eat.
        # As soon as everyone finishes eating, the process will start over.
        eaten_philosophers.add(id)
        if len(eaten_philosophers) == NUM_PHILOSOPHERS:
            eaten_philosophers.clear()

        for i in range(NUM_PHILOSOPHERS):
            avg_think = thinking_times[i] / thinking_counts[i] if thinking_counts[i] > 0 else 0
            avg_eat = eating_times[i] / eating_counts[i] if eating_counts[i] > 0 else 0
            print(f"Philosopher {i}: Avg Thinking t = {avg_think}s, Avg Eating t = {avg_eat}s")


threads = [threading.Thread(target=philosopher, args=(i,)) for i in range(NUM_PHILOSOPHERS)]
for t in threads:
    t.start()
