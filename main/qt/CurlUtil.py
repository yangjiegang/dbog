import pycurl
import io


class CurlUtil(object):
    @staticmethod
    # ------------------------自动处理cookile的函数----------------------------------#
    def init_curl():
        '''初始化一个pycurl对象，
        尽管urllib2也支持 cookie 但是在登录cas系统时总是失败，并且没有搞清楚失败的原因。
        这里采用pycurl主要是因为pycurl设置了cookie后，可以正常登录Cas系统
        '''
        c = pycurl.Curl()
        c.setopt(pycurl.COOKIEFILE, "cookie_file_name")  # 把cookie保存在该文件中
        c.setopt(pycurl.COOKIEJAR, "cookie_file_name")
        c.setopt(pycurl.FOLLOWLOCATION, 1)  # 允许跟踪来源
        c.setopt(pycurl.MAXREDIRS, 5)
        # 设置代理 如果有需要请去掉注释，并设置合适的参数
        # c.setopt(pycurl.PROXY, ‘http://11.11.11.11:8080′)
        # c.setopt(pycurl.PROXYUSERPWD, ‘aaa:aaa’)
        return c

    @staticmethod
    # -----------------------------------get函数-----------------------------------#
    def get_data(self, curl, url):
        '''获得url指定的资源，这里采用了HTTP的GET方法
        '''
        head = ['Accept:*/*',
                'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0']
        buf = io.StringIO()
        curl.setopt(pycurl.WRITEFUNCTION, buf.write)
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.HTTPHEADER, head)
        curl.perform()
        the_page = buf.getvalue()
        buf.close()
        return the_page

    @staticmethod
    # -----------------------------------post函数-----------------------------------#
    def post_data(curl, url, data):
        '''提交数据到url，这里使用了HTTP的POST方法
        备注，这里提交的数据为json数据，
        如果需要修改数据类型，请修改head中的数据类型声明
        '''
        head = ['Accept:*/*',
                'Content-Type:application/xml',
                'render:json',
                'clientType:json',
                'Accept-Charset:GBK,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding:gzip,deflate,sdch',
                'Accept-Language:zh-CN,zh;q=0.8',
                'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0']
        buf = io.BytesIO()
        curl.setopt(pycurl.WRITEFUNCTION, buf.write)
        curl.setopt(pycurl.POSTFIELDS, data)
        curl.setopt(pycurl.URL, url)
        # curl.setopt(pycurl.HTTPHEADER, head)
        curl.perform()
        the_page = buf.getvalue()
        # print the_page
        buf.close()
        return the_page
