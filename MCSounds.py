from soundScrapers import scrapeSound
import urlCheckers, sys, argparse, os
def readNames(names, dir = ''):
    for name in names:
        URL = urlCheckers.buildURL(name)
        if urlCheckers.checkURL(URL):
            scrapeSound(URL, dir = dir)
            
def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")
      
def main():
    parser = argparse.ArgumentParser(description='Grab Minecraft Mob sound information from the Minecraft wiki')
    parser.add_argument('names', help='A single or multiple names of valid Minecraft Mobs', action='extend', nargs='*', type=str)
    parser.add_argument('-l', help='A file containing a list of valid Minecraft Mobs', type=argparse.FileType('r'))
    parser.add_argument('-w', help='Folder to write the sound information of the given Minecraft Mobs to.', type=dir_path)
    args = vars(parser.parse_args())

    if args['l'] is not None:
        mobs = [mob.strip() for mob in args['l'].readlines()]
        readNames(mobs, dir = args['w'])
    else:
        readNames(args['names'], dir = args['w'])
        
main()