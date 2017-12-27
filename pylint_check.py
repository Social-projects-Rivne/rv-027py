import argparse
import sys

from pylint.lint import Run

parser = argparse.ArgumentParser(
    description='Make pylint to pass with custom score.')
parser.add_argument('-t', '--targets', nargs='+', dest='targets',
                    help='space separated paths to target modules or packages')
parser.add_argument('-s', '--score', type=float, dest='score',
                    default=7.0, help='float number, the affordable pylint score')
parser.add_argument('-l', '--load', dest='load_plugins',
                    help='load some plugins')

args = parser.parse_args()
args.load_plugins = ''.join(['--load-plugins=', args.load_plugins])
args.targets.append(args.load_plugins)


def _check_score(lint_results, score):
    if lint_results.linter.stats['global_note'] < score:
        print "Your code has been rated too low, expected score {} and more".format(score)
        sys.exit(1)


def _check_critical(lint_results):
    fatals = lint_results.linter.stats['fatal']
    errors = lint_results.linter.stats['error']
    if fatals > 0 or errors > 0:
        print "Encountered {0} fatals and {1} errors".format(fatals, errors)
        sys.exit(1)


def lint(targets, score):
    results = Run(targets, exit=False)
    _check_critical(results)
    _check_score(results, score)
    print "Pylint successful"
    sys.exit(0)


if __name__ == '__main__':
    lint(args.targets, args.score)
