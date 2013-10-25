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

from ooitk.session import Service
from pydap.client import open_url

class DataProductCatalog(Service):
    static_dap_host = 'localhost'
    static_dap_port = 8001

    def __init__(self, session):
        Service.__init__(self, session)

        self.data_products_cache = []
        self.refresh()

    def find_data_products(self):

        data_products = self.request('resource_registry', 'find_resources', 
                                     restype='DataProduct')
        return data_products

    def refresh(self):
        data_products, irrelevant = self.find_data_products()
        self.data_products_cache = data_products

    def download(self, data_product_id):
        dataset_ids, irrelevant = self.request('resource_registry', 'find_objects', subject=data_product_id, predicate='hasDataset', id_only=True)
        dataset_id = dataset_ids[0]

        dap_url = 'http://%s:%s/%s' %(self.static_dap_host, self.static_dap_port, dataset_id)
        ds = open_url(dap_url)
        return ds

    def list_data_products(self):
        return self.data_products_cache

    def find_data_product(self, name_like):
        relevant = [i for i in self.data_products_cache if name_like.lower() in i['name'].lower()]
        return relevant


