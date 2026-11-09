import math
import re
from urllib.parse import urlparse

POPULAR_TLDS = {
    'com', 'org', 'net', 'edu', 'gov', 'mil', 'co', 'io', 'ai', 'app', 'dev',
    'uk', 'ca', 'de', 'jp', 'fr', 'au', 'in', 'us'
}

SUSPICIOUS_EXTENSIONS = {
    '.exe', '.zip', '.tar', '.gz', '.rar', '.bin', '.apk', '.bat', '.cmd',
    '.scr', '.vbs', '.js', '.jar', '.wsf', '.iso', '.php'
}

IPV4_REGEX = re.compile(
    r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
)

def calculate_entropy(text: str) -> float:
    if not text:
        return 0.0
    prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    entropy = -sum([p * math.log2(p) for p in prob])
    return round(entropy, 4)

def extract_features(url: str) -> dict:
    url_clean = url.strip()

    if not re.match(r'^[a-zA-Z]+://', url_clean):
        parsed = urlparse('http://' + url_clean)
    else:
        parsed = urlparse(url_clean)

    hostname = (parsed.hostname or '').lower()
    path = parsed.path or ''
    query = parsed.query or ''

    url_length = len(url_clean)
    has_ip = 1 if IPV4_REGEX.match(hostname) else 0
    dot_count = url_clean.count('.')
    https_flag = 1 if parsed.scheme.lower() == 'https' else 0
    url_entropy = round(calculate_entropy(url_clean), 4)

    tokens = [t for t in re.split(r'[./\\-_?=&]', url_clean) if t]
    token_count = len(tokens)

    subdomain_parts = hostname.split('.')
    if len(subdomain_parts) > 2:
        subdomain_count = len(subdomain_parts) - 2
    else:
        subdomain_count = 0

    query_params = query.split('&') if query else []
    query_param_count = len([p for p in query_params if p])

    tld = subdomain_parts[-1] if subdomain_parts else ''
    tld_length = len(tld)
    path_length = len(path)
    has_hyphen_in_domain = 1 if '-' in hostname else 0
    number_of_digits = sum(c.isdigit() for c in url_clean)
    tld_popularity = 1 if tld in POPULAR_TLDS else 0

    suspicious_file_extension = 0
    lower_path = path.lower()
    for ext in SUSPICIOUS_EXTENSIONS:
        if lower_path.endswith(ext):
            suspicious_file_extension = 1
            break

    domain_name_length = len(hostname)
    percentage_numeric_chars = round((number_of_digits / url_length) * 100.0, 4) if url_length > 0 else 0.0

    return {
        'url_length': url_length,
        'has_ip_address': has_ip,
        'dot_count': dot_count,
        'https_flag': https_flag,
        'url_entropy': url_entropy,
        'token_count': token_count,
        'subdomain_count': subdomain_count,
        'query_param_count': query_param_count,
        'tld_length': tld_length,
        'path_length': path_length,
        'has_hyphen_in_domain': has_hyphen_in_domain,
        'number_of_digits': number_of_digits,
        'tld_popularity': tld_popularity,
        'suspicious_file_extension': suspicious_file_extension,
        'domain_name_length': domain_name_length,
        'percentage_numeric_chars': percentage_numeric_chars
    }

FEATURE_NAMES = [
    'url_length', 'has_ip_address', 'dot_count', 'https_flag', 'url_entropy',
    'token_count', 'subdomain_count', 'query_param_count', 'tld_length',
    'path_length', 'has_hyphen_in_domain', 'number_of_digits', 'tld_popularity',
    'suspicious_file_extension', 'domain_name_length', 'percentage_numeric_chars'
]

