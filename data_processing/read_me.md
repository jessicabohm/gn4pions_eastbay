# Process Input for Lawrence GNN
Step 1 - preprocess event root files to npy files 
* The input to the Lawrence data processing script is event files, either mixed pi+/- and pi0, or just pi+/-
* This script loads 2 pi+/- files and 1 pi0 file and mixes up the events and saves them to files of only 6000 events (with a ratio of 2 pipm : 1 pi0) - small number of events so they can be processed in parallel in step 2
* To run:
	* Set which files in gn4pions_eastbay/data_processing/preprocess_event_tree_to_npy_config.yaml
		* Been using files from the separate folders of pi0 and pipm files are stored /data/atlas/data/allCellTruthv1
	* Run gn4pions_eastbay/data_processing/preprocess_event_tree_to_npy.py and pass the config file as argument
* Saves the file as ie. pi0_13_pipm_11_12_len_6000_i_0.npy representing which pipm/pi0 files and i represents the index of the data cut
* Takes ~12 min to process 3 files of 400,000 events each (~10 min to load 3 files and ~2 min to process and save) and uses ~10-15 GB of memory
* Note: could be sped up by only loading the features necessary to the models input graph <br><br>

Step 2 - process the event npy files to the input for the Lawrence model
* Uses the Lawrence generator class to convert the events npy to a dataset of graph representation of each cluster and target
* To run:
	* Set which event npy files to process in gn4pions_eastbay/data_processing/preprocess_npy_to_graphs_config.yaml and run gn4pions_eastbay/data_processing/preprocess_npy_to_graphs.py passing the config as an argument
* The set of graphs and targets for the events is saved under the same name as the events npy file - so saving all clusters for the 6000 events loaded
* Takes ~0.5 GB per process, and ~1 min per file processed <br><br>

Note: <br>
* Tested training with no track information, on mixed pion sets that were preprocessed as above
	* Config file: gn4pions_eastbay/train_testing_nbs/baseline.yaml
	* Train script: gn4pions_eastbay/train.py
	* Analysis (using a subset of their analysis functions): gn4pions_eastbay/train_testing_nbs/analysis_example_sub_nb.ipynb
