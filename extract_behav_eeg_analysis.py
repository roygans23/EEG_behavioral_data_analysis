import pandas as pd
import numpy as np

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

def get_rts_of_participant(participant_data_url: str, rt_col_name: str) -> list:
    data = pd.read_csv(participant_data_url)

    target_trials_only_df = filter_df(data, lambda x: x['is_target'] == True)

    # print(f'Number of target trials: {len(target_trials_df)}')

    response_times = target_trials_only_df[rt_col_name]

    # Remove NaN values (Only calculate response time for target stimuli trials)
    response_times = response_times.dropna()
    print(type(response_times))

    return response_times

def get_group_accuracies(csv_group_path_prefix: str, num_of_participants: int) -> list:
    accuracy_list = []
    for i in range(1, num_of_participants + 1):
        csv_path_participant = csv_group_path_prefix.format(i=i)
        accuracy_of_participant = get_accuracy(csv_path_participant, lambda x: ((x['is_target'] == False) & (x['keyResponseStimuliOnset.keys'].isna())) |
                        ((x['is_target'] == True) & (x['keyResponseStimuliOnset.keys'] == 'space')))
        accuracy_list.append(accuracy_of_participant)
            
    return accuracy_list

def plot_group_rt_distribution(csv_group_prefix: list, num_of_participants: int, group_name: str):

    participants_rts_list = [[] for _ in range(num_of_participants)]

    for i in range(1, num_of_participants + 1):
        csv_path = csv_group_prefix.format(i=i)
        participant_rts = get_rts_of_participant(csv_path, 'keyResponseStimuliOnset.rt')
        participants_rts_list[i - 1] = participant_rts

    # Plot response time distribution
    GraphGenerator.plot_subplots([list(range(1, len(participant_rts) + 1)) for participant_rts in participants_rts_list]
                                  ,participants_rts_list, 'Trial Index', 'Response Time (s)', 
                                  'blue', f'{group_name} Participant', f'Response Time Distribution of {group_name} Participant', f'{group_name}_response_time_distribution.png')



def filter_df(data: pd.DataFrame, filter_func: callable) -> pd.DataFrame:
    return data[filter_func(data)]

if __name__ == '__main__':

    plot_group_rt_distribution(config.MANIP_CSV_PATH_PREFIX, config.NUM_OF_PARTICIPANTS_PER_GROUP, 'Meditation')
    plot_group_rt_distribution(config.NO_MANIP_CSV_PATH_PREFIX, config.NUM_OF_PARTICIPANTS_PER_GROUP, 'Control')

    manipulation_rt = get_group_rt(config.MANIP_CSV_PATH_PREFIX, config.NUM_OF_PARTICIPANTS_PER_GROUP)
    no_manipulation_rt = get_group_rt(config.NO_MANIP_CSV_PATH_PREFIX, config.NUM_OF_PARTICIPANTS_PER_GROUP)

    print(f'Mean response time for manipulated group: {np.mean(manipulation_rt[0]):.3f}')
    print(f'Mean response time for non-manipulated group: {np.mean(no_manipulation_rt[0]):.3f}')

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

    GraphGenerator.plot_bar_chart(['Meditation', 'Control'], [mean_rt_manip, mean_rt_no_manip], [mean_std_rt_manip, mean_std_rt_no_manip], 'Group Type', 'Respone Time', 'blue', 'Manipulated Group', 'response_time.png')

    mean_acc_manip = np.mean(manip_accs)
    std_acc_manip = np.std(manip_accs)

    mean_acc_no_manip = np.mean(no_manip_accs)
    std_acc_no_manip = np.std(no_manip_accs)

    GraphGenerator.plot_bar_chart(['Meditation', 'Control'], [mean_acc_manip, mean_acc_no_manip], [std_acc_manip, std_acc_no_manip], 'Group Type', 'Accuracy', 'blue', 'Manipulated Group', 'accuracy.png')