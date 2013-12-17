# Copyright 2013 Eucalyptus Systems, Inc.
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


import hashlib
import itertools
import multiprocessing
import os

import euca2ools.bundle.pipes
import euca2ools.bundle.util


def create_bundle_part_writer(infile, part_prefix, part_size):
    partinfo_result_mpqueue = multiprocessing.Queue()

    pid = os.fork()
    if pid == 0:
        for part_no in itertools.count():
            part_fname = '{0}.part.{1}'.format(part_prefix, part_no)
            part_digest = hashlib.sha1()
            with open(part_fname, 'w') as part:
                bytes_written = 0
                bytes_to_write = part_size
                while bytes_written < part_size:
                    chunk = infile.read(min((part_size - bytes_to_write,
                                             euca2ools.bundle.pipes._BUFSIZE)))
                    if chunk:
                        part.write(chunk)
                        part_digest.update(chunk)
                        bytes_to_write -= len(chunk)
                    else:
                        break
                partinfo = euca2ools.bundle.BundlePart(
                    part_fname, part_digest.hexdigest(), 'SHA1')
                partinfo_result_mpqueue.put(partinfo)
            if bytes_written < part_size:
                # That's the last part
                infile.close()
                partinfo_result_mpqueue.close()
                partinfo_result_mpqueue.join_thread()
                os._exit(os.EX_OK)
    infile.close()
    euca2ools.bundle.util.waitpid_in_thread(pid)
    return partinfo_result_mpqueue