import argparse

parser = argparse.ArgumentParser(description='description of your program')
parser.add_argument('--name', help='description of name')
parser.add_argument('--age', help='description of age')
args = parser.parse_args()

if __name__ == "__main__":
	print(args.name)
	print(args.age)