import json
import functools
from typing import Iterable, Dict, Callable

try:
    from flask import Flask, request, render_template, jsonify
except ModuleNotFoundError as E:
    from ..common import ModuleIsNotInstallError
    raise ModuleIsNotInstallError('Flask', 'pip install flask') from E


class NvwaOSFlask(Flask):
    def __init__(self, import_name: str, *args, global_config: Dict, **kwargs):
        """
        NvwaOS-Flask 拓展对象

        :param import_name: the name of the application package.
        :param global_config: 全局变量配置
                              - PROJECT_NAME: 项目名称
                              - LOCALS_FUNCTION: 本地环境变量构造函数
                              - INTERFACE_PARAM_ANALYSIS: 接口参数解析函数
        :param static_url_path: can be used to specify a different path for the
                            static files on the web.  Defaults to the name
                            of the `static_folder` folder.
        :param static_folder: the folder with static files that should be served
                              at `static_url_path`.  Defaults to the ``'static'``
                              folder in the root path of the application.
        :param static_host: the host to use when adding the static route.
            Defaults to None. Required when using ``host_matching=True``
            with a ``static_folder`` configured.
        :param host_matching: set ``url_map.host_matching`` attribute.
            Defaults to False.
        :param subdomain_matching: consider the subdomain relative to
            :data:`SERVER_NAME` when matching routes. Defaults to False.
        :param template_folder: the folder that contains the templates that should
                                be used by the application.  Defaults to
                                ``'templates'`` folder in the root path of the
                                application.
        :param instance_path: An alternative instance path for the application.
                              By default the folder ``'instance'`` next to the
                              package or module is assumed to be the instance
                              path.
        :param instance_relative_config: if set to ``True`` relative filenames
                                         for loading the config are assumed to
                                         be relative to the instance path instead
                                         of the application root.
        :param root_path: Flask by default will automatically calculate the path
                          to the root of the application.  In certain situations
                          this cannot be achieved (for instance if the package
                          is a Python 3 namespace package) and needs to be
                          manually defined.
        """
        super().__init__(import_name, *args, **kwargs)
        self.GLOBAL_CONFIG: dict = global_config

    def page(self, route: str = None, template: str = None, methods: Iterable[str] = None, route_options: Dict = None):
        """
        装饰器：页面

        :param route: 请求地址，默认为 <被修饰的函数名>
        :param template: 模板路径，默认为 <被修饰的函数同名的模板>
        :param methods: HTTP 请求的方式
        :param route_options: 路由的其他参数
        """
        local_func = self.GLOBAL_CONFIG.get('LOCALS_FUNCTION', lambda local: local)

        def decorator(func):
            # 构造当前路由环境变量
            # local_func:
            #   - local: 默认 local 变量
            local = local_func({
                'url': route if route else f'/{func.__name__}',
                'method': func.__name__,
                'template': template if template else f'{func.__name__}.html'
            })

            @self.route(local['url'], methods=methods, **(route_options if route_options is not None else {}))
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                result_type = type(result)
                if result_type is not dict:
                    result = {'result': result}
                params = {
                    'debug_mode': self.debug,
                    'local': local,
                    'global': self.GLOBAL_CONFIG
                }
                return render_template(local['template'], **params, **result)
            return wrapper
        return decorator

    def interface(self, route: str = None, methods: Iterable[str] = ('POST',), **required: Callable[[dict], None]):
        """
        装饰器：接口

        :param route: 请求地址，默认为 <被修饰的函数名>
        :param methods: HTTP 请求的方式，默认为 POST
        :param required: 必要参数，用于参数校验
        """

        interface_param_analysis = self.GLOBAL_CONFIG.get('INTERFACE_PARAM_ANALYSIS', jsonify)

        # 加载参数
        def load_parameters() -> dict:
            if request.method == 'GET':
                parameters = dict(request.args)
            elif request.method == 'POST':
                json_str = request.get_data().decode()
                parameters = json.loads(json_str) if json_str else dict()
            else:
                parameters = dict()
            # 必要参数校验
            if required:
                for name, p_type in required.items():
                    if name not in parameters:
                        raise RuntimeError('必须指定 {} 参数'.format(name))
                    else:
                        # 转换参数类型
                        parameters[name] = p_type(parameters[name])
            return parameters

        def decorator(func):
            @self.route(route if route else f'/{func.__name__}', methods=methods)
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    # 获取参数
                    parameters = load_parameters()
                    kwargs.update(parameters)
                    result = func(*args, **kwargs)
                    return interface_param_analysis(result)
                except RuntimeError as e:
                    return interface_param_analysis(e)
            return wrapper
        return decorator
