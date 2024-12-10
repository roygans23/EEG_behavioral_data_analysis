import pandas as pd
import numpy as np

import config

def load_data_from_csv(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    return data

def extract_data(data: pd.DataFrame, cols: list) -> pd.DataFrame:
    # Extract data
    data = data[cols]
    return data

def get_target_trials(data: pd.DataFrame, target_col_name: str, target_col_val: str) -> pd.DataFrame:

    return data[data[target_col_name] == target_col_val]

def get_accuracy(data_url: str) -> float:
    data = pd.read_csv(data_url)
    data = data[['is_target', 'keyResponseStimuliOnset.keys']]
    data = data.dropna(how='all')

    # print(data)
    correct_trials = data[((data['is_target'] == False) & (data['keyResponseStimuliOnset.keys'].isna())) |
                           ((data['is_target'] == True) & (data['keyResponseStimuliOnset.keys'] == 'space'))]
    print(f'Number of correct trials: {len(correct_trials)} / {len(data)}')
    accuracy = len(correct_trials) / len(data)
    return accuracy

def get_rt_metrics(data_url: str, rt_col_name: str) -> pd.DataFrame:
    data = pd.read_csv(data_url)
    target_trials_df = get_target_trials(data, 'is_target', True)

    # print(f'Number of target trials: {len(target_trials_df)}')

    response_time = target_trials_df[rt_col_name]

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
        rt_list.append(mean_rt)
    return rt_list


if __name__ == '__main__':

    manipulation_rt = get_group_rt(config.MANIP_CSV_PATH_PREFIX, config.NUM_OF_PARTICIPANTS_PER_GROUP)
    no_manipulation_rt = get_group_rt(config.NO_MANIP_CSV_PATH_PREFIX, config.NUM_OF_PARTICIPANTS_PER_GROUP)

    print(f'Mean response time for manipulated group: {np.mean(manipulation_rt)}')
    print(f'Mean response time for non-manipulated group: {np.mean(no_manipulation_rt)}')


    # # Calculate accuracy
    # data = pd.read_csv('data/meditation/manip1.csv')
    # data = data[['is_target', 'keyResponseStimuliOnset.keys']]
    # print(data)
    # correct_trials = data[((data['is_target'] == False) & (data['keyResponseStimuliOnset.keys'].isna())) |
    #                        ((data['is_target'] == True) & (data['keyResponseStimuliOnset.keys'] == 'space'))]
    # print(correct_trials)
    # accuracy = len(correct_trials) / len(data)
    # print(f'Accuracy: {accuracy}')

    print('\n')

    accuracy_list = []
    no_accuracy_list = []

    for i in range(1, config.NUM_OF_PARTICIPANTS_PER_GROUP + 1):
            csv_path = config.MANIP_CSV_PATH_PREFIX.format(i=i)
            accuracy = get_accuracy(csv_path)
            accuracy_list.append(accuracy)
    
    print(f'Mean accuracy for manipulated group: {np.mean(accuracy_list)}')

    for i in range(1, config.NUM_OF_PARTICIPANTS_PER_GROUP + 1):
            csv_path = config.NO_MANIP_CSV_PATH_PREFIX.format(i=i)
            accuracy = get_accuracy(csv_path)
            no_accuracy_list.append(accuracy)
    
    print(f'Mean accuracy for no manipulated group: {np.mean(no_accuracy_list)}')
    
    # Extract data
    cols_to_extract = ['is_target', 'keyResponseStimuliOnset.keys', 'keyResponseStimuliOnset.rt']
