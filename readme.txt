# enaCLI

## Introduction
ENA-CLI is a command-line tool designed to facilitate the validation and submission of data to the European Nucleotide Archive (ENA). This tool streamlines the process of preparing and uploading data files, ensuring they meet ENA's submission requirements.

## Installation 
```
pip install enaCLI
```

## [templates](https://github.com/KhadimGueyeKGY/ena-CLI/blob/master/templates/templates.xlsx) or [templates_all](https://github.com/KhadimGueyeKGY/ena-CLI/blob/master/templates/templates_all.xlsx)

## [Test Data](https://github.com/KhadimGueyeKGY/ena-CLI/tree/master/test_data)

## File Upload Reminder
Before using the enaCLI for other type of analysis submission (5), ensure you have uploaded your files to ENA using the Webin file uploader. Detailed instructions on how to upload files can be found [here](https://ena-docs.readthedocs.io/en/latest/submit/fileprep/upload.html#uploading-files-to-ena).

## [Doker image](https://hub.docker.com/r/khadimgueyekgy1/ena-cli)

## Usage

### 1. Project Submission

#### Usage
```
enaCLI project -h
```

#### Example
```
enaCLI project -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -t
```

#### Options
- `-u`: Webin submission account
- `-p`: Password for the submission account
- `-m`: Manifest file (template: templates/templates.xlsx)
- `-t`: Use Webin test service (optional)

### 2. Sample Submission

#### Usage
```
enaCLI sample -h
```

#### Example
```
enaCLI sample -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -t
```

#### Options
- `-u`: Webin submission account
- `-p`: Password for the submission account
- `-m`: Manifest file (template: templates/templates.xlsx)
- `-t`: Use Webin test service (optional)

### 3. Run Submission

#### Usage
```
enaCLI run -h
```

#### Example
```
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
```
enaCLI genome -h
```

#### Example
```
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

The `targeted` command facilitates the submission of targeted sequences to the public repository ENA (European Nucleotide Archive). It requires the following mandatory arguments:

- `-u`, `--username`: Webin submission account (e.g., Webin-XXX).
- `-p`, `--password`: Password for the submission account.
- `-m`, `--manifestFile`: Path to the manifest file specifying the details of the submission. The manifest file should follow the template provided in `templates/templates.xlsx`.
- `-i`, `--inputDir`: Path to the input directory containing the files declared in the manifest file.

Additionally, the following optional arguments can be provided:
- `-C`, `--centerName`: The center name of the submitter (mandatory for broker accounts).
- `-t`, `--test`: Use Webin test service instead of the production service. Please note that the Webin upload area is shared between test and production services, and that test submission files will not be archived.

### Usage Example:

```
enaCLI targeted -u Webin-XXXX -p 'XXXXXX' -m templates/templates.xlsx -i test_data/targeted -t
```


### 6. Other Submission

#### Usage
```
enaCLI other -h
```

#### Example
```
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

### 7. enaCLI all (the 🪄 option)  

#### Description
The `all` command combines all submissions (projects, samples, runs, genome assemblies, targets, and other analysis objects) into a single command line. This aims to streamline submission to ENA. However, please note the following before running the package:

1. Submit all associated data for other analysis types (different to genome or transcriptome) via Webin file uploader or other tools. More information is available [here](https://ena-docs.readthedocs.io/en/latest/submit/fileprep/upload.html#using-webin-file-uploader).
2. Remove all lines or prepend '#' to each line if they are already submitted or you do not wish to submit them.
3. You can reference projects, samples, or runs using their aliases or accession numbers. Please add the prefix 'webin-reads-' if you want to use the alias with a run. For example, if you set alias=run_alias_1 during your run submission, then to refer to this submission, you would use 'webin-reads-run_alias_1'.
4. Ensure all data is placed in a single folder for the 'inputDir' option.
5. Complete the template while adhering to its structure - an example template is available [here](https://github.com/KhadimGueyeKGY/ena-CLI/blob/master/templates/templates_all.xlsx).

#### Help
```
enaCLI all -h
```

#### Example
```
enaCLI all -u webin-XXXX -p 'XXXXXX' -m templates/templates_all.xlsx -i test_data/all/ -c genome -a AMR_ANTIBIOGRAM -t
```

#### Options 
- `-u`: Webin submission account: Indicates the Webin submission account.
- `-p`: Password: Indicates the password for the Webin submission account.
- `-m`: Manifest file: Specifies the path to the manifest file.
- `-i`: Input directory for all files declared in the manifest file
- `-a`: Analysis type: Specifies the type of analysis provided in the XML.
- `-c`: Assembly submission type: Specifies the type of assembly submission.
- `-C`: Center name: Specifies the center name of the submitter.
- `-t`: Test submission: Submits the data as a test (optional).


## Contact Information
For any errors or assistance, please contact the [ENA helpdesk](https://www.ebi.ac.uk/ena/browser/support).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

