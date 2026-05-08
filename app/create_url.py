from urllib.parse import urlencode

BASE_URL = "https://hh.ru/search/vacancy"

DEFAULT_PARAMS = {
    "salary": "",
    "ored_clusters": "true",
    "hhtmFrom": "vacancy_search_list",
    "hhtmFromLabel": "vacancy_search_list",
}

def build_search_url(custom_params: dict, page: int = 0) -> str:
    params = {**DEFAULT_PARAMS, **custom_params, "page": page,}
    
    return f"{BASE_URL}?{urlencode(params)}"