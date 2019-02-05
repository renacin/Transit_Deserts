# Name:                                             Renacin Matadeen
# Date:                                                02/04/2019
# Title                               Functions Used Determine Distance To Transit Stop
#
# ----------------------------------------------------------------------------------------------------------------------
import multiprocessing
from functions import find_closest_pc
import pandas as pd
# ----------------------------------------------------------------------------------------------------------------------

# Import Massing Data
massing_path = r"C:\Users\renac\Desktop\Transit_Data\Data\Massing.csv"
massing_data_df = pd.read_csv(massing_path)

massing_data_df = massing_data_df.copy()
massing_data_df['LATITUDE'] = massing_data_df['LATITUDE'].astype('float32')
massing_data_df['LONGITUDE'] = massing_data_df['LONGITUDE'].astype('float32')

# Import Transit Data
transit_path = r"C:\Users\renac\Desktop\Transit_Data\Data\Stops.csv"
transit_data_df = pd.read_csv(transit_path)

transit_data_df = transit_data_df.copy()
transit_data_df['Lat'] = transit_data_df['Lat'].astype('float32')
transit_data_df['Long'] = transit_data_df['Long'].astype('float32')

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    # Chunk Massing DataFrame For Multiprocessing
    num_chunks = 4
    len_of_df = len(massing_data_df)
    chunk_size = int(len_of_df / num_chunks)

    # Values Needed For Structure | List Spliting
    t_val = 0
    b_val = chunk_size

    # Split Centroid Dataframe Into Multiple Chunks
    for chunk in range(num_chunks):
        exec("df_" + str(chunk + 1) + " = massing_data_df[" + str(t_val) + ":" + str(b_val) + "]")
        t_val += chunk_size
        b_val += chunk_size

    # Initialize Multiprocessing Units
    for chunk in range(num_chunks):
        exec("p_" + str(chunk + 1) + " = multiprocessing.Process(target=find_closest_pc, args=(" + "df_" + str(chunk + 1) + ", transit_data_df," + str(chunk + 1) + ")) ")

    # Start Multiprocessing
    for chunk in range(num_chunks):
        exec("p_" + str(chunk + 1) + ".start()")
