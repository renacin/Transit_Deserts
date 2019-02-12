# Name:                                             Renacin Matadeen
# Date:                                               02/09/2019
# Title                               Functions Used Determine Distance To Transit Stop
#
# ----------------------------------------------------------------------------------------------------------------------
# import multiprocessing as mp
# import psutil
# from psutil import virtual_memory
# # ----------------------------------------------------------------------------------------------------------------------
# # Sys Memory Count
# mem = virtual_memory()
# sys_mem = mem.available # In Bytes Divide By 1048576 For Megabytes
#
# # CPU Count
# cpu_count_hyper = psutil.cpu_count()
# cpu_count_no_hyper = psutil.cpu_count(logical=False)
#
# # Print Information
# print("Number Of Cores: " + str(cpu_count_no_hyper), "| " + str(cpu_count_hyper))
# # print("CPU Stats: " + str(psutil.cpu_freq())) # Expressed In Mhz
# print("Available Memory: " + str(round(sys_mem / 1048576, 2)) + "MB")


import pandas as pd
columns=["Test_1", "Test_2", "Test_3"]
test_df = pd.DataFrame(columns=columns)

print(test_df)
