#!/usr/bin/env python
'''
Copyright (c) 2013, UC Regents
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of the FreeBSD Project.
'''

import requests
from ooitk.serial import Serializer
from ooitk.exception import ConnectionError, GatewayError

class Session:
    host='localhost'
    port=5000
    def __init__(self, host, port):
        self.url = 'http://%s:%s/ion-service/' % (host, port)
    

class Service:
    session=None
    def __init__(self, session):
        self.session = session

    def request(self,service_name, op, **kwargs):
        url = self.session.url
        url = url + service_name + '/' + op
        r = { "serviceRequest": { 
            "serviceName" : service_name, 
            "serviceOp" : op, 
            "params" : kwargs
            }
        }
        resp = requests.post(url, data={'payload':Serializer.encode(r)})
        if resp.status_code == 200:
            data = resp.json()
            if 'GatewayError' in data['data']:
                error = GatewayError(data['data']['Message'])
                error.trace = data['data']['Trace']
                raise error
            if 'GatewayResponse' in data['data']:
                return data['data']['GatewayResponse']

        raise ConnectionError("HTTP [%s]" % resp.status_code)


def retrieve(session, **kwargs):
    url = session.url
    url += 'retrieve'


    r = {'serviceRequest':{'params':kwargs}}
    
    resp = requests.post(url, data={'payload':Serializer.encode(r)})
    data = Serializer.decode(resp.text)
    data = data['data']['GatewayResponse']['value_dict']
    return data

