import requests
import concurrent.futures
import argparse
import os

def fetch_from_crtsh(domain):
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        response = requests.get(url)
        if response.status_code == 200:
            return set(cert['name_value'] for cert in response.json() if 'name_value' in cert)
    except Exception as e:
        print(f"Error fetching from crt.sh: {e}")
    return set()

def fetch_from_certspotter(domain):
    try:
        url = f"https://api.certspotter.com/v1/issuances?domain={domain}&expand=dns_names"
        response = requests.get(url)
        if response.status_code == 200:
            return set(name for cert in response.json() for name in cert['dns_names'])
    except Exception as e:
        print(f"Error fetching from CertSpotter: {e}")
    return set()

def process_single_domain(domain):
    crtsh_results = fetch_from_crtsh(domain)
    certspotter_results = fetch_from_certspotter(domain)
    results = crtsh_results.union(certspotter_results)
    print(f"Found {len(results)} unique subdomains for {domain}")
    
    output_file = os.path.join(os.getcwd(), f"{domain}.txt")
    with open(output_file, 'w') as f:
        for subdomain in sorted(results):
            f.write(subdomain + '\n')

def process_batch_domains(input_file, output):
    results = set()
    with open(input_file, 'r') as f:
        for line in f:
            domain = line.strip()
            crtsh_results = fetch_from_crtsh(domain)
            certspotter_results = fetch_from_certspotter(domain)
            results |= crtsh_results.union(certspotter_results)

    print(f"Found {len(results)} unique subdomains")

    if output.endswith('.txt'):
        with open(output, 'w') as f:
            for subdomain in sorted(results):
                f.write(subdomain + '\n')
    else:
        for subdomain in sorted(results):
            domain_name = subdomain.split('.')[0]
            output_file = os.path.join(output, f"{domain_name}.txt")
            with open(output_file, 'a') as f:
                f.write(subdomain + '\n')

def process_input_file(input_file, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(input_file, 'r') as f:
        for line in f:
            domain = line.strip()
            output_file = os.path.join(output_directory, f"{domain}.txt")

            crtsh_results = fetch_from_crtsh(domain)
            certspotter_results = fetch_from_certspotter(domain)
            results = crtsh_results.union(certspotter_results)

            with open(output_file, 'w') as out_f:
                for subdomain in sorted(results):
                    out_f.write(subdomain + '\n')


def main(args):
    if args.domain:
        process_single_domain(args.domain)
    elif args.input:
        output_dir = args.output if args.output else "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        process_input_file(args.input, output_dir)
    else:
        print("Please provide either a single domain with -d or an input file with -i.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-d", "--domain", help="Domain name to fetch subdomains for")
    parser.add_argument("-i", "--input", help="Input file containing domain names, one per line")
    parser.add_argument("-o", "--output", help="Output directory or file to store results")
    args = parser.parse_args()

    main(args)    