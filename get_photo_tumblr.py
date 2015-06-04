import string, urllib2  
import re
    
def getContent(url,type):  
    print(">>start connecting:%s" % url)  
    from urllib2 import Request, urlopen, URLError, HTTPError        
    #proxy = urllib2.ProxyHandler({'http':'http://127.0.0.1:8087'})   
    #opener = urllib2.build_opener(proxy,urllib2.HTTPHandler)   
    #urllib2.install_opener(opener)  
    try:  
        urlHandler = urllib2.urlopen(url)  
        headers = urlHandler.info().headers  
        length = 0  
        for header in headers:  
            if header.find('Length') != -1:  
                length = header.split(':')[-1].strip()  
                length = int(length)  
        """
        if(type=="img" and length<15000):
        #if(type=="img"):  
            print(" >>>>>>>>%d" % length)  
            dataStr = 'EOF'  
        else:  
            print(" ++++++++%d" % length)  
            dataStr = urlHandler.read()
        """
        dataStr = urlHandler.read()      
    except HTTPError, e:  
        print 'The server couldn\'t fulfill the request.'  
        print 'Error code: ', e.code  
    except URLError, e:  
        print 'We failed to reach a server.'  
        print 'Reason: ', e.reason  
    else:
        return dataStr 

def baidu_tieba(url,current_page='/page/1',x=1):
    if int(current_page.split('/')[-1])<=end_page:       
        if url == bdurl:
            dataStr = getContent(url+current_page,"html") 
            reg_img = r"""img.+src\s*=\s*"(\S+)\.(\w+)"(data-highres|\s+)"""
        '''
        else:
            dataStr = getContent(url,"html")
            reg_img = r"""a\s+href\s*=\s*"?(\S+)\.(\w+)"""          
        '''
        urlre_img = re.compile(reg_img)
        imglist = urlre_img.findall(dataStr)
        for imgurl in imglist:
            print imgurl  
            if imgurl[1]!='com':
                imgtype=imgurl[1]
                imgurl =''.join('%s.%s' % (imgurl[0],imgtype))
                #print imgurl
                if imgurl.find('http:')>=0:
                    print "\tdownloading: %s,%s" % (x,imgurl)
                    imgdata=getContent(imgurl,"img")
                    if imgdata!='EOF':
                        outputFile = 'ai/%s.%s.%s' % (current_page.split('/')[-1],x,imgtype)
                        #print x
                        f = open(outputFile,'wb')
                        try:

                            f.write(imgdata)
                        except:
                            print "*****"    
                        f.close()
                        x = x + 1   
           
        
        reg_link=r"""src\s*=\s*"?(http://dailycatdrawings\.tumblr\.com/post/\S+/false)"""
        urlre_link = re.compile(reg_link)  
        linklist=urlre_link.findall(dataStr)
        for link in linklist:
            #print link
            x=baidu_tieba(link,current_page,x)

        reg_nextpage = r"""href\s*=\s*"?(/page/\d+)"""  
        urlre_nextpage = re.compile(reg_nextpage)
        nextpage=urlre_nextpage.findall(dataStr)
        print nextpage
        if nextpage!=[]:
            if nextpage[0] == nextpage[-1] and nextpage[0] != "/page/2":
                print "Finished! :)"
            else:
                x=baidu_tieba(url,nextpage[-1])            
        
        return x
"""
bdurl = str(raw_input(u'URL:\n'))  
begin_page = int(raw_input(u'START PAGE:\n'))  
end_page = int(raw_input(u'END PAGE:\n'))  
"""
bdurl='http://dailycatdrawings.tumblr.com'
start_page=1
end_page=75
baidu_tieba(bdurl) 