import argparse
import os , sys
import pandas as pd

from .packages.XMLGenerator import XML_generator
from .packages.submission import submission
from .packages.antibiogram import Validation
from .packages.webin import webin
from .others.XMLGenerator import XMLGenerator

# color https://gist.github.com/Prakasaka/219fe5695beeb4d6311583e79933a009

# run 
# https://github.com/enasequence/webin-cli/releases/latest 
import pkg_resources

# Get the path to the webin-cli-7.0.1.jar file
webin_cli = pkg_resources.resource_filename('enaCLI.packages', 'webin-cli-7.3.1.jar')

#webin_cli = '.packages/webin-cli-7.0.1.jar'
version = '1.0.8'


def get_args(): # https://docs.python.org/3/library/argparse.html
    epilog = ("""
            \033[93mNote:
            (1) \033[0mPlease register your project and sample object before registering the antibiogram. 
            Here is the link for more information: \033[94mhttps://ena-docs.readthedocs.io/en/latest/\033[0m.
            \033[93m(2) \033[0mPlease make sure to provide the title and description using single quotes if they contain spaces or special characters. 
            For any error or assistance please contact the ENA helpdesk: \033[94mhttps://www.ebi.ac.uk/ena/browser/support \033[93m(3) Tempalte: \033[94mhttps://github.com/KhadimGueyeKGY/ena-CLI/blob/master/templates/templates.xlsx\033[0m
        """) 
    parser = argparse.ArgumentParser(description='\033[93mThis script facilitates the submission of projects, samples, runs, assemblies, and other analyses to the public repository ENA (European Nucleotide Archive). It also assists in validating AMR (Antimicrobial Resistance) antibiograms before submission.\033[0m'
                                     ,epilog=epilog)
    
    # Create subparsers
    subparsers = parser.add_subparsers(title='\033[93mSubcommands\033[0m', dest='subcommand')
    
    # 1. Project submission
    project = subparsers.add_parser('project', help='Register a Study (Project)',epilog=epilog)
    
    #### Required arguments
    mandatory_p = project.add_argument_group('\033[93mMandatory arguments\033[0m')
    mandatory_p.add_argument('-u', '--username', type=str, help='Webin submission account (e.g., Webin-XXX)', required=True)
    mandatory_p.add_argument('-p', '--password', type=str, help='Password for the submission account', required=True)
    mandatory_p.add_argument('-m', '--manifestFile', type=str, help='Manifest file (template: templates/templates.xlsx)', required=True)

    ##### Optional arguments
    optional_p = project.add_argument_group('\033[93mOptional arguments\033[0m')
    optional_p.add_argument('-C', '--centerName', type=str, help=' the center name of the submitter (mandatory for broker accounts).')
    optional_p.add_argument('-t', '--test', action='store_true', help='use Webin test service instead of the production service. Please note that the Webin upload area is shared between test and production services, and that test submission files will not be archived. (Optional)')
    
    
    # 2. Sample submission
    sample = subparsers.add_parser('sample', help='Register samples',epilog=epilog)
    #### Required arguments
    mandatory_s = sample.add_argument_group('\033[93mMandatory arguments\033[0m')
    mandatory_s.add_argument('-u', '--username', type=str, help='Webin submission account (e.g., Webin-XXX)', required=True)
    mandatory_s.add_argument('-p', '--password', type=str, help='Password for the submission account', required=True)
    mandatory_s.add_argument('-m', '--manifestFile', type=str, help='Manifest file (template: templates/templates.xlsx) - Sample manifest file (template on: \033[94mhttps://www.ebi.ac.uk/ena/browser/checklist\033[0m)', required=True)

    #### Optional arguments
    optional_s = sample.add_argument_group('\033[93mOptional arguments\033[0m')
    optional_s.add_argument('-C', '--centerName', type=str, help=' the center name of the submitter (mandatory for broker accounts).')
    optional_s.add_argument('-t', '--test', action='store_true', help='use Webin test service instead of the production service. Please note that the Webin upload area is shared between test and production services, and that test submission files will not be archived. (Optional)')

    # 3. run submission
    run = subparsers.add_parser('run', help='Register run',epilog=epilog)
    #### Required arguments
    mandatory_r = run.add_argument_group('\033[93mMandatory arguments\033[0m')
    mandatory_r.add_argument('-u', '--username', type=str, help='Webin submission account (e.g., Webin-XXX)', required=True)
    mandatory_r.add_argument('-p', '--password', type=str, help='Password for the submission account', required=True)
    mandatory_r.add_argument('-m', '--manifestFile', type=str, help='Manifest file (template: templates/templates.xlsx)', required=True)
    mandatory_r.add_argument('-i', '--inputDir', type=str, help=' input directory for files declared in manifest file', required=True)
    

    #### Optional arguments
    optional_r = run.add_argument_group('\033[93mOptional arguments\033[0m')
    optional_r.add_argument('-C', '--centerName', type=str, help=' the center name of the submitter (mandatory for broker accounts).')
    optional_r.add_argument('-t', '--test', action='store_true', help='use Webin test service instead of the production service. Please note that the Webin upload area is shared between test and production services, and that test submission files will not be archived. (Optional)')
    
    # 4. Genome Assemblies 
    Genome = subparsers.add_parser('genome', help='Submitting Genome Assemblies of Individuals or Cultured Isolates - Metagenome Assemblies - Environmental Single-Cell Amplified Genomes - Transcriptome Assemblies - Metatranscriptome Assemblies',epilog=epilog)
    #### Required arguments
    mandatory_g = Genome.add_argument_group('\033[93mMandatory arguments\033[0m')
    mandatory_g.add_argument('-u', '--username', type=str, help='Webin submission account (e.g., Webin-XXX)', required=True)
    mandatory_g.add_argument('-p', '--password', type=str, help='Password for the submission account', required=True)
    mandatory_g.add_argument('-m', '--manifestFile', type=str, help='Manifest file (template: templates/templates.xlsx)', required=True)
    mandatory_g.add_argument('-i', '--inputDir', type=str, help=' input directory for files declared in manifest file', required=True)
    mandatory_g.add_argument('-c', '--context', choices=['genome','transcriptome'], help=' the assembly submission type', required=True)
    

    #### Optional arguments
    optional_g = Genome.add_argument_group('\033[93mOptional arguments\033[0m')
    optional_g.add_argument('-C', '--centerName', type=str, help=' the center name of the submitter (mandatory for broker accounts).')
    optional_g.add_argument('-t', '--test', action='store_true', help='use Webin test service instead of the production service. Please note that the Webin upload area is shared between test and production services, and that test submission files will not be archived. (Optional)')
    
    # 5. Submit Targeted Sequences
    Targeted = subparsers.add_parser('targeted', help='Submit Targeted Sequences',epilog=epilog)
    
    #### Required arguments
    mandatory_t = Targeted.add_argument_group('\033[93mMandatory arguments\033[0m')
    mandatory_t.add_argument('-u', '--username', type=str, help='Webin submission account (e.g., Webin-XXX)', required=True)
    mandatory_t.add_argument('-p', '--password', type=str, help='Password for the submission account', required=True)
    mandatory_t.add_argument('-m', '--manifestFile', type=str, help='Manifest file (template: templates/templates.xlsx)', required=True)
    mandatory_t.add_argument('-i', '--inputDir', type=str, help=' input directory for files declared in manifest file', required=True)
    

    #### Optional arguments
    optional_t = Targeted.add_argument_group('\033[93mOptional arguments\033[0m')
    optional_t.add_argument('-C', '--centerName', type=str, help=' the center name of the submitter (mandatory for broker accounts).')
    optional_t.add_argument('-t', '--test', action='store_true', help='use Webin test service instead of the production service. Please note that the Webin upload area is shared between test and production services, and that test submission files will not be archived. (Optional)')

    # 6. Other Analyses
    # 7. antibiograms submission
    Other = subparsers.add_parser('other', help='Submit Other Analyses',epilog=epilog)
    
    #### Required arguments
    mandatory_o = Other.add_argument_group('\033[93mMandatory arguments\033[0m')
    mandatory_o.add_argument('-u', '--username', type=str, help='Webin submission account (e.g., Webin-XXX)', required=True)
    mandatory_o.add_argument('-p', '--password', type=str, help='Password for the submission account', required=True)
    mandatory_o.add_argument('-m', '--manifestFile', type=str, help='Manifest file (template: templates/templates.xlsx)', required=True)
    mandatory_o.add_argument('-a', '--analysisType', choices=['GENOME_MAP','REFERENCE_ALIGNMENT','SEQUENCE_ANNOTATION','ASSEMBLY_GRAPH','PROCESSED_READ','PATHOGEN_ANALYSIS','AMR_ANTIBIOGRAM','COVID-19_FILTERED_VCF','COVID-19_CONSENSUS','PHYLOGENY_ANALYSIS'], help='The analysis type is provided in the XML itself. It must be one of the following', required=True)
    mandatory_o.add_argument('-i', '--inputDir', type=str, help=' input directory for files declared in manifest file', required=True)


    #### Optional arguments
    optional_o = Other.add_argument_group('\033[93mOptional arguments\033[0m')
    optional_o.add_argument('-C', '--centerName', type=str, help=' the center name of the submitter (mandatory for broker accounts).')
    optional_o.add_argument('-t', '--test', action='store_true', help='use Webin test service instead of the production service. Please note that the Webin upload area is shared between test and production services, and that test submission files will not be archived. (Optional)')

    # 8. All arguments
    all_args = subparsers.add_parser('all', help='Submit all types of data at once' ,epilog=epilog)
    
    #### Required arguments
    mandatory_a = all_args.add_argument_group('\033[93mMandatory arguments\033[0m')
    mandatory_a.add_argument('-u', '--username', type=str, help='Webin submission account (e.g., Webin-XXX)', required=True)
    mandatory_a.add_argument('-p', '--password', type=str, help='Password for the submission account', required=True)
    mandatory_a.add_argument('-m', '--manifestFile', type=str, help='Manifest file (template: templates/templates.xlsx)', required=True)

    #### Optional arguments
    optional_a = all_args.add_argument_group('\033[93mOptional arguments\033[0m')
    optional_a.add_argument('-i', '--inputDir', type=str, help='Input directory for files declared in manifest file')
    optional_a.add_argument('-C', '--centerName', type=str, help='The center name of the submitter (mandatory for broker accounts)')
    optional_a.add_argument('-c', '--context', choices=['genome','transcriptome'], help=' the assembly submission type')
    optional_a.add_argument('-a', '--analysisType', choices=['GENOME_MAP','REFERENCE_ALIGNMENT','SEQUENCE_ANNOTATION','ASSEMBLY_GRAPH','PROCESSED_READ','PATHOGEN_ANALYSIS','AMR_ANTIBIOGRAM','COVID-19_FILTERED_VCF','COVID-19_CONSENSUS','PHYLOGENY_ANALYSIS'], help='The analysis type is provided in the XML itself. It must be one of the following (other submission type)')
    optional_a.add_argument('-t', '--test', action='store_true', help='Use Webin test service instead of the production service. Please note that the Webin upload area is shared between test and production services, and that test submission files will not be archived.')

    #args = parser.parse_args()
    # Add version argument
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {version}')

    return parser

def sub_project (result_directory,args):
    try:
        manifestFile = pd.read_excel(args.manifestFile, sheet_name="project")
        
    except Exception as e:
        print(f"\033[91mError: reading file {args.manifestFile}.\033[0m\nException: {e}")
        sys.exit() 
    # Create the second ACTION element with HOLD
    head = [i for i in manifestFile]
    a = 0 
    for i in range(len(manifestFile[head[0]])):
        if '#' not in str(manifestFile[head[0]][i]):
            if not pd.isna(manifestFile[head[0]][i]):
                a = 1
                break 
    if a == 1 :
        print ('\033[93m\n\n------------------------ [ PROJECT Submission ] ------------------------ \n\n\033[0m')
        submission_file = XML_generator.project_submission_xml(result_directory,args)
        submission_set_file = XML_generator.generate_project_xml (result_directory, args)
        submission.submit_to_ENA(submission_file , submission_set_file, args, 'PROJECT')
        print ('\033[92m\n\n------------------------ [ PROJECT Submission - Done ] ------------------------ \n\n\033[0m')

def sub_sample (result_directory,args):
    try:
        # Read the manifest file into a pandas DataFrame
        manifestFile = pd.read_excel(args.manifestFile, sheet_name="sample",header=1)
        
    except Exception as e:
        print(f"\033[91mError: Failed to read the manifest file {args.manifestFile}.\033[0m\nException: {e}")
        sys.exit() 
    # Create the second ACTION element with HOLD
    head = [i for i in manifestFile]
    a = 0 
    for i in range(len(manifestFile[head[0]])):
        if '#' not in str(manifestFile[head[0]][i]):
            if not pd.isna(manifestFile[head[0]][i]):
                a = 1
                break 
    if a == 1 :
        print ('\033[93m\n\n------------------------ [ SAMPLE Submission ] ------------------------ \n\n\033[0m')
        submission_file = XML_generator.build_submission_xml(result_directory)
        submission_set_file = XML_generator.generate_sample_xml(result_directory,args)
        submission.submit_to_ENA(submission_file , submission_set_file, args , 'SAMPLE')
        print ('\033[92m\n\n------------------------ [ SAMPLE Submission - Done ] ------------------------ \n\n\033[0m')

def sub_run (result_directory, args  , webin_cli):
    try:
        manifestFile = pd.read_excel(args.manifestFile, sheet_name="run",header = 1)
    except Exception as e:
        print(f"\033[91mError: reading file {args.manifestFile}.\033[0m\nException: {e}")
        sys.exit()
    # Create the second ACTION element with HOLD
    head = [i for i in manifestFile]
    a = 0 
    for i in range(len(manifestFile[head[0]])):
        if '#' not in str(manifestFile[head[0]][i]):
            if not pd.isna(manifestFile[head[0]][i]):
                a = 1
                break 
    if a == 1 :
        print ('\033[93m\n\n------------------------ [ RUN Submission ] ------------------------ \n\n\033[0m')
        webin.run_submission(result_directory, args  , webin_cli)
        print ('\033[92m\n\n------------------------ [ RUN Submission - Done ] ------------------------ \n\n\033[0m')
        
def sub_genome (result_directory, args  , webin_cli):
    try:
        manifestFile = pd.read_excel(args.manifestFile, sheet_name="genome")
        
    except Exception as e:
        print(f"\033[91mError: reading file {args.manifestFile}.\033[0m\nException: {e}")
        sys.exit() 
    # Create the second ACTION element with HOLD
    head = [i for i in manifestFile]
    a = 0 
    for i in range(len(manifestFile[head[0]])):
        if '#' not in str(manifestFile[head[0]][i]):
            if not pd.isna(manifestFile[head[0]][i]):
                a = 1
                break 
    if a == 1 :
        print ('\033[93m\n\n------------------------ [ GENOME Submission ] ------------------------ \n\n\033[0m')
        webin.genome_submission(result_directory, args  , webin_cli)
        print ('\033[92m\n\n------------------------ [ GENOME Submission - Done ] ------------------------ \n\n\033[0m')

def sub_targeted (result_directory, args  , webin_cli) :
    try:
        manifestFile = pd.read_excel(args.manifestFile, sheet_name="targeted")
        
    except Exception as e:
        print(f"\033[91mError: reading file {args.manifestFile}.\033[0m\nException: {e}")
        sys.exit()
    # Create the second ACTION element with HOLD
    head = [i for i in manifestFile]
    a = 0 
    for i in range(len(manifestFile[head[0]])):
        if '#' not in str(manifestFile[head[0]][i]):
            if not pd.isna(manifestFile[head[0]][i]):
                a = 1
                break 
    if a == 1 :
        print ('\033[93m\n\n------------------------ [ TARGETED Submission ] ------------------------ \n\n\033[0m')
        webin.targeted_submission(result_directory, args  , webin_cli)
        print ('\033[92m\n\n------------------------ [ TARGETED Submission - Done ] ------------------------ \n\n\033[0m')

def sub_other (result_directory, args):
    try:
        #antibiogram_file = pd.read_csv (args.filename, sep='\t')
        manifestFile = pd.read_excel(args.manifestFile, sheet_name="Other Analyses", header = 1)
        
    except Exception as e:
        print(f"\033[91mError: reading file {args.manifestFile}.\033[0m\nException: {e}")
        sys.exit()
    # Create the second ACTION element with HOLD
    head = [i for i in manifestFile]
    a = 0 
    for i in range(len(manifestFile[head[0]])):
        if '#' not in str(manifestFile[head[0]][i]):
            if not pd.isna(manifestFile[head[0]][i]):
                a = 1
                break 
    if a == 1 :
        print ('\033[93m\n\n------------------------ [ OTHER ANALYSIS Submission ] ------------------------ \n\n\033[0m')
        if args.analysisType == 'AMR_ANTIBIOGRAM' :
            print (f'\033[93m\n\n------------------------ [ AMR_ANTIBIOGRAM Validation ] ------------------------ \n\n\033[0m')
            for i in range(len(manifestFile[head[0]])):
                if '#' not in str(manifestFile[head[0]][i]):
                    file_path = os.path.join(args.inputDir, manifestFile['FILES'][i] )
                    
                    print (f'\033[93m\n\n------------------------ [ AMR_ANTIBIOGRAM Validation of {file_path} ] ------------------------ \n\n\033[0m')
                    Validation.validate_csv(file_path)
                    
            print ('\033[93m\n\n------------------------ [ AMR_ANTIBIOGRAM Validation - Done ] ------------------------ \n\n\033[0m')

        XMLGenerator.filesubmission(args)
        submission_file = XML_generator.build_submission_xml(args.inputDir)
        submission_set_file= XMLGenerator.other_submission(result_directory, args )
        submission.submit_to_ENA(submission_file , submission_set_file, args , 'ANALYSIS')
        print ('\033[92m\n\n------------------------ [ OTHER ANALYSIS Submission - Done ] ------------------------ \n\n\033[0m')
    
def process():
    if len(sys.argv) <= 1: 
        print(get_args().print_help())
        sys.exit()
    args = get_args().parse_args()

    result_directory = 'results'  
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)
    result_directory = os.path.abspath(result_directory)

    if args.subcommand == 'project':
        sub_project (result_directory,args)

    elif args.subcommand == 'sample':
        sub_sample (result_directory,args)

    elif args.subcommand == 'run':
        sub_run (result_directory, args  , webin_cli)

    elif args.subcommand == 'genome':
        sub_genome (result_directory, args  , webin_cli)
        
    elif args.subcommand == 'targeted':
        sub_targeted (result_directory, args  , webin_cli)    

    elif args.subcommand == 'other':
        sub_other (result_directory, args)
        
    elif args.subcommand == 'all':
        sub_project (result_directory,args)
        sub_sample (result_directory,args)
        sub_run (result_directory, args  , webin_cli)
        sub_genome (result_directory, args  , webin_cli)
        sub_targeted (result_directory, args  , webin_cli)
        sub_other (result_directory, args)
        
        

    print(f"\033[93m\n\n-------[ done ]-------\033[0m")
    print(f"\033[94mFor any error or assistance please contact the ENA helpdesk: https://www.ebi.ac.uk/ena/browser/support \n\n\033[0m")


#if __name__ == '__main__':
#   process()
    