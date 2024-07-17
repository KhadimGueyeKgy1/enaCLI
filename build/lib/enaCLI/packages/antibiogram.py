import csv
import requests
import sys
import pkg_resources
import pandas as pd

class Validation:
    antibiotic_file = pkg_resources.resource_filename('enaCLI.packages', 'antibiotics.txt')
    laboratory_typing_methods = ['BROTH DILUTION', 'MICROBROTH DILUTION', 'AGAR DILUTION', 'DISC-DIFFUSION', 'NEO-SENSITABS', 'ETEST']
    dilution_methods = ['BROTH DILUTION', 'MICROBROTH DILUTION', 'AGAR DILUTION', 'ETEST']
    diffusion_methods = ['DISC-DIFFUSION', 'NEO-SENSITABS']

    def validate_csv(file):
        try: 
            reader = pd.read_csv (file, sep='\t')
        except Exception as e:
            print(f"\033[91mError: reading file {file}.\033[0m\nException: {e}")
            sys.exit()
        for line_number, row in reader.iterrows():
            Validation.val_biosample_id(row['bioSample_ID'], line_number)
            Validation.val_species(row['species'], line_number)
            Validation.val_antibiotic_name(row['antibiotic_name'], line_number)
            Validation.val_ast_standard(row['ast_standard'], line_number)
            Validation.val_breakpoint_version(row['breakpoint_version'], line_number)
            Validation.val_laboratory_typing_method(row['laboratory_typing_method'], line_number)
            Validation.val_measurement(row['measurement'], row['laboratory_typing_method'], line_number)
            Validation.val_measurement_units(row['measurement_units'], row['laboratory_typing_method'], line_number)
            Validation.val_measurement_sign(row['measurement_sign'], line_number)
            Validation.val_resistance_phenotype(row['resistance_phenotype'], line_number)
            Validation.val_platform(row['platform'], line_number)

    def val_biosample_id( biosample_id, line_number):
        if 'SAM' not in biosample_id and 'ERS' not in biosample_id:
            print(f"\033[91mERROR: {biosample_id} is not a valid biosample accession in line number {line_number+1}. (e.g SAMXXXX or ERSXXX) \033[0m")
            sys.exit()

    def val_species(species, line_number):
        sp = str(species).replace(" ", "%20")
        scientific_name_url = f"https://www.ebi.ac.uk/ena/taxonomy/rest/scientific-name/{sp}"
        any_name_url = f"https://www.ebi.ac.uk/ena/taxonomy/rest/any-name/{sp}"
        
        try:
            # Check scientific name URL
            resp = requests.get(scientific_name_url)
            if resp.status_code == 200:
                data = resp.json()
                if data and data[0]['scientificName'].lower() == species.lower():
                    return
                else:
                    print(f"\033[91mERROR: The scientific name '{species}' does not match the taxonomy database entry in line number {line_number + 1}.\033[0m")
                    sys.exit()
            else:
                # Check any name URL if scientific name URL fails
                resp = requests.get(any_name_url)
                if resp.status_code == 200:
                    data = resp.json()
                    print(f"\033[91mERROR: The scientific name '{species}' does not exist in taxonomy database in line number {line_number + 1}.\033[0m")
                    print(f"\033[93mSome close matches scientific names are:\n{', '.join([item['scientificName'] for item in data])}\033[0m")
                else:
                    print(f"\033[91mERROR: The species '{species}' does not exist in taxonomy database in line number {line_number + 1}.\033[0m")
                sys.exit()
        except Exception as e:
            print(f"\033[91mERROR: Failed to validate species '{species}' in line number {line_number + 1}.\033[0m\nException: {e}")
            sys.exit()

    def val_antibiotic_name( antibiotic_name, line_number):
        with open(Validation.antibiotic_file) as f:
            antibiotics = f.read().upper().splitlines()
        if str(antibiotic_name).upper() not in antibiotics:
            print(f"\033[91mERROR: '{antibiotic_name}' is not a valid antibiotic name in line number {line_number+1}.\nValid ones are {antibiotics}\033[0m")
            sys.exit()

    def val_ast_standard( ast_standard, line_number):
        accepted_ast_standards = ['CLSI', 'EUCAST', 'CA-SFM', 'BSAC', 'DIN', 'SIR', 'WRG']
        if str(ast_standard).upper() not in accepted_ast_standards:
            print(f"\033[91mERROR: {ast_standard} is not a valid ast_standard in line number {line_number+1}.\nValid ones are {accepted_ast_standards}\033[0m")
            sys.exit()

    def val_breakpoint_version( breakpoint_version, line_number):
        pass

    def val_laboratory_typing_method( laboratory_typing_method, line_number):
        if str(laboratory_typing_method).upper() not in Validation.laboratory_typing_methods:
            print(f"\033[91mERROR: {laboratory_typing_method} is not a valid laboratory_typing_method in line number {line_number+1}. \nValid ones are {Validation.laboratory_typing_methods}\033[0m")
            sys.exit()

    def val_measurement( measurement, laboratory_typing_method, line_number):
        if str(measurement).find('-') != -1:
            measurements = str(measurement).split('-')
            for meas in measurements:
                Validation._validate_single_measurement(meas, laboratory_typing_method, line_number)
        else:
            Validation._validate_single_measurement(measurement, laboratory_typing_method, line_number)

    def _validate_single_measurement( measurement, laboratory_typing_method, line_number):
        if str(laboratory_typing_method).upper() in Validation.dilution_methods:
            try:
                if not 0.01 <= float(measurement) <= 2048:
                    print(f"\033[91mERROR: {measurement} is not a valid measurement, accepted one is between 0.01 and 2048 for dilution methods in line number {line_number+1}.\033[0m")
                    sys.exit()
            except:
                print(f"\033[91mERROR: the measurement value format of {measurement} is not correct in line number {line_number+1}.\033[0m")
                sys.exit()
        elif str(laboratory_typing_method).upper() in Validation.diffusion_methods:
            try:
                if not 6 <= float(measurement) <= 99:
                    print(f"\033[91mERROR: {measurement} is not a valid measurement, accepted one is between 6 and 99 for diffusion methods in line number {line_number+1}.\033[0m")
                    sys.exit()
            except:
                print(f"\033[91mERROR: the measurement value format of {measurement} is not correct in line number {line_number+1}.\033[0m")
                sys.exit()
        else:
            print(f"\033[91mERROR: measurement can't be validated as laboratory_typing_method needs to be valid to validate the measurement in line number {line_number+1}.\033[0m")
            sys.exit()

    def val_measurement_units( measurement_units, laboratory_typing_method, line_number):
        if str(laboratory_typing_method).upper() in Validation.dilution_methods:
            if str(measurement_units).lower() != 'mg/l':
                print(f"\033[91mERROR: {measurement_units} is not a valid measurement unit, accepted one is 'mg/L' for dilution methods in line number {line_number+1}.\033[0m")
                sys.exit()
        elif str(laboratory_typing_method).upper() in Validation.diffusion_methods:
            if str(measurement_units).lower() != 'mm':
                print(f"\033[91mERROR: {measurement_units} is not a valid measurement unit, accepted one is 'mm' for diffusion methods in line number {line_number+1}.\033[0m")
                sys.exit()
        else:
            print(f"\033[91mERROR: measurement unit can't be validated as laboratory_typing_method needs to be valid to validate the measurement unit in line number {line_number+1}.\033[0m")
            sys.exit()

    def val_measurement_sign( measurement_sign, line_number):
        accepted_val_measurement_signs = ['>', '<', '=', '<=', '>=']
        if measurement_sign not in accepted_val_measurement_signs:
            print(f"\033[91mERROR: {measurement_sign} is not a valid measurement sign. Valid ones are {accepted_val_measurement_signs} in line number {line_number+1}.\033[0m")
            sys.exit()

    def val_resistance_phenotype( resistance_phenotype, line_number):
        accepted_resistance_phenotype = ['intermediate', 'susceptible', 'resistant', 'non-susceptible', 'not-defined']
        if str(resistance_phenotype).lower() not in accepted_resistance_phenotype:
            print(f"\033[91mERROR: '{resistance_phenotype}' is not a valid resistance phenotype. \nValid ones are {accepted_resistance_phenotype} in line number {line_number+1}\033[0m")
            sys.exit()

    def val_platform( platform, line_number):
        pass

