#!/usr/bin/env python

__author__ = "Mike McCann"
__copyright__ = "Copyright 2011, MBARI"
__credits__ = ["Chander Ganesan, Open Technology Group"]
__license__ = "GPL"
__version__ = "$Revision: 12276 $".split()[1]
__maintainer__ = "Mike McCann"
__email__ = "mccann at mbari.org"
__status__ = "Development"
__doc__ = '''

Unit tests for the STOQS project.  Test with:
    python -Wall manage.py test stoqs -v 2


Mike McCann
MBARI Dec 29, 2011

@var __date__: Date of last svn commit
@undocumented: __doc__ parser
@author: __author__
@status: __status__
@license: __license__
'''

import os
import sys
import time
import json

from django.utils import unittest
from django.test.client import Client
from django.test import TestCase
from django.core.urlresolvers import reverse

from stoqs.models import Activity
import logging
import time

logger = logging.getLogger(__name__)


class BaseAndMeasurementViewsTestCase(TestCase):
    fixtures = ['stoqs_test_data.json']
    format_types = ['html', 'json', 'xml', 'csv']
    multi_db = False
    
    def setup(self):
        ##call_setup_methods()
        pass

    # Base class view tests
    def test_campaign(self):
        for fmt in self.format_types:
            req = reverse('show-campaign', kwargs={'format': fmt,
                                                   'dbAlias': 'default'})
            response = self.client.get(req)
            self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
    
    def test_parameter(self):
       for fmt in self.format_types:
           req = reverse('show-parameter', kwargs={'format': fmt,
                                                   'dbAlias': 'default'})
           response = self.client.get(req)
           self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
   
    def test_platform(self):
       for fmt in self.format_types:
           req = reverse('show-platform', kwargs={'format': fmt,
                                                  'dbAlias': 'default'})
           response = self.client.get(req)
           self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)

    def test_platformType(self):
       for fmt in self.format_types:
           req = reverse('show-platformtype', kwargs={'format': fmt,
                                                      'dbAlias': 'default'})
           response = self.client.get(req)
           self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
   
    def test_activity(self):
       for fmt in self.format_types:
           req = reverse('show-activity', kwargs={'format': fmt,
                                                  'dbAlias': 'default'})
           response = self.client.get(req)
           self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)

    def test_activityType(self):
       for fmt in self.format_types:
           req = reverse('show-activitytype', kwargs={'format': fmt,
                                                      'dbAlias': 'default'})
           response = self.client.get(req)
           self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
    
    def test_activity_parameter(self):
       for fmt in self.format_types:
           req = reverse('show-activityparameter', kwargs={'format': fmt,
                                                           'dbAlias': 'default'})
           response = self.client.get(req)
           self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
   
    def test_resource(self):
       for fmt in self.format_types:
           req = reverse('show-resource', kwargs={'format': fmt,
                                                  'dbAlias': 'default'})
           response = self.client.get(req)
           self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
    
    def test_resourceType(self):
       for fmt in self.format_types:
           req = reverse('show-resourcetype', kwargs={'format': fmt,
                                                      'dbAlias': 'default'})
           response = self.client.get(req)
           self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
   
    def test_activity_resource(self):
       for fmt in self.format_types:
           req = reverse('show-activityresource', kwargs={'format': fmt,
                                                          'dbAlias': 'default'})
           response = self.client.get(req)
           self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)

    def test_query_jsonencoded(self):
        req = reverse('stoqs-query-results', kwargs={'format': 'json',
                                                     'dbAlias': 'default'})
        response = self.client.get(req)
        json.loads(response.content) # Verify we don't get an exception when we load the data.
        self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)

    def test_query_summary(self):
        req = reverse('stoqs-query-summary', kwargs={'dbAlias': 'default'})
        response = self.client.get(req)
        json.loads(response.content) # Verify we don't get an exception when we load the data.
        self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
   
    def test_query_ui(self):
        req = reverse('stoqs-query-ui', kwargs={'dbAlias': 'default'})
        response = self.client.get(req)
        self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
   
    # Measurement view tests 
    def test_measurementStandardNameBetween(self):
        # For the load of:
        #   http://dods.mbari.org/opendap/data/auvctd/surveys/2010/netcdf/Dorado389_2010_300_00_300_00_decim.nc
        #   with stride = 1000    
        # there are 47 measurements for each parameter
        for parm in ('sea_water_salinity', 'sea_water_temperature', 'sea_water_sigma_t', 
                     'mass_concentration_of_chlorophyll_in_sea_water',
                    ):
            req = '/test_stoqs/measurement/sn/%s/between/20101027T215155/20101028T155157/depth/0/300/count' % parm
            response = self.client.get(req)
            self.assertEqual(response.content, '47', 'Measurement between count for %s' % req)  # ?
            
        # Make sure all the formats return 200
        for fmt in ('html', 'csv', 'kml'):
            req = '/test_stoqs/measurement/sn/sea_water_salinity/between/20101028T075155/20101029T015157/depth/0/300/data.%s' % fmt
            response = self.client.get(req)
            self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
        
        # Now with a stride
        for fmt in ('html', 'csv', 'kml'):
            req = '/test_stoqs/measurement/sn/sea_water_salinity/between/20101028T075155/20101029T015157/depth/0/300/stride/10/data.%s' % fmt
            response = self.client.get(req)
            self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
  
    def test_measurementBetween(self):
        
        # For the load of:
        #   http://dods.mbari.org/opendap/data/auvctd/surveys/2010/netcdf/Dorado389_2010_300_00_300_00_decim.nc
        #   with stride = 1000    
        # there are 47 measurements for each parameter
        for parm in ('bbp420', 'bbp700', 'biolume', 'fl700_uncorr', 'mass_concentration_of_chlorophyll_in_sea_water',
                    'nitrate', 'oxygen', 'salinity', 'sea_water_sigma_t', 'temperature'):
            req = '/test_stoqs/measurement/%s/between/20101027T215155/20101028T155157/depth/0/300/count' % parm
            response = self.client.get(req)
            self.assertEqual(response.content, '47', 'Measurement between count for %s' % req)  # ?
           
        # Make sure all the formats return 200
        for fmt in ('html', 'csv', 'kml'):
            req = '/test_stoqs/measurement/temperature/between/20101028T075155/20101029T015157/depth/0/300/data.%s' % fmt
            response = self.client.get(req)
            self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
        
        # Now with a stride
        for fmt in ('html', 'csv', 'kml'):
            req = '/test_stoqs/measurement/temperature/between/20101028T075155/20101029T015157/depth/0/300/stride/10/data.%s' % fmt
            response = self.client.get(req)
            self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
   
    # Management tests 
    def test_manage(self):
        req = '/test_stoqs/mgmt'
        response = self.client.get(req)
        self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
        
        req = '/test_stoqs/activitiesMBARICustom'
        response = self.client.get(req)
        self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
        loadedText = '498 MeasuredParameters'
        self.assertTrue(response.content.find(loadedText) != -1, 'Should find "%s" string at %s' % (loadedText, req))
        
        req = '/test_stoqs/deleteActivity/1'
        response = self.client.get(req)
        self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
        
        # Now test that the activity was deleted, after sleeping for a bit.  Need to see if Celery can provide notification
        # This should work, but as of 10 Jan 2010 it does not.  COmmented out for now.
#        logger.info('Sleeping after delete')
#        time.sleep(20)
#        req = '/test_stoqs/activities'
#        response = self.client.get(req)
#        logger.debug(response.content)
#        self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
#        self.assertTrue(response.content.find(loadedText) == -1, 'Should not find "%s" string at %s' % (loadedText, req))

    
#    def test_admin_stoqs_that_should_be_there(self):
#	'''Need to pass login credentials, and create the login...'''
#        req='http://localhost:8000/test_stoqs/admin/stoqs'
#        response = self.client.get(req)
#        self.assertEqual(response.status_code, 200, 'Status code should be 200 for %s' % req)
#        logger.debug(response.content)
        