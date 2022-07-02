import pandas as pd
import argparse
import numpy as np
from typing import List
from tqdm import tqdm


def missing_elements(data: List):
    return sorted(set(range(1, 801)).difference(data))


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--file', "-f", action='store',
                    help='The file which should be converted', required=True)
parser.add_argument('--output', "-o", action='store',
                    help='The output file name', required=True)

args = parser.parse_args()

data = pd.read_csv(args.file)

# Create new dataframe
columns = ["ImageNumber"]
columns.extend([f"Object Number {i + 1}" for i in range(data["ObjectNumber"].max())])
converted_data = pd.DataFrame(columns=columns)
converted_data["ImageNumber"] = data["ImageNumber"].unique()

for column in tqdm(converted_data.columns):
    if column == "ImageNumber":
        continue

    number = int(column.split(' ')[-1])
    temp = data[data["ObjectNumber"] == number]

    if len(temp) < 800:
        missing_image_ids = missing_elements(temp["ImageNumber"].tolist())
        temp = temp["Intensity_IntegratedIntensity_Fluo4"]
        temp = temp.tolist()

        for missing_image_id in missing_image_ids:
            temp.insert(missing_image_id, np.nan)
        temp = pd.Series(temp)
    else:
        temp = temp["Intensity_IntegratedIntensity_Fluo4"]

    converted_data[column] = temp.values

output_name = args.output if ".csv" in args.output else f"{args.output}.csv"
print(f"Saving file as {output_name}")
converted_data.to_csv(output_name, index=False)

# print(data["ObjectNumber"])
# print(data.head())
