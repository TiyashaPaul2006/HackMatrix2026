"""
URL Feature Extraction Pipeline
Reproduces the 16 exact numerical features used during training for real-time inference.
"""

import math
import re
from collections import Counter
from urllib.parse import urlparse
import numpy as np
import pandas as pd

FEATURE_NAMES = [
    'url_length',
    'has_ip_address',
    'dot_count',
    'https_flag',
    'url_entropy',
    'token_count',
    'subdomain_count',
    'query_param_count',
    'tld_length',
    'path_length',
    'has_hyphen_in_domain',
    'number_of_digits',
    'tld_popularity',
    'suspicious_file_extension',
    'domain_name_length',
    'percentage_numeric_chars'
]

SUSPICIOUS_EXTENSIONS = {'.exe', '.bin', '.apk', '.zip', '.cmd', '.js', '.1exe', '.sh', '.vbs', '.bat', '.scr'}
POPULAR_TLDS = {'com'}

IP_PATTERN = re.compile(
    r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?::\d+)?$'
)


def calculate_entropy(text: str) -> float:
    """Calculate Shannon entropy (base 2) for a given string."""
    if not text:
        return 0.0
    length = len(text)
    counts = Counter(text)
    return -sum((c / length) * math.log2(c / length) for c in counts.values())


def extract_features_from_url(raw_url: str) -> dict:
    """
    Extracts all 16 features from a raw URL string matching training definitions.
    """
    url = raw_url.strip()
    if not url:
        raise ValueError("URL cannot be empty")

    # Add scheme if missing for accurate urlparse parsing
    has_scheme = bool(re.match(r'^[a-zA-Z]+://', url))
    parse_url = url if has_scheme else 'http://' + url

    try:
        parsed = urlparse(parse_url)
    except Exception:
        parsed = urlparse('http://invalid')

    netloc = parsed.netloc.split(':')[0].lower()
    path = parsed.path if parsed.path else ('/' if url.endswith('/') else '')
    query = parsed.query

    # 1. url_length
    url_length = len(url)

    # 2. has_ip_address
    # Check if host or full netloc is an IP address
    host_clean = netloc
    is_ip = 1 if bool(IP_PATTERN.match(host_clean)) else 0
    # Also check if raw url starts with IP directly
    if not is_ip:
        raw_host = url.split('/')[2] if '://' in url else url.split('/')[0]
        raw_host = raw_host.split(':')[0]
        if IP_PATTERN.match(raw_host):
            is_ip = 1

    # 3. dot_count
    dot_count = url.count('.')

    # 4. https_flag
    https_flag = 1 if url.lower().startswith('https://') else 0

    # 5. url_entropy
    url_entropy = calculate_entropy(url)

    # 6. token_count: delimiters count + 1
    # Count dots, slashes, query delimiters (? and &)
    delim_count = url.count('.') + url.count('/') + url.count('?') + url.count('&')
    token_count = max(1, delim_count + 1)

    # 7. domain parsing for domain_name_length, tld_length, subdomain_count, tld_popularity
    # Clean host parts
    host_parts = [p for p in netloc.split('.') if p]
    if is_ip or len(host_parts) == 0:
        subdomain_count = np.nan
        domain_name_length = np.nan
        tld_length = 0
        tld_popularity = 0
        has_hyphen_in_domain = 1 if '-' in netloc else 0
    else:
        tld = host_parts[-1]
        tld_length = len(tld)
        tld_popularity = 1 if tld in POPULAR_TLDS else 0
        
        if len(host_parts) >= 2:
            main_domain = host_parts[-2]
            domain_name_length = float(len(main_domain))
            subdomains = host_parts[:-2]
            # Strip 'www' if it's the only subdomain
            subdomain_count = float(len(subdomains))
        else:
            main_domain = host_parts[0]
            domain_name_length = float(len(main_domain))
            subdomain_count = 0.0

        has_hyphen_in_domain = 1 if '-' in netloc else 0

    # 8. query_param_count
    if query:
        query_param_count = len([q for q in query.split('&') if q])
        query_param_count = max(1, query_param_count)
    else:
        query_param_count = 1

    # 10. path_length
    path_length = len(path)

    # 12. number_of_digits
    number_of_digits = sum(c.isdigit() for c in url)

    # 14. suspicious_file_extension
    suspicious_file_ext = 0
    path_lower = path.lower()
    for ext in SUSPICIOUS_EXTENSIONS:
        if path_lower.endswith(ext) or (ext + '?') in path_lower or (ext + '/') in path_lower:
            suspicious_file_ext = 1
            break

    # 16. percentage_numeric_chars
    percentage_numeric = (number_of_digits / url_length) * 100.0 if url_length > 0 else 0.0

    return {
        'url_length': url_length,
        'has_ip_address': is_ip,
        'dot_count': dot_count,
        'https_flag': https_flag,
        'url_entropy': round(url_entropy, 9),
        'token_count': token_count,
        'subdomain_count': subdomain_count,
        'query_param_count': query_param_count,
        'tld_length': tld_length,
        'path_length': path_length,
        'has_hyphen_in_domain': has_hyphen_in_domain,
        'number_of_digits': number_of_digits,
        'tld_popularity': tld_popularity,
        'suspicious_file_extension': suspicious_file_ext,
        'domain_name_length': domain_name_length,
        'percentage_numeric_chars': round(percentage_numeric, 8)
    }


def extract_features_dataframe(urls: list[str]) -> pd.DataFrame:
    """Convert a list of raw URLs into a DataFrame of 16 features."""
    rows = [extract_features_from_url(u) for u in urls]
    return pd.DataFrame(rows, columns=FEATURE_NAMES)

