# -*- coding: utf-8 -*-

# Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. (MPG) is
# holder of all proprietary rights on this computer program.
# You can only use this computer program if you have closed
# a license agreement with MPG or you get the right to use the computer
# program from someone who is authorized to grant you that right.
# Any use of the computer program without a valid license is prohibited and
# liable to prosecution.
#
# Copyright©2022 Max-Planck-Gesellschaft zur Förderung
# der Wissenschaften e.V. (MPG). acting on behalf of its Max Planck Institute
# for Intelligent Systems. All rights reserved.
#
# Contact: mica@tue.mpg.de


import os
import sys

import torch
import torch.backends.cudnn as cudnn
import torch.multiprocessing as mp

from jobs import train

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# BERNARDO
import numpy as np
import random
import socket
host_name = socket.gethostname()


if __name__ == '__main__':
    from configs.config import parse_args

    # BERNARDO
    print('Running on \'' + host_name + '\' machine...')

    if len(sys.argv) < 2:
        if host_name == 'OptiPlex-3080':
            sys.argv.append('--cfg')
            sys.argv.append('/media/biesseck/DATA/BernardoBiesseck/BOVIFOCR_project/GitHub/MICA/configs/mica_OptiPlex-3080.yml')
            sys.argv.append('--test_dataset')
            sys.argv.append('NOW')
            sys.argv.append('--checkpoint')
            sys.argv.append('')
        elif host_name == 'duo':
            sys.argv.append('--cfg')
            sys.argv.append('/home/bjgbiesseck/GitHub/MICA/configs/mica_duo.yml')
            sys.argv.append('--test_dataset')
            sys.argv.append('NOW')
            sys.argv.append('--checkpoint')
            sys.argv.append('')

    cfg, args = parse_args()

    if cfg.cfg_file is not None:
        exp_name = cfg.cfg_file.split('/')[-1].split('.')[0]
        cfg.output_dir = os.path.join('./output', exp_name)

    cudnn.benchmark = False
    cudnn.deterministic = True
    torch.cuda.empty_cache()
    num_gpus = torch.cuda.device_count()

    # BERNARDO (from 'https://github.com/pytorch/pytorch/issues/45042#issuecomment-701115885' - on 29 Sep 2020)
    seed = 440
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.backends.cudnn.enabled = True
    torch.backends.cudnn.benchmark = True

    # BERNARDO
    # print('train.py: num_gpus:', num_gpus, '   cfg:', cfg)
    print('train.py: num_gpus:', num_gpus)

    # mp.spawn(train, args=(num_gpus, cfg), nprocs=num_gpus, join=True)   # Original
    mp.spawn(train, args=(num_gpus, cfg), nprocs=1, join=True)   # BERNARDO
    # train(rank=num_gpus, world_size=num_gpus, cfg=cfg)

    exit(0)
