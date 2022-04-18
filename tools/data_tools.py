import os
import pathlib

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def get_data(path: pathlib.WindowsPath) -> pd.DataFrame:
  # comments
  data = pd.DataFrame()
  files = [x for x in path.glob("*") if x.is_file()]
  for file in files:
    content = pd.read_csv(path / file, index_col=0).sort_index()
    content = content.drop_duplicates()
    content = content.applymap(remove_negative)
    if len(data):
      data = pd.merge(data, content, on=["codering","gemeentenaam"], how="inner")
    else:
      data = content

  return data


def remove_negative(cell):
  # comments
  return cell * -1 if isinstance(cell, (int, float)) and cell < 0 else cell


def get_data_for_given_type(column: str, type: str, data) -> pd.DataFrame:
  # comments
  return data.loc[data[column] == type]


def write_data_to_file(path: pathlib.WindowsPath, name: str, data: pd.DataFrame):
  # comments
  if not os.path.exists(path):
    os.mkdir(path)

  data.to_csv(path / name)


def calculate_averages(data: pd.DataFrame) -> pd.DataFrame:
  averages = pd.DataFrame(columns=data.columns)
  for column in data.columns:
    if isinstance(data[column][0], (int, float)):
      averages[column] = [data[column].mean()]
    else:
      averages[column] = [None]

  return averages


def plot_data(x_axis: str, y_axis: str, data: pd.DataFrame, path: pathlib.WindowsPath) -> plt.plot:
  # comments
  data = data.dropna(subset=[x_axis, y_axis])
  data = data.sort_values([x_axis])
  regression, offset = np.polyfit(data[x_axis], data[y_axis], 1)
  plt.plot(data[x_axis], data[y_axis], 'o')
  plt.plot(data[x_axis], regression*data[x_axis] + offset)
  plt.ylabel(y_axis)
  plt.xlabel(x_axis)
  plt.savefig(path / f"{x_axis} vs {y_axis}.png")


def calculate_potential(data: pd.DataFrame, averages: pd.DataFrame, worth: pd.DataFrame) -> pd.DataFrame:
  data["potential"] = None

  for index, row in data.iterrows():
    potential = 1

    for column in data:

      if not isinstance(data.loc[index, column], (int, float)) or np.isnan(data.loc[index, column]):
        continue

      potential += - ((averages[column][0] - data.loc[index, column])/averages[column][0] * worth[column][0])

    data.loc[index, "potential"] = potential

  return data
