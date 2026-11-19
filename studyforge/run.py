"""Run: python -m studyforge.run"""
import argparse
from .server import run

def main():
    parser=argparse.ArgumentParser(description='Run the local StudyForge dashboard')
    parser.add_argument('--port',type=int,default=8765)
    args=parser.parse_args()
    if not 1024 <= args.port <= 65535:parser.error('Port must be 1024–65535')
    run(port=args.port)

if __name__=='__main__':main()
