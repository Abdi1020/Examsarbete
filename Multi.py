import subprocess
import time
from multiprocessing import Process, Manager

client_ranges = {
    'client1': [(0, 250), (1000, 1250), (2000, 2250)],
    'client2': [(250, 500), (1250, 1500), (2250, 2500)],
    'client3': [(500, 750), (1500, 1750), (2500, 2750)],
    'client4': [(750, 1000), (1750, 2000), (2750, 3000)],
}

def run_node(node_name, start, end, results):
    start_time = time.time()
    cmd = f'sudo kubectl run {node_name}-primes --image=abdi1999/primes-image --restart=Never --command -- python generate_p>
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
        results = manager.dict()
        for client in client_ranges:
            results[client] = manager.list()

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
        for client in client_ranges:
            print(f"\n{client} total time: {results[client][-1]:.2f}s")

if __name__ == '__main__':
    run_simulation()
