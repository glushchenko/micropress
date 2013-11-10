micropress
==========

Python blog generator for hackers  

## Install

pip install micropress  
micropress init — install config in home (~/.microrc) and default templates in ~/Documents/Micropress/ directory.   

## Config

vim ~/.microrc

## Usage 

micropress generate — save public and generated content into build directory.   
micropress preview — blog preview on http://127.0.0.1:8080  
micropress sync — upload content in production server.  

micropress gp - generate content and preview on http://127.0.0.1:8080    
micropress gs - generate and sync  

## Uninstall

pip uninstall micropress  
rm ~/.microrc  
rm -r ~/Documents/Micropress  
