import socket
import re
import select

def manager(client_socket,recv_mes):
    '''处理用户数据'''
    
        
    #请求响应 进行切片,获取url
    
    request_header=recv_mes.splitlines()[0]
    #按行切片
    #print(request_header)
                
    ret=re.match(r'[^/]+(/[^ ]*)',request_header)
    if ret :
        request_http=ret.group(1)   
        print(request_http)
        
        if request_http == '/':
            request_http = '/index.html'
            
            
    #如果访问对是/index, 就给相应的html --->不可取，因为还有很多被动请求
    #if request_http == '/index.html':
                    
            

        #body 为打开html文件存储对内容,可以二进制方式打开
        #with open('./index.html','rb') as f:
        #   context= f.read()
    try:
        f=open('.'+request_http,'rb')
        #context=f.read()                         
        #f.close()  

    except Exception as ret:
        header = "HTTP/1.1 404 NOT FOUND\r\n"
        #body 为打开html文件存储对内容,可以二进制方式打开
        
        respon = header +'\r\n'
        respon += "----not found--"         

        client_socket.send(respon.encode('utf-8'))

        #client_socket .close()
        #不能关闭套接字，
                
    else:
        context = f.read()                         
        f.close()   

        # retu
        #分开给 浏览器，发送信息a
        header = "HTTP/1.1 200 OK \r\n"
        respon = header +'\r\n'
        
        client_socket.send(respon.encode('utf-8'))
        client_socket.send(context)
    

            
    client_socket.close()
        

#tcp服务器
def main():
    #创建套接字
    tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #绑定端口，里面是一个元组，‘’空字段表上本机，port
    tcp_socket.bind(('',8099))
    ##监听状态, 监听字节长度
    tcp_socket.listen(128)

    #引入 epoll 机制m, 创建epoll 对象
    epl = select.epoll()

    client_socket_dict=dict()

    #注意流程#把监听套接字，注册
    epl.register(tcp_socket.fileno(),select.EPOLLIN)

    while True:


    #套接字有链接信息，就做处理,  
        man_mes=epl.poll()        #返回对是一个元组， 一个是套接字，一个是事件

        for  mange_target_socket,target_event in  man_mes:
            if  mange_target_socket == tcp_socket.fileno():   #fileno方法是对应文件描述符号
                #事件响应是目标对socket


                    # accept(),接受到的连接信息，是元组，通过元组拆包。一个是给客户端的套接字   #一个是记录客户端对地址。
                #说明有客户端链接了
                client_socket,client_add = tcp_socket.accept()
                #将客户端socket,一样注册epoll
                epl.register(client_socket.fileno(),select.EPOLLIN)

                client_socket_dict[client_socket.fileno()] = client_socket

            
            elif target_event == select.EPOLLIN:
                #客户端套接字 已经链接进来了 EPOLLIN
                #然后对具体对客户进行服务 #服务套接字接受信息， ，
                recv_mes=client_socket_dict[mange_target_socket].recv(1024).decode('utf-8')

                if recv_mes:
                    
                    manager(client_socket_dict[mange_target_socket],recv_mes)
        
                client_socket_dict[mange_target_socket].close()
                #注销epoll 
                epl.unregister(mange_target_socket)
                #并从字典中，移除
                del client_socket_dict[mange_target_socket]

    tcp_socket.close()          

if __name__ == "__main__":
    main()
