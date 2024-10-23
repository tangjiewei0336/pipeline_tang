from schematic.verb import verb


@verb
def hello(input_file, output_folder):
    with open(input_file, 'r') as f:
        print(f.read())
    with open(output_folder + "/output.txt", 'w') as f:
        f.write("Hello, world!")


if __name__ == '__main__':
    hello()