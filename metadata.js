module.exports = {
  'name': 'zip compress',                                 
  'description': 'Auto-decompression of OSS uploading super-large zip compressed files by function computer',                    
  'userPrompt': [                                         
    {
      'type': 'input',                             
      'name': 'bucketName',                                 
      'message': 'Please input oss bucketName?'            
    },
    {
      'type': 'input',                             
      'name': 'prefix',                                 
      'message': 'Please input prefix?',
      validate: function(pre) {
        if (pre.startsWith('/')) {
          return pre;
        }
        return "请以/结尾";
      }
    },
    {
      'type': 'input',                             
      'name': 'unzipFileDirectory',                                 
      'message': 'Please input unzip file directory?',
    },
    {
      'type': 'list',                             
      'name': 'suffix',                                 
      'message': 'Please choose a file suffix?',
      'choices': [
        '.zip',
        '.jar'
      ]
    }
  ],
  'vars': {
    'service': '{{ projectName }}'
  }
}