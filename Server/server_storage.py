import pickle
from typing import Any

from Server.data_categories import GameDataType as gdt


def store_data(category: gdt, data: Any, debug: bool = False):
    """
    Store data in a pickle file based on the given category.

    :param category: The category name, used as the filename.
    :param data: The data to be stored.
    """
    with open(f"{category}_debug_{debug}.pkl", "wb") as file:
        pickle.dump(data, file)


def retrieve_data(category: gdt, debug: bool = False) -> Any:
    """
    Retrieve data from a pickle file based on the given category.

    :param category: The category name, corresponding to the filename.
    :return: The data retrieved from the file.
    """
    try:
        with open(f"{category}_debug_{debug}.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        print(f"Error: No data found for category '{category}'.")
        return None


if __name__ == '__main__':
    # Example usage
    store_data(gdt.LATEST_ACTIVE_PLAYERS, ["Marijn", "Jeroen", "Salih"])
    store_data(gdt.HIGH_SCORES, [("Marijn", 75), ("Jeroen", 50), ("Salih", 25)])

    # Retrieving the data
    fruits = retrieve_data(gdt.LATEST_ACTIVE_PLAYERS)
    numbers = retrieve_data(gdt.HIGH_SCORES)
