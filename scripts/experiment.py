from subprocess import Popen, PIPE
from pathlib import Path
import os

def execute_binary(args):
    process = Popen(' '.join(args), shell=True, stdout=PIPE, stderr=PIPE)
    return process

def generate_args(binary, *params):
    arguments = [binary]
    arguments.extend(list(params))
    return arguments

def get_command(dataset, epochs, output_path, full_data_dir, learning_rate):
    command = generate_args("python3 active_train.py",
                            '--dataset', dataset,                             
                            '--epochs', str(epochs),
                            '--output_path', output_path,
                            '--full_data_dir', full_data_dir,
                            '--learning_rate', str(learning_rate),
                            '--mode', 'train',
                            '--batch_size', '2', 
                            '--model_type', 'GIN',
                            '--embed_type', 'freq',
                            '--active_iters', '0',
                            '--matching', 'iso',
                            '--multi_task', '\"\"')
    return command

if __name__ == '__main__':
    dataset = 'yeast'
    full_data_dir = '/home/lxhq/Documents/workspace/dataset/'
    output_dir = 'outputs/{}/'.format(dataset)
    if not Path(output_dir).is_dir():
        os.makedirs(output_dir)
    learning_rates = [1e-3, 5e-4, 1e-4]
    epochs = [150]
    repeat = 4
    for epoch in epochs:
        for learning_rate in learning_rates:
            processes = []
            for idx in range(repeat):
                output_name = 'baseline_{}_{}_{}.txt'.format(epoch, learning_rate, idx)
                output_path = output_dir + output_name
                command = get_command(dataset, epoch, output_path, full_data_dir, learning_rate)
                processes.append(execute_binary(command))
            for process in processes:
                process.wait()