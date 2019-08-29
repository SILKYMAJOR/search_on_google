import os
import requests
import sys
import yaml

GOOGLE_HOST = "https://google.com/"

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
}


def banner(search_host):
    print('-' * 60)
    print('[*] Search "{}" on Google'.format(search_host))
    print('-' * 60)


def parse_arg():
    if len(sys.argv) == 1:
        print("Usage: python {} example.com".format(os.path.basename(__file__)))
        sys.exit()
    else:
        return sys.argv[1]


def read_yaml(file):
    with open(file) as f:
        yml = yaml.load(f)
    return yml


def main():
    search_host = parse_arg()
    search_list = read_yaml("search_list.yaml")
    banner(search_host)

    for search_item in search_list:
        url = GOOGLE_HOST + search_item['query'].format(site=search_host)
        res = requests.get(url=url, headers=REQUEST_HEADERS)

        if res.text.find("recaptcha"):
            print("[-]" + search_item['perspective'] + ": Determined as a robot", url, sep='\t')
            continue

        if res.status_code == 200:
            print("[!]" + search_item['perspective'] + ": Found", url, sep='\t')
        elif res.status_code == 429:
            print("[-]" + search_item['perspective'] + ": None", url, sep='\t')
        else:
            print("[E]" + search_item['perspective'] + ": Unexpected response {}".format(res.status_code))


if __name__ == '__main__':
    main()
