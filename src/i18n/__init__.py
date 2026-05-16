import json
import os
import sys

_zh = None
_en = None
_es = None

if getattr(sys, 'frozen', False):
    ROOT_DIR = sys._MEIPASS
else:
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

USER_CONFIG_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "WinOptimizer")
USER_CONFIG_PATH = os.path.join(USER_CONFIG_DIR, "config.json")
DEFAULT_CONFIG_PATH = os.path.join(ROOT_DIR, "config.json")
I18N_DIR = os.path.dirname(os.path.abspath(__file__))


def _load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_all():
    global _zh, _en, _es
    _zh = _load_json(os.path.join(I18N_DIR, "zh.json"))
    _en = _load_json(os.path.join(I18N_DIR, "en.json"))
    _es = _load_json(os.path.join(I18N_DIR, "es.json"))


def reload_language(lang=None):
    if lang is None:
        lang = _get_config_language()
    _load_all()


def _get_config_language():
    for cfg_path in (USER_CONFIG_PATH, DEFAULT_CONFIG_PATH):
        try:
            if os.path.exists(cfg_path):
                with open(cfg_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                return config.get("language", "en")
        except Exception:
            pass
    return "en"


def tr(key, lang=None, **kwargs):
    global _zh, _en, _es
    if _zh is None:
        _load_all()
    if lang is None:
        lang = _get_config_language()
    translations = {"zh": _zh, "en": _en, "es": _es}
    t = translations.get(lang, _zh)
    parts = key.split(".")
    value = t
    for part in parts:
        if isinstance(value, dict):
            value = value.get(part, key)
        else:
            return key
    if isinstance(value, dict):
        return key
    if kwargs and isinstance(value, str):
        try:
            return value.format(**kwargs)
        except KeyError:
            return value
    return value


def _resolve_config_path():
    if os.path.exists(USER_CONFIG_PATH):
        return USER_CONFIG_PATH
    return DEFAULT_CONFIG_PATH


def get_config():
    cfg_path = _resolve_config_path()
    try:
        if os.path.exists(cfg_path):
            with open(cfg_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {
        "app": {"name": "WinOptimizer", "version": "1.0.0", "author": "lorime", "email": "lorime@126.com"},
        "language": "en",
        "languages": ["zh", "en", "es"],
    }


def save_config(config):
    os.makedirs(USER_CONFIG_DIR, exist_ok=True)
    with open(USER_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)


def set_language(lang):
    config = get_config()
    config["language"] = lang
    save_config(config)
    reload_language(lang)