from helpers.data import EXPECTED_DOMAINS

def check_domains(current_url) -> bool:
    return any(domain in current_url for domain in EXPECTED_DOMAINS)