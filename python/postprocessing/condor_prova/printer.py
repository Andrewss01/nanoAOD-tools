
import optparse

parser = optparse.OptionParser()
parser.add_option('-s', '--stringa', dest='parola', type=str, default = 'kakka', help='Please enter a string')

(opt, args) = parser.parse_args()
stringa = opt.parola

print(stringa)
