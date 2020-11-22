import argparse
import pandas as pd


def search_options():
    data = pd.read_json('car-list.json')
    brands = data['brand'].tolist()

    # Create the parser and add arguments
    parser = argparse.ArgumentParser()
    # subparsers = parser.add_subparsers(help='commands')

    # parser.add_argument('-t', help="Car brand: ", choices=['BMW', 'Mercedes-Benz', 'Nissan'])
    # create_parser = subparsers.add_parser('create', help='Create a directory')
    parser.add_argument('-b', help="Car brand: ", choices=brands)
    parser.add_argument('-m', help="Brand model", choices=['Passat', 'Vectra', 'X3',''])
    parser.add_argument('-f', help="Fuel type: ", choices=['Toate', 'Benzina', 'Diesel', 'GPL', 'Hybrid', 'Electic'])
    parser.add_argument('-g', help="Gearbox: ", choices=['manuala', 'automata'])

    '''
    By default argparse create all the arguments at once.
    So I must find ways to sort this out
    
    https://docs.python.org/3.4//library/argparse.html
    https://stackoverflow.com/questions/54383659/python-argparse-value-after-positional-argument
    https://pymotw.com/2/argparse/
    
    args = parser.parse_args()
    b = args.b
    models = data[data['brand'] == b]['models'].tolist()[0]
    print(models)
    parser.add_argument('-m', help="Brand model: ", choices=models)
    '''

    args = parser.parse_args()
    b, f, g = args.b, args.f, args.g
    models = data[data['brand'] == b]['models'].tolist()[0]

    for opt, val in zip(["-b", "-f", "-g"], [b, f, g]):
        print(opt, val)

    print("Choose one of these models: {} {} {}".format("\n", models, "\n"))
    m = input("Model: ")
    if m not in models:
        m = ""
        print("Incorrect model option")

    query = ""

    for item in [b, m, f, g]:
        if item is not None:
            query += item + " "

    return query


if __name__ == "__main__":

    q = search_options()
    print(q)