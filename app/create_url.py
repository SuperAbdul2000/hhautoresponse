from urllib.parse import urlencode

BASE_URL = "https://hh.ru/search/vacancy"

#обязательные парамметры, которые я не изменяю для постройки базового url с вакансиями
DEFAULT_PARAMS = {
    "salary": "",
    "ored_clusters": "true",
    "hhtmFrom": "vacancy_search_list",
    "hhtmFromLabel": "vacancy_search_list",
}

#функция для построения url с default парамметрами, с параметрами, которые мы изменяем в config и текущей страницей
def build_search_url(custom_params: dict, page: int = 0) -> str:
    params = {**DEFAULT_PARAMS, **custom_params, "page": page,}
    
    return f"{BASE_URL}?{urlencode(params)}"
