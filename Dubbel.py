import subprocess
import time
from multiprocessing import Process, Manager

client_ranges = {
    'client1': [(0, 250), (500, 750), (1000, 1250), (1500, 1750), (2000, 2250), (2500, 2750)],
    'client2': [(250, 500), (750, 1000), (1250, 1500), (1750, 2000), (2250, 2500),(2750, 3000)],
}

def run_node(node_name, start, end, results):
    cmd = f'sudo kubectl run {node_name}-primes --image=abdi1999/primes-image --restart=Never --command -- python generate_p>
    start_time = time.time()
    subprocess.run(cmd, shell=True)
    end_time = time.time()
    elapsed_time = end_time - start_time
    if results[node_name]:
        elapsed_time += results[node_name][-1]
    print(f"{node_name} range {start}-{end}: {elapsed_time:.2f}s")
    results[node_name].append(elapsed_time)

def delete_pods():
    print("\nDeleting all pods...")
    cmd = 'sudo kubectl delete pods --all'
    subprocess.run(cmd, shell=True)

def run_simulation():
    with Manager() as manager:
        results = manager.dict({
            'client1': manager.list(),
            'client2': manager.list(),
        })

        for i in range(len(client_ranges['client1'])):
            delete_pods()
            processes = []

            for node_name in client_ranges.keys():
                start, end = client_ranges[node_name][i]
                print(f"\nRange: {start}-{end}")
                p = Process(target=run_node, args=(node_name, start, end, results))
                processes.append(p)
                p.start()

            for p in processes:
                p.join()

        print("\nResults:")
        for node_name, times in results.items():
            total_time = sum(times)
            print(f"{node_name} total time: {total_time:.2f}s")

if __name__ == '__main__':
    run_simulation()
