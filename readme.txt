# enaCLI

## Introduction
enaCLI is a command-line tool designed to facilitate the validation and submission of data to the European Nucleotide Archive (ENA). This tool streamlines the process of preparing and uploading data files, ensuring they meet ENA's submission requirements.

## Installation 
```bash
sudo apt install lftp
pip install enaCLI
```

## Resources
- [Templates](https://github.com/KhadimGueyeKgy1/enaCLI/blob/main/templates/templates.xlsx)
- [Complete Templates](https://github.com/KhadimGueyeKgy1/enaCLI/blob/main/templates/templates_all.xlsx)
- [Test Data](https://github.com/KhadimGueyeKgy1/enaCLI/tree/main/test_data)
- [Docker Image](https://hub.docker.com/r/khadimgueyekgy1/ena-cli)

## Usage
```bash
enaCLI -h
```

### 1. Project Submission

#### Usage
```bash
enaCLI project -h
```

#### Example
```bash
enaCLI project -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -t
```

#### Options
- `-u`: Webin submission account
- `-p`: Password for the submission account
- `-m`: Manifest file (template: templates/templates.xlsx)
- `-t`: Use Webin test service (optional)

### 2. Sample Submission

#### Usage
```bash
enaCLI sample -h
```

#### Example
```bash
enaCLI sample -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -t
```

#### Options
- `-u`: Webin submission account
- `-p`: Password for the submission account
- `-m`: Manifest file (template: templates/templates.xlsx)
- `-t`: Use Webin test service (optional)

### 3. Run Submission

#### Usage
```bash
enaCLI run -h
```

#### Example
```bash
enaCLI run -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -i test_data/run -t
```

#### Options
- `-u`: Webin submission account
- `-p`: Password for the submission account
- `-m`: Manifest file (template: templates/templates.xlsx)
- `-i`: Input directory for files declared in the manifest file
- `-C`: The center name of the submitter (mandatory for broker accounts)
- `-t`: Use Webin test service (optional)

### 4. Genome Assembly Submissions

#### Usage
```bash
enaCLI genome -h
```

#### Example
```bash
enaCLI genome -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -i test_data/genome -c genome -t
```

#### Options
- `-u`: Webin submission account
- `-p`: Password for the submission account
- `-m`: Manifest file (template: templates/templates.xlsx)
- `-i`: Input directory for files declared in the manifest file
- `-c`: Assembly submission type (choices: genome, transcriptome)
- `-C`: The center name of the submitter (mandatory for broker accounts)
- `-t`: Use Webin test service (optional)

### 5. Targeted Command

The `targeted` command facilitates the submission of targeted sequences to the public repository ENA (European Nucleotide Archive).

#### Usage Example
```bash
enaCLI targeted -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -i test_data/targeted -t
```

#### Options
- `-u`, `--username`: Webin submission account (e.g., Webin-XXX)
- `-p`, `--password`: Password for the submission account
- `-m`, `--manifestFile`: Path to the manifest file specifying the details of the submission. The manifest file should follow the template provided in `templates/templates.xlsx`
- `-i`, `--inputDir`: Path to the input directory containing the files declared in the manifest file
- `-C`, `--centerName`: The center name of the submitter (mandatory for broker accounts)
- `-t`, `--test`: Use Webin test service instead of the production service

### 6. Other Submission

#### Usage
```bash
enaCLI other -h
```

#### Example
```bash
enaCLI other -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -i test_data/other -a AMR_ANTIBIOGRAM -t
```

#### Options
- `-u`: Webin submission account
- `-p`: Password for the submission account
- `-m`: Manifest file (template: templates/templates.xlsx)
- `-i`: Input directory for files declared in the manifest file
- `-a`: Analysis type (choices: GENOME_MAP, REFERENCE_ALIGNMENT, SEQUENCE_ANNOTATION, ASSEMBLY_GRAPH, PROCESSED_READ, PATHOGEN_ANALYSIS, AMR_ANTIBIOGRAM, COVID-19_FILTERED_VCF, COVID-19_CONSENSUS, PHYLOGENY_ANALYSIS)
- `-C`: The center name of the submitter (mandatory for broker accounts)
- `-t`: Use Webin test service (optional)

#### Validating Antimicrobial Resistance (AMR) Data

When submitting AMR data, it is crucial to ensure that each column in your antibiogram files adheres to specific validation rules:

- **bioSample_ID**: Must contain 'SAM' or 'ERS' as part of the identifier.
- **species**: Must be validated against the ENA taxonomy database to ensure correct scientific naming.
- **antibiotic_name**: Must match the list provided in [antibiotics.txt](https://github.com/KhadimGueyeKgy1/enaCLI/blob/main/enaCLI/packages/antibiotics.txt).
- **ast_standard**: Must be one of the accepted standards (e.g., CLSI, EUCAST, CA-SFM, BSAC, DIN, SIR or WRG).
- **breakpoint_version**: Ensures compatibility with the chosen AST standard.
- **laboratory_typing_method**: Must be one of the predefined methods (e.g., BROTH DILUTION, MICROBROTH DILUTION, AGAR DILUTION or DISC-DIFFUSION, NEO-SENSITABS, ETEST).
- **measurement**: Must fall within valid ranges depending on the typing method.
- **measurement_units**: Must be appropriate for the typing method (e.g., 'mg/L' for dilution methods or 'mm' for diffusion methods).
- **measurement_sign**: Must be a valid comparison operator (e.g., >, <, =).
- **resistance_phenotype**: Must be one of the accepted phenotypes (e.g., intermediate, susceptible, resistant, non-susceptible or not-defined).
- **platform**: While not always mandatory, must be consistent with the data submitted.

For each column, the validation ensures that the data complies with ENA standards, preventing errors and ensuring smooth submission.

### 7. enaCLI All (the magic🪄 option)  

#### Description
The `all` command combines all submissions (projects, samples, runs, genome assemblies, targets, and other analysis objects) into a single command line. This aims to streamline submission to ENA.

#### Help
```bash
enaCLI all -h
```

#### Example
```bash
enaCLI all -u webin-XXXX -p 'XXXXXX' -m templates/templates_all.xlsx -i test_data/all/ -c genome -a AMR_ANTIBIOGRAM -t
```

#### Options 
- `-u`: Webin submission account
- `-p`: Password for the submission account
- `-m`: Manifest file
- `-i`: Input directory for all files declared in the manifest file (optional)
- `-a`: Analysis type (optional)
- `-c`: Assembly submission type (optional)
- `-C`: Center name (optional)
- `-t`: Test submission (optional)

## Contact Information
For any errors or assistance, please contact the [ENA helpdesk](https://www.ebi.ac.uk/ena/browser/support).

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
```

This documentation provides clear and concise instructions for installing, using, and troubleshooting the `enaCLI` tool. It also includes specific validation steps for AMR data, ensuring users submit accurate and valid information to the ENA.