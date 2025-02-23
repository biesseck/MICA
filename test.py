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

from jobs import test

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


# BERNARDO
# --cfg /media/biesseck/DATA/BernardoBiesseck/BOVIFOCR_project/GitHub/MICA/configs/mica_Bernardo.yml --test_dataset NOW


if __name__ == '__main__':
    from configs.config import parse_args

    # BERNARDO
    if len(sys.argv) < 2:
        sys.argv.append('--cfg')
        sys.argv.append('/media/biesseck/DATA/BernardoBiesseck/BOVIFOCR_project/GitHub/MICA/configs/mica_Bernardo.yml')
        sys.argv.append('--test_dataset')
        sys.argv.append('NOW')

    cfg, args = parse_args()

    if cfg.cfg_file is not None:
        exp_name = cfg.cfg_file.split('/')[-1].split('.')[0]
        cfg.output_dir = os.path.join('./output', exp_name)

    cudnn.benchmark = False
    cudnn.deterministic = True
    torch.cuda.empty_cache()
    num_gpus = torch.cuda.device_count()

    # BERNARDO
    if num_gpus == 0:
        num_gpus = 1    # cpu

    mp.spawn(test, args=(num_gpus, cfg, args), nprocs=num_gpus, join=True)

    exit(0)
