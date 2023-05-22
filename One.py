import subprocess
import time
import math

client_ranges = {
     'client1': [(0, 250), (250, 500), (500, 750), (750, 1000), (1000, 1250), (1250, 1500), (1500, 1750), (1750, 2000), (200>
}

def run_node(node_name, start, end, cumulative_time=0):
    start_time = time.time()
    cmd = f'sudo kubectl run {node_name}-primes --image=abdi1999/primes-image --restart=Never --command -- python generate_p>
    subprocess.run(cmd, shell=True)
    end_time = time.time()
    elapsed_time = cumulative_time + (end_time - start_time)
    print(f"{node_name}: {elapsed_time:.2f}")
    return elapsed_time

def delete_pods():
    print("\nDeleting all pods...")
    cmd = 'sudo kubectl delete pods --all'
    subprocess.run(cmd, shell=True)

def run_simulation():
    delete_pods()
    results = []
    total_time = 0.0

    # Run jobs in sequence for all ranges
    for node_name, ranges in client_ranges.items():
        cumulative_time = 0.0
        for i, (start, end) in enumerate(ranges):
            print(f"\nRange: {start}-{end}")
            elapsed_time = run_node(node_name, start, end, cumulative_time)
            cumulative_time = elapsed_time
            results.append(elapsed_time)
            print("{:<10} {:<15.2f}".format(f"{node_name}-{i+1}", elapsed_time * 1000))
            total_time += elapsed_time
            delete_pods()
    average_time = total_time / len(results)
    print(f"\nAverage time per range: {average_time:.2f} seconds")
    deviation = [(elapsed_time - average_time) ** 2 for elapsed_time in results]
    standard_d = math.sqrt(sum(deviation) / (len(results) - 1))
    print(f"\nStandard deviation per range: {standard_d:.2f} seconds")

if __name__ == '__main__':
    run_simulation()
