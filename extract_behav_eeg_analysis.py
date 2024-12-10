import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import config
from graph_generator import GraphGenerator

def load_data_from_csv(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    return data

def extract_data(data: pd.DataFrame, cols: list) -> pd.DataFrame:
    # Extract data
    data = data[cols]
    return data

def get_accuracy(data_url: str, filter_func: callable) -> float:
    data = pd.read_csv(data_url)
    data = data[['is_target', 'keyResponseStimuliOnset.keys']]
    data = data.dropna(how='all')

    # print(data)
    correct_trials = filter_df(data, filter_func)
    print(f'Number of correct trials: {len(correct_trials)} / {len(data)}')
    accuracy = len(correct_trials) / len(data)
    return accuracy

def get_rt_metrics(data_url: str, rt_col_name: str) -> pd.DataFrame:
    data = pd.read_csv(data_url)

    target_trials_only_df = filter_df(data, lambda x: x['is_target'] == True)

    # print(f'Number of target trials: {len(target_trials_df)}')

    response_time = target_trials_only_df[rt_col_name]

    # Remove NaN values (Only calculate response time for target stimuli trials)
    response_time = response_time.dropna()

    # Calculate standard deviagtion & mean response time
    mean_rt = np.mean(response_time)
    std_rt = np.std(response_time)

    return mean_rt, std_rt

def get_group_rt(csv_group_path_prefix: str, num_of_participants: int) -> list:
    rt_list = []
    for i in range(1, num_of_participants + 1):
        csv_path = csv_group_path_prefix.format(i=i)
        mean_rt, std_rt = get_rt_metrics(csv_path, 'keyResponseStimuliOnset.rt')
        rt_list.append((mean_rt, std_rt))
    return rt_list

def get_group_accuracies(csv_group_path_prefix: str, num_of_participants: int) -> list:
    accuracy_list = []
    for i in range(1, num_of_participants + 1):
        csv_path_participant = csv_group_path_prefix.format(i=i)
        accuracy_of_participant = get_accuracy(csv_path_participant, lambda x: ((x['is_target'] == False) & (x['keyResponseStimuliOnset.keys'].isna())) |
                        ((x['is_target'] == True) & (x['keyResponseStimuliOnset.keys'] == 'space')))
        accuracy_list.append(accuracy_of_participant)
            
    return accuracy_list

def plot_rt_distribution(response_times: list, trial_indices: int):
    # Create plot
    # plt.scatter(trial_indices, response_times, color='blue', alpha=0.7, label='Response Times')

    plt.plot(trial_indices, response_times, color='red', linestyle='-', linewidth=2, label='Trend Line')


    # Add labels and title
    plt.xlabel('Trial Index', fontsize=12)
    plt.ylabel('Response Time (s)', fontsize=12)
    plt.title('Response Times Over Trials', fontsize=14)

    # Add gridlines
    plt.grid(alpha=0.3)

    # Add legend
    plt.legend()

    # Show plot
    plt.show()

def filter_df(data: pd.DataFrame, filter_func: callable) -> pd.DataFrame:
    return data[filter_func(data)]

if __name__ == '__main__':

    manipulation_rt = get_group_rt(config.MANIP_CSV_PATH_PREFIX, config.NUM_OF_PARTICIPANTS_PER_GROUP)
    no_manipulation_rt = get_group_rt(config.NO_MANIP_CSV_PATH_PREFIX, config.NUM_OF_PARTICIPANTS_PER_GROUP)

    print(f'Mean response time for manipulated group: {np.mean(manipulation_rt[0]):.3f}')
    print(f'Mean response time for non-manipulated group: {np.mean(no_manipulation_rt[0]):.3f}')

    # GraphGenerator.plot_bar_chart([f'Participant {i}' for i in range(1, config.NUM_OF_PARTICIPANTS_PER_GROUP + 1)], manipulation_rt, 'Participant', 'Mean Response Time (s)', 'blue', 'Manipulated Group')

    manip_accs = get_group_accuracies(config.MANIP_CSV_PATH_PREFIX, config.NUM_OF_PARTICIPANTS_PER_GROUP)
    no_manip_accs = get_group_accuracies(config.NO_MANIP_CSV_PATH_PREFIX, config.NUM_OF_PARTICIPANTS_PER_GROUP)

    print(f'Mean accuracy for manipulated group: {np.mean(manip_accs):.3f}')
    print(f'Mean accuracy for non-manipulated group: {np.mean(no_manip_accs):.3f}')

    mean_rt_per_participant_manip = [rt_data[0] for rt_data in manipulation_rt]
    std_rt_per_participant_manip = [rt_data[1] for rt_data in manipulation_rt]

    mean_rt_per_participant_no_manip = [rt_data[0] for rt_data in no_manipulation_rt]
    std_rt_per_participant_no_manip = [rt_data[1] for rt_data in no_manipulation_rt]

    mean_rt_manip = np.mean(mean_rt_per_participant_manip)
    mean_rt_no_manip = np.mean(mean_rt_per_participant_no_manip)

    mean_std_rt_manip = np.mean(std_rt_per_participant_manip)
    mean_std_rt_no_manip = np.mean(std_rt_per_participant_no_manip)
    print(mean_std_rt_manip, mean_std_rt_no_manip)

    GraphGenerator.plot_bar_chart(['Meditation', 'Control'], [mean_rt_manip, mean_rt_no_manip], [mean_std_rt_manip, mean_std_rt_no_manip], 'Group Type', 'Respone Time', 'blue', 'Manipulated Group')
    

    mean_acc_manip = np.mean(manip_accs)
    std_acc_manip = np.std(manip_accs)

    mean_acc_no_manip = np.mean(no_manip_accs)
    std_acc_no_manip = np.std(no_manip_accs)

    GraphGenerator.plot_bar_chart(['Meditation', 'Control'], [mean_acc_manip, mean_acc_no_manip], [std_acc_manip, std_acc_no_manip], 'Group Type', 'Accuracy', 'blue', 'Manipulated Group')

    # Extract data
    # cols_to_extract = ['is_target', 'keyResponseStimuliOnset.keys', 'keyResponseStimuliOnset.rt']
