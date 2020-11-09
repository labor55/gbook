
from scrapy.utils.project import get_project_settings as get_pro
import warnings


def get_project_settings():
    warnings.warn("the spam module is deprecated, please use 'from scrapy.utils.project import get_project_settings'", DeprecationWarning,
                  stacklevel=2)
    return get_pro()
