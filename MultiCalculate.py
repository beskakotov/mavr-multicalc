import multiprocessing as mp
from tkinter import filedialog, Tk
from loguru import logger
from shutil import copy
from subprocess import call
from time import monotonic
import keyring
import os
import psutil

def prepare_directory():
    root = Tk()
    root.withdraw()
    print('Choose directory for phase reconstruction')
    folder_selected = filedialog.askdirectory()
    
    list_of_files = []
    for root, dirs, files in os.walk(folder_selected):
        for f in files:
            if f.lower().endswith('.dat'):
                list_of_files.append(os.path.join(root, f))
                copy(os.path.join(__bispectr_path__, 'template', 'template_uint16.dat.xfs'), os.path.join(root, f+'.xfs'))
            elif f.lower().endswith('.spe'):
                list_of_files.append(os.path.join(root, f))
                copy(os.path.join(__bispectr_path__, 'template', 'template.SPE.xfs'), os.path.join(root, f+'.xfs'))
    return list_of_files

def calculate(path_for_calculate):
    start_calculate = monotonic()
    call([os.path.join(keyring.get_password('bispectr', 'path'), 'bispectr64.exe'), path_for_calculate])
    end_calculate = monotonic()
    print(f'[DONE] {path_for_calculate} : {end_calculate-start_calculate:.2f}sec')

def get_bispectr_path():
    output_path = keyring.get_password('bispectr', 'path')
    if os.path.exists(output_path):
        return output_path
    else:
        return set_bispectr_path()

def set_bispectr_path():
    root = Tk()
    root.withdraw()
    print('Choose "Speckle" software directory')
    folder_selected = filedialog.askdirectory()
    if os.path.exists(folder_selected):
        keyring.set_password('bispectr', 'path', folder_selected)
        return folder_selected
    else:
        raise OSError(f'Directory "{folder_selected}" not found')

def delete_inactive_processes(processes_list):
    output_processes_list = []
    for process in processes_list:
        if process.is_alive():
            output_processes_list.append(process)
    return output_processes_list

if __name__ == '__main__':

    __bispectr_path__ = get_bispectr_path()
    __template_path__ = os.path.join(__bispectr_path__, 'template')

    list_of_files = prepare_directory()

    processes_by_cpu = mp.cpu_count() - 2
    if processes_by_cpu < 1:
        processes_by_cpu = 1

    processes_by_ram = int(psutil.virtual_memory().available / 1024 ** 3 / 4)

    __AVAILABLE_PROCESSES__ = processes_by_cpu if processes_by_cpu < processes_by_ram else processes_by_ram
    if __AVAILABLE_PROCESSES__ < 1:
        __AVAILABLE_PROCESSES__ = 1

    processes_list = []

    print(f'Max calculation processes: {__AVAILABLE_PROCESSES__}')

    start_of_calculation = monotonic()
    while True:
        if not processes_list and not list_of_files:
            break

        if processes_list:
            processes_list = delete_inactive_processes(processes_list)
        
        if list_of_files and len(processes_list) < __AVAILABLE_PROCESSES__:
            new_process = mp.Process(target=calculate, args=(list_of_files.pop(0), ))
            new_process.start()
            processes_list.append(new_process)

    end_of_calculation = monotonic()
