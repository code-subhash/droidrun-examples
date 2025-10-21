#!/usr/bin/env python3
"""
Utility functions for LeadSpot.

This module provides helper functions for data manipulation,
particularly for converting between JSON and CSV formats
and appending data to existing CSV files.
"""
import os
import csv
import json


def append_to_csv(csv_file, data_dict, header_fields=None):
    """
    Append a dictionary of data to a CSV file.
    Creates a new file with headers if it doesn't exist.

    Args:
        csv_file: Path to the CSV file
        data_dict: Dictionary of data to append
        header_fields: List of field names to use as headers (optional)
    """
    # Determine if file exists to know if we need to write headers
    file_exists = os.path.isfile(csv_file)

    # Make sure directory exists
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    # Use provided header fields or keys from data_dict
    fieldnames = header_fields if header_fields else list(data_dict.keys())

    with open(csv_file, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header if the file doesn't exist
        if not file_exists:
            writer.writeheader()

        # Write the data row
        writer.writerow(data_dict)

    return True


def json_to_csv(json_file, csv_file, field_mappings=None):
    """
    Convert a JSON file to a CSV file.

    Args:
        json_file: Path to the JSON file
        csv_file: Path to the CSV file to create
        field_mappings: Dictionary mapping JSON fields to CSV fields (optional)
    """
    # Load JSON data
    with open(json_file, "r") as f:
        json_data = json.load(f)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    # Determine fields to export
    if field_mappings:
        fieldnames = list(field_mappings.values())
    else:
        # Assume first item has all fields
        if isinstance(json_data, list) and json_data:
            fieldnames = list(json_data[0].keys())
        elif isinstance(json_data, dict):
            fieldnames = list(json_data.keys())
        else:
            return False

    # Write to CSV
    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Handle different JSON structures
        if isinstance(json_data, list):
            for item in json_data:
                if field_mappings:
                    row = {
                        csv_field: item.get(json_field, "")
                        for json_field, csv_field in field_mappings.items()
                    }
                else:
                    row = item
                writer.writerow(row)
        elif isinstance(json_data, dict):
            if field_mappings:
                row = {
                    csv_field: json_data.get(json_field, "")
                    for json_field, csv_field in field_mappings.items()
                }
            else:
                row = json_data
            writer.writerow(row)

    return True
