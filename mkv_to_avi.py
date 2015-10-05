#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Matheus Rosa <matheusdsrosa@gmail.com>
# Date: 11/07/2010
# Description: This script makes converting MKV files to AVI
# using the tool MEncoder

import sys
import os


def show_info(info):
    """Shows the basic information of the file"""
    
    print '=' * 100
    print 'MKV File: %s' % info['file_name']
    print 'Size: %s' %  info['file_size']
    print '=' * 100

def show_help():
    """Shows how to use the script"""
    print 'MKV to AVI Converter by Matheus Rosa'
    print 'Usage: %s mkv_file.mkv' % sys.argv[0]
    

def human_readable_size(size):
    """Returns the size human readable formatted"""
    
    suffixes = {1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}
    
    if size < 0:
        return 'Could not get the size!'
    
    for suffix in suffixes[1024]:
        size /= 1024
        if size < 1024:
            return '{0:.1f} {1}'.format(size, suffix)
                
def main():
     if len(sys.argv) < 2:
        show_help()
     
     mkv_file = sys.argv[1]
     
     if os.path.exists(mkv_file):
        extension = mkv_file[-3:]
        size = os.path.getsize(mkv_file)
        
        if extension == 'mkv':
            info = {'file_name':mkv_file,'size':human_readable_size(size)}
            show_info(info)
            
            print 'Starting conversion ...'
            os.system('mencoder ' + mkv_file + ' -oac copy -ovc copy -o '+ mkv_file[:-4] + '.avi')
            print 'Done.'
            
        else:
            print 'Invalid file. You need an MKV file to continue.'
     else:
        print 'File %s not found.' % mkv_file
        
if __name__ == '__main__':
    main()
