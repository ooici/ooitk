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

class DataProductCatalog(object):

    def __init__(self, host='localhost', port=3000):
        self.host = host
        self.port = port
        self.cached = None


    def list_data_products(self, refresh=False):
        '''
        Returns a list of data product resources
        '''
        if not refresh and self.cached is not None:
            return self.cached

        resp = requests.get('http://%s:%s/DataProduct/list/' % (self.host, self.port), headers={'Content-type':'application/json', 'Accept':'application/json'})
        if resp.status_code == 200:
            content = resp.json()
            content = content['data'] # Now a list of data products
            self.cached = content
            return content
        return []

    def named_listing(self):
        '''
        Returns a dictionary of Data Product Name and Data Product Resource
        '''
        listing = self.list_data_products()
        listing = {i['name'] : i for i in listing}
        return listing
    
    def list_parameters(self, data_product_id):
        resp = requests.get('http://%s:%s/DataProduct/parameters/%s/' % (self.host, self.port, data_product_id))
        if resp.status_code == 200:
            content = resp.json()
            content = content['data']
            return content
        return []

