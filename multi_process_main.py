import csv
import datetime
import multiprocessing as mp
import os
import time
from functools import partial
from typing import List

from tqdm import tqdm

from algo_genetique import algo_genetique
from item import Item
from quality_population_enum import QualityPopulationEnum
from result import Result

from csv_column_name import CsvColumnName


def task_unpacker(packed_data):
    task_index, params, max_capacity, items, file_name, total_tasks = packed_data
    return process_single_task(task_index, params, max_capacity, items, file_name, total_tasks)


def get_data_from_file(file_name: str) -> (int, List[Item]):
    items = []
    max_capacity = 0

    with open("data/{}".format(file_name), "r") as file:
        for index, line in enumerate(file):
            # MAX_CAPACITY
            if index == 4:
                max_capacity = int(line.split("MAX_CAPACITY: ")[1])

            # ITEMS
            if index >= 7:
                line_info = line.split(" ")
                items.append(Item(id=int(line_info[0]), profit=int(line_info[1]), weight=int(line_info[2])))

    return max_capacity, items


def write_data_in_file(file_name: str, results: List[Result]):
    header = [
        CsvColumnName.PROFIT.name,
        CsvColumnName.WEIGHT.name,
        CsvColumnName.ITEMS.name,
        CsvColumnName.NB_GENERATION.name,
        CsvColumnName.NB_POPULATION.name,
        CsvColumnName.NB_BEST.name,
        CsvColumnName.PROBA_CROSSOVER.name,
        CsvColumnName.PROBA_MUTATION.name,
        CsvColumnName.TYPE_INIT_POP.name,
        CsvColumnName.TIME_EXECUTION.name
    ]

    with open('result/{}.csv'.format(file_name), 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(header)

        for result in results:
            writer.writerow(result.result_to_csv())


def process_single_task(task_index, params, max_capacity, items, file_name, total_tasks):
    number_generation, number_population, nb_best, proba_crossover, proba_mutation, type_init_population = params

    start_time = time.time()
    try:
        current_solution = algo_genetique(
            number_generation, number_population, max_capacity, items,
            nb_best, proba_crossover, proba_mutation, False, type_init_population
        )
    except Exception as e:
        print(f"Une exception est survenue : {e} avec les paramètres suivants :\n"
              f" - Nombre de génération : {number_generation}\n"
              f" - Nombre de population : {number_population}\n"
              f" - Nombre de best : {nb_best}\n"
              f" - Probabilité crossover : {proba_crossover}\n"
              f" - Probabilité mutation : {proba_mutation}\n"
              f" - Type init population : {type_init_population.name}\n")

        return "ERROR", file_name, None, task_index

    end_time = time.time()

    result = Result(
        current_solution, items, number_generation, number_population,
        nb_best, proba_crossover, proba_mutation, type_init_population,
        end_time - start_time
    )

    return "SUCCESS", file_name, result, task_index


def format_time(seconds):
    """Convert seconds to a human-readable format"""
    return str(datetime.timedelta(seconds=int(seconds)))


def main():
    folder_path = "data"
    files = os.listdir(folder_path)

    proba_crossovers = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    proba_mutations = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    quality_init_population = [QualityPopulationEnum.LOW, QualityPopulationEnum.MEDIUM, QualityPopulationEnum.HIGH]

    # Number of processes to use
    num_processes = mp.cpu_count() - 1  # Leave one CPU free for system tasks
    print(f"Using {num_processes} processes")

    # Track overall progress across all files
    total_files = len(files)
    file_counter = 0

    overall_start_time = time.time()

    files_100 = [6, 3, 0]
    files_1000 = [7, 4, 1]
    files_10000 = [2]
    total_files = 3

    for file_index in files_10000:
        file_name = files[file_index]
        file_counter += 1
        file_start_time = time.time()

        # Calculate overall progress for files
        elapsed_total = time.time() - overall_start_time
        if file_counter > 1:
            estimated_total = elapsed_total / (file_counter - 1) * total_files
            time_remaining_total = estimated_total - elapsed_total
            print(
                f"\n[{file_counter}/{total_files}] Progress: {file_counter / total_files * 100:.1f}% - Est. remaining: {format_time(time_remaining_total)}")

        print(f"Début itération fichier {file_name} !")

        max_capacity, items = get_data_from_file(file_name)

        # Create a list of all parameter combinations
        all_params = []

        for proba_crossover in proba_crossovers:
            for proba_mutation in proba_mutations:
                for type_init_population in quality_init_population:
                    all_params.append((
                        300, 100, 50,
                        proba_crossover, proba_mutation, type_init_population
                    ))

        # for number_generation in range(60, 360, 100):
        #     for number_population in range(10, 310, 100):
        #         for nb_best in range(int(number_population * 0.2), number_population, int(number_population / 5)):
        #             for type_init_population in quality_init_population:
        #                 all_params.append((
        #                     number_generation, number_population, nb_best,
        #                     0.5, 0.5, type_init_population
        #                 ))
        #             # for proba_crossover in proba_crossovers:
        #             #     for proba_mutation in proba_mutations:
        #             #         for type_init_population in quality_init_population:
        #             #             all_params.append((
        #             #                 number_generation, number_population, nb_best,
        #             #                 proba_crossover, proba_mutation, type_init_population
        #             #             ))

        total_tasks = len(all_params)
        print(f"Total tasks for file {file_name}: {total_tasks}")
        # Prepare data for multiprocessing
        task_data = []

        for i, params in enumerate(all_params[::-1]):
            task_data.append((i, params, max_capacity, items, file_name, total_tasks))

        # Initialize results list and counters
        results = []
        error_results = []

        # Create a pool of workers
        with mp.Pool(processes=num_processes) as pool:
            # Use tqdm to track progress with detailed information
            progress_bar = tqdm(
                total=total_tasks,
                desc=f"[{file_counter}/{total_files}] {file_name}",
                unit="task"
            )

            task_times = []
            completed = 0

            # Start time for the current batch
            batch_start_time = time.time()

            # Process tasks
            for status, file, result, task_index in pool.imap_unordered(task_unpacker, task_data):
                completed += 1
                progress_bar.update(1)

                # Record task completion
                task_time = time.time() - batch_start_time
                task_times.append(task_time)
                batch_start_time = time.time()

                # Calculate and update progress bar with estimates
                if len(task_times) > 5:  # Need some samples for better estimation
                    avg_time_per_task = sum(task_times[-50:]) / len(
                        task_times[-50:])  # Use last 50 tasks for moving average
                    tasks_remaining = total_tasks - completed
                    est_time_remaining = avg_time_per_task * tasks_remaining / num_processes

                    progress_bar.set_postfix({
                        'avg': f"{avg_time_per_task:.2f}s/task",
                        'remaining': format_time(est_time_remaining),
                        'completed': f"{completed}/{total_tasks}"
                    })

                if status == "SUCCESS":
                    results.append(result)
                else:
                    error_results.append(result)

            progress_bar.close()

        # Write results to file
        write_data_in_file('test-proba-' + file_name, results)

        # If there were errors, write them to the error file
        if error_results:
            write_data_in_file(file_name + "_erreur", error_results)

        file_elapsed = time.time() - file_start_time
        print(f"Fichier {file_name} terminé en {format_time(file_elapsed)} !")


if __name__ == "__main__":
    mp.freeze_support()
    main()
