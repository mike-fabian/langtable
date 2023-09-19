from .langtable import *
from .langtable import _test_language_territory
from .langtable import _test_cldr_locale_pattern
from .langtable import _init
from .langtable import _languages_db
from .langtable import _territories_db
from .langtable import _timezoneIdParts_db
from .langtable import _write_files

#  Deleting a module prevents one from import <pack>.somemodule1
#  directly. You can only import from <pack> objects defined or
#  imported in its __init__.py, and non-deleted submodules.
del langtable # type: ignore

