import argparse
import numpy as np
import yaml
import uproot

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", default=None)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()

    # load config info
    config_file = args.config
    config = yaml.load(open(config_file), Loader=yaml.FullLoader)

    pipm1_files = config["pipm1_files"]
    pipm2_files = config["pipm2_files"]
    pi0_files = config["pi0_files"]
    save_dir = config["save_dir"]

    keys = ["eventNumber", "nCluster", "truthPartE", "truthPartPt", "cluster_E", "cluster_E_LCCalib", "cluster_EM_PROBABILITY", "cluster_E", "cluster_HAD_WEIGHT", "truthPartPdgId", "cluster_ENG_CALIB_TOT", "cluster_Eta", "cluster_cell_ID", "cluster_cell_E"]# , "cluster_cell_ID", "cluster_cell_hitsE_EM", "cluster_cell_hitsE_nonEM", "cluster_cell_E", "cell_geo_eta", "cell_geo_rPerp", "cell_geo_phi", "cluster_Pt", ]

    # num events to save to mixed file - equal num from pipm1, pipm2, pi0 files
    len_file = 6000
    events_per_file = int(len_file / 3)
    np.random.seed(0) # always use seed 0


    for i, pi0_file in enumerate(pi0_files): # NOTE: shouldn't use array of files or this will mess up rand shuffling being consistent over calls to this script
        # load event tree to numpy arrays
        pi0_event_data = uproot.open(pi0_file + ":EventTree").arrays(library="np")
        print("loaded pi0 event data")
        pipm1_event_data = uproot.open(pipm1_files[i] + ":EventTree").arrays(library="np")
        print("loaded pipm1 event data")
        pipm2_event_data = uproot.open(pipm2_files[i] + ":EventTree").arrays(library="np")
        print("loaded pipm2 event data")

        pi0_num = int(pi0_file.split("_")[-1].split(".")[0])
        pipm1_num = int(pipm1_files[i].split("_")[-1].split(".")[0])
        pipm2_num = int(pipm2_files[i].split("_")[-1].split(".")[0])

        # split up data and save to npy files of len_file events (6000 => 2000 pi0, 4000 pi+/-)
        file_indicies = np.arange(len(pi0_event_data["eventNumber"]))
        event_data_indicies = np.arange(len_file)
        np.random.shuffle(file_indicies)

        num_mixed_files = int(np.min([len(pi0_event_data["eventNumber"])/events_per_file, len(pipm1_event_data["eventNumber"])/events_per_file, len(pipm2_event_data["eventNumber"])/events_per_file]))
        
        for j in range(num_mixed_files):
            np.random.shuffle(event_data_indicies)
            pion_data = {}
            for key in keys:
                pion_data[key] = np.zeros(len_file, dtype=object)
                pion_data[key][event_data_indicies] = np.concatenate((pi0_event_data[key][file_indicies[j*events_per_file:(j+1)*events_per_file]],
                    pipm1_event_data[key][file_indicies[j*events_per_file:(j+1)*events_per_file]], pipm2_event_data[key][file_indicies[j*events_per_file:(j+1)*events_per_file]]))

            np.save(save_dir + "/pi0_" + str(pi0_num) + "_pipm_" + str(pipm1_num) + "_" + str(pipm2_num) + "_len_" + str(len_file) + "_i_" + str(j), pion_data, allow_pickle=True)
            #np.save(save_dir + "/pipm_" + str(pipm1_num) + "_" + str(pipm2_num) + "_" + str(pi0_num) + "_len_" + str(len_file) + "_i_" + str(j), pion_data, allow_pickle=True)


