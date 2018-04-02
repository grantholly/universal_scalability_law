import multiprocessing
import string

from map_reduce import SimpleMapReduce

def file_to_letters(filename):
    """Read a file and return a sequence of (letter, occurances) values.
    """
    TR = string.maketrans(string.punctuation, ' ' * len(string.punctuation))

    print multiprocessing.current_process().name, 'reading', filename
    output = []

    with open(filename, 'rt') as f:
        for line in f:
            if line.lstrip().startswith('..'): # Skip rst comment lines
                continue
            line = line.translate(TR) # Strip punctuation
            for word in line.split():
                word = word.lower()
                if word.isalpha():
                    for letter in word:
                        output.append( (letter, 1) )
    return output


def count_letters(item):
    """Convert the partitioned data for a word to a
    tuple containing the word and the number of occurances.
    """
    letter, occurances = item
    return (letter, sum(occurances))


if __name__ == '__main__':
    import operator
    import glob

    input_files = glob.glob('*.txt')

    mapper = SimpleMapReduce(file_to_letters, count_letters)
    letter_counts = mapper(input_files)
    letter_counts.sort(key=operator.itemgetter(1))
    letter_counts.reverse()

    print '\nTOP LETTERS BY FREQUENCY\n'
    longest = max(len(letter) for letter, count in letter_counts)
    for letter, count in letter_counts:
        print '%-*s: %5s' % (longest+1, letter, count)
