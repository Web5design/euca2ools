# Copyright 2011-2013 Eucalyptus Systems, Inc.
#
# Redistribution and use of this software in source and binary forms,
# with or without modification, are permitted provided that the following
# conditions are met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from euca2ools.commands import Euca2ools
from requestbuilder import Arg, MutuallyExclusiveArgList
from requestbuilder.request import BaseRequest
from requestbuilder.service import BaseService


class EuStore(BaseService):
    NAME = 'eustore'
    DESCRIPTION = 'Eucalyptus Image Store'
    REGION_ENVVAR = 'EUCA_REGION'
    URL_ENVVAR = 'EUSTORE_URL'
    ARGS = [MutuallyExclusiveArgList(
                Arg('--region', dest='userregion', metavar='USER@REGION',
                    help='''name of the region and/or user in config files to
                    use to connect to the service'''),
                Arg('-U', '--url', help='EuStore service URL'))]


class EuStoreRequest(BaseRequest):
    SUITE = Euca2ools
    SERVICE_CLASS = EuStore
    DEFAULT_ROUTES = ()
