import os
import psutil

def set_cpu_affinity(process_id, cpus):
    try:
        process = psutil.Process(process_id)
        process.cpu_affinity(cpus)
        print(f"Process {process_id} is now running on CPU(s): {cpus}")
    except Exception as e:
        print(f"Error setting CPU affinity: {e}")

if __name__ == "__main__":
    process_id = os.getpid()  # 获取当前进程 ID
    cpus = [0, 1]  # 指定 CPU 核心的列表，例如：0 和 1 号核心
    set_cpu_affinity(process_id, cpus)
