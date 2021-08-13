import os
from avm import registered_applications
import pytest

@pytest.fixture(scope='function')
def setUp():
        # path to application listing file
        ret = {'xml': os.path.join(os.path.dirname(__file__), 'data', 'ApplicationVersions.xml'),
               'apps': registered_applications(appverxml=os.path.join(os.path.dirname(__file__), 'data', 'ApplicationVersions.xml'))
               }
        return ret
