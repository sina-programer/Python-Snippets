import configparser

config = configparser.ConfigParser()
config.read('config.ini')

for section in list(config.keys())[1:]:
    print()
    print(f' {section} '.center(20, '-'))
    for item in config[section]:
        print(f"{item} = <{config.get(section, item)}>")


server = config['Proxy']['server']
