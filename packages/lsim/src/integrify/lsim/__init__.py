"""
Dokumentasiya:

EN: https://integrify.mmzeynalli.dev/integrations/lsim/official/api/
"""

from .bulk.client import LSIMBulkSMSAsyncClient, LSIMBulkSMSClient, LSIMBulkSMSClientClass
from .bulk.env import VERSION as BULKSMS_VERSION
from .single.client import LSIMSingleSMSAsyncClient, LSIMSingleSMSClient, LSIMSingleSMSClientClass
from .single.env import VERSION as SINGLESMS_VERSION

__all__ = [
    'LSIMBulkSMSAsyncClient',
    'LSIMBulkSMSClient',
    'LSIMBulkSMSClientClass',
    'BULKSMS_VERSION',
    'LSIMSingleSMSAsyncClient',
    'LSIMSingleSMSClient',
    'LSIMSingleSMSClientClass',
    'SINGLESMS_VERSION',
]
