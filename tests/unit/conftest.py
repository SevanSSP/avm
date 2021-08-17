import os
import pytest
from avm import registered_applications


@pytest.fixture(scope='function')
def setUp():
        # path to application listing file
        ret = {'xml': os.path.join(os.path.dirname(__file__), 'data', 'ApplicationVersions.xml'),
               'apps': registered_applications(appverxml=os.path.join(os.path.dirname(__file__), 'data', 'ApplicationVersions.xml'))
               }
        return ret
