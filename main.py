import tools.data_tools as tools
from config import BASE_DIR


if __name__ == '__main__':
    path = BASE_DIR / "data"

    # get data for analysis
    data = tools.get_data(path)

    # get data needed for analysis
    filtered_data = tools.get_data_for_given_type("soort_regio", "Gemeente", data)

    # plot with regression and save plot to output folder
    tools.plot_data("stadsverwarming", "gemiddeld_elektriciteitsverbruik_totaal", data=filtered_data, path=path / "output")

    # write data to file in output folder
    tools.write_data_to_file(path / "output", "name.csv", data)

    # calculated average
    averages = tools.calculate_averages(data)
    tools.write_data_to_file(path / "output", "averages.csv", averages)

    # A "potential" csv file similar to the "averages" file needs to be created manually in the output folder for this part to work.
    # The "potential" values add the importance of the variable to the calculation of the potential profit that can be made in that region.
    # A positive value (like 1) implies a positive relation, a negative "potential" value (-1 for example) implies an inverse relation,
    # while a 0 implies no relation at all between the variable and the profit potential.

    # potential = pd.read_csv(path / "output" / "potential.csv", index_col=0).applymap(lambda x: float(str(x).replace(",", ".")))
    # data_with_potential = tools.calculate_potential(data, averages, potential)
    # tools.write_data_to_file(path / "output", "data_with_potential.csv", data_with_potential)

