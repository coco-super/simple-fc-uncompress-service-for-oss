# -*- coding: utf-8 -*-
import oss2, json
import zipfile
import os, io
import logging

LOGGER = logging.getLogger()

def handler(event, context):
  """
  The object from OSS will be decompressed automatically .
  param: event:   The OSS event json string. Including oss object uri and other information.
      For detail info, please refer https://help.aliyun.com/document_detail/70140.html?spm=a2c4g.11186623.6.578.5eb8cc74AJCA9p#OSS
  
  param: context: The function context, including credential and runtime info.

      For detail info, please refer to https://help.aliyun.com/document_detail/56316.html#using-context
  """
  evt_lst = json.loads(event)
  creds = context.credentials
  auth=oss2.StsAuth(
     creds.access_key_id,
     creds.access_key_secret,
     creds.security_token)

  evt = evt_lst['events'][0]
  bucket_name = evt['oss']['bucket']['name']
  endpoint = 'oss-' +  evt['region'] + '-internal.aliyuncs.com'
  bucket = oss2.Bucket(auth, endpoint, bucket_name)
  object_name = evt['oss']['object']['key']

  """
  When a source/ prefix object is placed in an OSS, it is hoped that the object will be decompressed and then stored in the OSS as processed/ prefixed.
  For example, source/a.zip will be processed as processed/a/... 
  "source /", "processed/" can be changed according to the user's requirements."""

  file_type = os.path.splitext(object_name)[1]

  if file_type != ".zip":
    raise RuntimeError('{} filetype is not zip'.format(object_name))

  newKey = object_name.replace("source/", "processed/")
  remote_stream = bucket.get_object(object_name)
  if not remote_stream:
    raise RuntimeError('failed to get oss object. bucket: %s. object: %s' % (bucket_name, object_name))
  zip_buffer = io.BytesIO(remote_stream.read())

  LOGGER.info('download object from oss success: {}'.format(object_name))

  newKey = newKey.replace(".zip", "/")
  with zipfile.ZipFile(zip_buffer) as zip_file:
    for name in zip_file.namelist():
      with zip_file.open(name) as file_obj:
        # fix chinese directory name garbled problem
        try:
          name = name.encode(encoding='cp437')
        except:
          name = name.encode(encoding='utf-8')
        detect = chardet.detect( (name*100)[0:100] )
        confidence = detect["confidence"]
        if confidence >= 0.8:
          try:
            name = name.decode(encoding=detect["encoding"])
          except: 
            name = name.decode(encoding="gb2312")
        else:
           name = name.decode(encoding="gb2312")
          
        bucket.put_object(newKey +  name, file_obj.read())