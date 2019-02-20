# Name:                                             Renacin Matadeen
# Date:                                                02/12/2019
# Title               Functions Used Determine Distance To Transit Stop, Update For Brampton Transit
#
# ----------------------------------------------------------------------------------------------------------------------
import multiprocessing as mp
from psutil import virtual_memory
from functions import find_closest_pc, comb_df
import pandas as pd
# ----------------------------------------------------------------------------------------------------------------------

# Import Massing Data
massing_path = r"C:\Users\renac\Documents\Data\Brampton_Massing\Raw_Data\Data.csv"
massing_data_df = pd.read_csv(massing_path)

massing_data_df = massing_data_df.copy()
massing_data_df['Latitude'] = massing_data_df['Latitude'].astype('float32')
massing_data_df['Longitude'] = massing_data_df['Longitude'].astype('float32')

# Import Transit Data
transit_path = r"C:\Users\renac\Documents\Data\Brampton_Transit\Transit_Stops.csv"
transit_data_df = pd.read_csv(transit_path)

transit_data_df = transit_data_df.copy()
transit_data_df['Latitude'] = transit_data_df['Latitude'].astype('float32')
transit_data_df['Longitude'] = transit_data_df['Longitude'].astype('float32')

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    # Print basic Information For User
    core_count = int(mp.cpu_count())
    mem = virtual_memory()
    sys_mem = mem.available # In Bytes Divide By 1048576 For Megabytes

    # Info
    print("Number Of Cores: " + str(core_count))
    print("Available Memory: " + str(round(sys_mem / 1048576, 2)) + "MB" + "\n")
    print("-------Worker Progress-------")

    # Chunk Massing DataFrame For Multiprocessing
    num_chunks = core_count
    len_of_df = len(massing_data_df)
    chunk_size = int(len_of_df / num_chunks)

    # Values Needed For Structure | List Spliting
    t_val = 0
    b_val = chunk_size

    # Create A Queue Instance
    manager = mp.Manager()
    return_dict = manager.dict()

    # Split Centroid Dataframe Into Multiple Chunks
    for chunk in range(num_chunks):
        exec("df_" + str(chunk + 1) + " = massing_data_df[" + str(t_val) + ":" + str(b_val) + "]")
        t_val += chunk_size
        b_val += chunk_size

    # Initialize Multiprocessing Units
    for chunk in range(num_chunks):
        exec("p_" + str(chunk + 1) + " = mp.Process(target=find_closest_pc, args=(df_" + str(chunk + 1) + ", transit_data_df," + str(chunk + 1) + ")) ")

    # Start Multiprocessing
    for chunk in range(num_chunks):
        exec("p_" + str(chunk + 1) + ".start()")

    # Combine CSV Files
    comb_df(r"C:\Users\renac\Documents\Data\Brampton_Massing\Raw_Data\Data")
