# Name:                                             Renacin Matadeen
# Date:                                               02/04/2019
# Title                               Functions Used Determine Distance To Transit Stop
#
# ----------------------------------------------------------------------------------------------------------------------
import geopy
from geopy.distance import VincentyDistance, geodesic
import pandas as pd
import time
import math
# ----------------------------------------------------------------------------------------------------------------------

# This Function Will Return A DF With Values That Are Within A Bounding Box For A Specific Massing
def bounding_box_df(focus_lat, focus_long, pc_df, distance_):

    # Find MIN/MAX Lat/Long
    lat_range = []
    long_range = []

    bearing = [45, 225]
    for b in bearing:
        origin = geopy.Point(focus_lat, focus_long)
        destination = VincentyDistance(kilometers= distance_).destination(origin, b)
        lat_range.append(destination.latitude)
        long_range.append(destination.longitude)

    # Return A Version Of PC_Location_DF, That Extends Only To Identified Range
    pc_loc_long = pc_df[pc_df['Longitude'].between(min(long_range), max(long_range), inclusive=True)]
    pc_loc_ = pc_loc_long[pc_loc_long['Latitude'].between(min(lat_range), max(lat_range), inclusive=True)]
    return pc_loc_


# This Function Will Find The Closest Postal Code To A Centroid, And Return A List That Matches The Index Of The Centroid File
def find_closest_pc(centroid_df, pc_df, num):

    # Data To Be Collected
    distance_list = []

    # Needed Hyperparametres
    centroid_df_len = len(centroid_df)
    counter_x = 1

    initial_min_distance = 1
    min_distance = initial_min_distance
    initial_distance = min_distance / (math.cos(45)) # Related To The Bearing! [45, 225]
    distance_km = initial_distance

    for index, row_c in centroid_df.iterrows():
        centroid_location = geopy.Point(row_c["Latitude"], row_c["Longitude"])

        # Keep Trying Until A Good Distance Value Is Found & Utilized
        while True:
            try:
                # Find Focus Values & Add Index As A Column
                focus_df = bounding_box_df(row_c["Latitude"], row_c["Longitude"], pc_df, distance_km)

                # Find Closest Postal Code To Focus Centroid
                focus_df["D_To_C"] = focus_df.apply(lambda row: geodesic(centroid_location, geopy.Point(row["Latitude"], row["Longitude"])), axis=1)
                val_list = focus_df["D_To_C"].tolist()

                # Find Min Distance
                place_holder = str(min(val_list))
                place_holder = place_holder.split(" ")
                min_distance_value = float(place_holder[0])

                # To Solve Bounding Box Issue Only Take Answers That Are Smaller Than The Min Distance
                if min_distance_value > min_distance:
                    raise ValueError
                else:
                    pass

                # If Everything Checks Out Break This While Loop
                break

            # If A Value Error Is Detected Iteratively Increase Distance By 1 KM Until Code Works
            except ValueError:
                distance_km += 1.5
                min_distance += 1.5

        # Reset The Value Of distance_km
        distance_km = initial_distance
        min_distance = initial_min_distance

        # Append The Needed Information
        distance_list.append(min_distance_value)

        # Monitor Progress
        if (counter_x % 1000 == 0) or (counter_x == centroid_df_len):
            print("Worker: " + str(num) + ", Progress: " + str(counter_x) + "/" + str(centroid_df_len))
        else:
            pass

        # Del Column Just Created
        focus_df.drop(["D_To_C"], axis=1)

        # Add To Counter
        counter_x += 1

    centroid_df["Distances"] = distance_list

    # Have Workers Add To One File, Writing To Multiple CSVs Is Poor Programming, Return DF To Queue
    centroid_df.to_csv(r"C:\Users\renac\Documents\Data\Brampton_Massing\Raw_Data\Data\DF_" + str(num) + ".csv", index=False)
