import argparse
import sys

from pylint.lint import Run

parser = argparse.ArgumentParser(description='Make pylint to pass with custom score.')
parser.add_argument('-t', '--targets', nargs='+', dest='targets',
                    help='space separated paths to target modules or packages')
parser.add_argument('-s', '--score', type=float, dest='score',
                    default=7.0, help='float number, the affordable pylint score')
args = parser.parse_args()


def lint(targets, score):
    results = Run(targets, exit=False)
    if results.linter.stats['global_note'] < score:
        print "Your code has been rated too low, expected score {} and more".format(score)
        sys.exit(1)
    print "Pylint successful"
    sys.exit(0)


if __name__ == '__main__':
    lint(args.targets, args.score)