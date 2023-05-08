from ..options.session import Session
import sys
import argparse

def _args():
    
    
    parser = argparse.ArgumentParser()
    
    # Seletor de usuário
    
    parser.add_argument("-u", "--kr_usr", required=True)
    
    
    # Seletor de nome da credencial
    
    parser.add_argument("-a", "--kr_addr", required=False)
    
    
    # Seletor de caminho do chromedriver
    
    parser.add_argument("-c", "--driver_path", required=False)
    
    
    # Seletor de caminho de download
    
    parser.add_argument("-d", "--download_path", required=False)
    
    
    # Seletor de ferramenta
    
    subparsers = parser.add_subparsers(dest="tool")
    
    
    # Ferramenta get_report
    
    get_report = subparsers.add_parser("get_report")
    
    
    # Argumento report
    
    get_report.add_argument("-r", "--report", required=True)
    
    
    # Argumentos parseados
    args = parser.parse_args(sys.argv[1:])
    
    
    parsed_args = vars(args)
    
    
    #dels
    del parser
    del subparsers
    del get_report
    del args
    
    
    return parsed_args


    
def cli():
    
    
    
    method_args = ('report')

    
    args = _args()
    
    tool = args.pop('tool')
    
    print(tool)
    
    session_args = {k: v for k, v in args.items() if k not in method_args and v is not None}
    method_args = {k: v for k, v in args.items() if k in method_args and v is not None}
    
    print(session_args)
    print(method_args)
    
    session = Session(**session_args)
    
    if tool == 'get_report':
    
        return session.get_report(**method_args)
    
    
    
    print(session_args)
    return

if __name__ == "__main__":
    cli()
    
    
