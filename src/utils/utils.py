import numpy as np
import torch
import argparse

def set_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(seed)
    
def logging(message, path, mode="w+"):
    print(message)
    message += "\n"
    with open(path, mode) as file:
        file.write(message)
        
def set_arguments():
    parser = argparse.ArgumentParser(description='Set up arguments for this experiment.')
    parser.add_argument(
        '--model', type=str,
        help='{cnn, resnet}')
    parser.add_argument(
        '--experiment_title', type=str,
        help='Set up the title of this experiment which will be the file name of model checkpoints and other pickle files.')
    parser.add_argument(
        '--root', default="./", type=str,
        help='The root path of this repository.')
    parser.add_argument(
        '--seeds', default=123, type=int,
        help='The random seed setting.')
    parser.add_argument(
        '--batch_size', default=16, type=int,
        help='The batch size of the trainloader.')
    parser.add_argument(
        '--class_a_index', default=5, type=int,
        help='The class index of the dog.')
    parser.add_argument(
        '--class_b_index', default=3, type=int,
        help='The class index of the cat.')
    parser.add_argument(
        '--class_a_size', default=None, type=float,
        help='The number of the dog samples.')
    parser.add_argument(
        '--class_b_size', default=None, type=float,
        help='The number of the cat samples.')
    parser.add_argument(
        '--class_a_weight', default=1, type=float,
        help='The root path of this repository.')
    parser.add_argument(
        '--class_b_weight', default=1, type=float,
        help='The root path of this repository.')
    parser.add_argument(
        '--epoch', default=1000, type=int,
        help='The number of training epochs.')
    parser.add_argument(
        '--download_cifar10', default=True, type=bool,
        help='Whether we need to download Cifar10 dataset from the website or not.')
    parser.add_argument(
        '--lr', default=0.1, type=float,
        help='The learning rate.')
    parser.add_argument(
        '--use_batchnorm', default=True, type=bool,
        help='Whether we apply Batchnorm after each convolutional layer or not.')
    parser.add_argument(
        '--num_classes', default=10, type=int,
        help='The number of class labels.')
    args = parser.parse_args()

    return args