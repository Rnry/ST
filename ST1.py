import threading
import time
import random
# Task 2: number of philosophers 5->7
NUM_PHILOSOPHERS = 7
#Deadlocks do not occur either way (after changing the number of philosophers to 6, 7 and 10)
forks = [threading.Semaphore(1) for _ in range(NUM_PHILOSOPHERS)]

eaten_philosophers = set()

thinking_times = {i: 0 for i in range(NUM_PHILOSOPHERS)}
eating_times = {i: 0 for i in range(NUM_PHILOSOPHERS)}
thinking_counts = {i: 0 for i in range(NUM_PHILOSOPHERS)}
eating_counts = {i: 0 for i in range(NUM_PHILOSOPHERS)}

def philosopher(id):
    global eaten_philosophers
    global thinking_times
    global eating_times
    global thinking_counts
    global eating_counts

    while True:
        #Task 4: creating a priority system.
        while id in eaten_philosophers and len(eaten_philosophers) < NUM_PHILOSOPHERS:
            time.sleep(0.1)

        think_start = time.time()
        print(f"Philosopher {id} is thinking")
        time.sleep(random.uniform(0.1, 0.5))
        think_end = time.time()

        #Task 5 :calculating thinking time
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
           #Task 3: adding random delays.
        time.sleep(random.uniform(0.1, 0.5))
        #Task 3: If delays cause some philosophers to be blocked for too long while others keep finishing cycles quickly, starvation can happen.
        forks[second].release()
        forks[first].release()
        eat_end = time.time()

         #Task 5: calculating eating time
        eating_times[id] += (eat_end - eat_start)
        eating_counts[id] += 1

        print(f"Philosopher {id} has finished eating")

        #Task 4: with this approach the ones who have already eaten will gain a delay therefore giving the opportunity for others to eat. 
        #As soon as everyone finishes eating, the process will start over.
        eaten_philosophers.add(id)
        if len(eaten_philosophers) == NUM_PHILOSOPHERS:
            eaten_philosophers.clear()


        for i in range(NUM_PHILOSOPHERS):
            avg_think = thinking_times[i] / thinking_counts[i] if thinking_counts[i] > 0 else 0
            avg_eat = eating_times[i] / eating_counts[i] if eating_counts[i] > 0 else 0
            print(f"Philosopher {i}: Avg Thinking Time = {avg_think}s, Avg Eating Time = {avg_eat}s")

threads = [threading.Thread(target=philosopher, args=(i,)) for i in
range(NUM_PHILOSOPHERS)]
for t in threads:
    t.start()

#Task 5 output:
'''
Philosopher 0: Avg Thinking Time = 0.33431265904353213s, Avg Eating Time = 0.45732890642606294s
Philosopher 1: Avg Thinking Time = 0.2846822371849647s, Avg Eating Time = 0.5677898663740891s
Philosopher 2: Avg Thinking Time = 0.26495649264408994s, Avg Eating Time = 0.4615902533897987s
Philosopher 3: Avg Thinking Time = 0.3437967300415039s, Avg Eating Time = 0.5304339298835168s
Philosopher 4: Avg Thinking Time = 0.30418073214017427s, Avg Eating Time = 0.5044113122499906s
Philosopher 5: Avg Thinking Time = 0.3297857871422401s, Avg Eating Time = 0.5269032991849459s
Philosopher 6: Avg Thinking Time = 0.268082306935237s, Avg Eating Time = 0.5432999684260442s
Philosopher 7: Avg Thinking Time = 0.2781997277186467s, Avg Eating Time = 0.5300878011263334s
Philosopher 8: Avg Thinking Time = 0.31453789197481596s, Avg Eating Time = 0.5165378313798171s
Philosopher 9: Avg Thinking Time = 0.29631913625277007s, Avg Eating Time = 0.491009363761315s
'''

#Task 6: The arbiter approach ensures fairness by preventing starvation but may slightly reduce throughput due 
#to controlled access to forks. The fork-ordering approach allows higher throughput but can lead to starvation 
#if unlucky philosophers keep missing their turn.
