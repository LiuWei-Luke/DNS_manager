启动：
    程序入口文件为： main.py

路由：
    主路由:/apis/v1.0/
    路由地址文件为: views.py
使用：
    named_conf:检查服务配置
    zones/check/<zone> 检查给定域名及其配置文件
    named/?oper= 后面跟named服务的操作，start ,stop, status, reload等
    server_status 查看服务状态
    zones/reload/<zone> 重新加载给定域名
    zones/flush/<zone> 刷新域名缓存活这个服务缓存，all代表所有
    zones  方法：post 参数：['zone']，添加给定域名，需要有该域名配置文件
    zones/delete/<zone> 删除域名,这里只是删除服务记录,保留了域名的配置文件
    zones/notify/<zone> 发送notify给指定域名
    download/<filename> 从备份文件夹中下载指定文件
    backup 对域名文件进行备份并打包压缩