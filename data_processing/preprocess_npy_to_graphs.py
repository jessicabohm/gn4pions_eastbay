import argparse
import numpy as np
import yaml
import sys
sys.path.append('/home/jbohm/start_tf/gn4pions_eastbay/')
from gn4pions.modules.data import GraphDataGenerator

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", default=None, type=str)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()

    # load config info
    config_file = args.config
    config = yaml.load(open(config_file), Loader=yaml.FullLoader)

    pion_dir = config["pion_dir"]
    save_dir = config["save_dir"]
    pi0_file_nums = config["pi0_file_nums"]
    pipm1_file_nums = config["pipm1_file_nums"]
    pipm2_file_nums = config["pipm2_file_nums"]
    len_file = config["len_file"]
    i_low = config["i_low"]
    i_high = config["i_high"]
    num_procs = config["num_procs"]

    for j, pi0_num in enumerate(pi0_file_nums):
        pion_files = list(map(lambda i: pion_dir + "/pi0_" + str(pi0_num) + "_pipm_" + str(pipm1_file_nums[j]) + "_" + str(pipm2_file_nums[j]) + "_len_" + str(len_file) + "_i_" + str(i) + ".npy", np.arange(i_low, i_high + 1)))

        GraphDataGenerator(pi0_file_list=None,
            pion_file_list=pion_files,
            cellGeo_file="/data/atlas/data/allCellTruthv1/pi0/user.mswiatlo.27153451.OutputStream._000001.root",
            batch_size=1, # doesn't matter for processing
            shuffle=False,
            num_procs=num_procs,
            preprocess=True,
            output_dir=save_dir,
            keep_file_name=True)