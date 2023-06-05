from types import FunctionType
from typing import Generator, Optional

from app.core import settings
from app.helper import ModuleHelper
from app.log import logger
from app.utils.singleton import Singleton


class ModuleManager(metaclass=Singleton):
    """
    模块管理器
    """

    # 模块列表
    _modules: dict = {}
    # 运行态模块列表
    _running_modules: dict = {}

    def __init__(self):
        self.load_modules()

    def load_modules(self):
        """
        加载所有模块
        """
        # 扫描模块目录
        modules = ModuleHelper.load(
            "app.modules",
            filter_func=lambda _, obj: hasattr(obj, 'init_module') and hasattr(obj, 'init_setting')
        )
        self._running_modules = {}
        self._modules = {}
        for module in modules:
            module_id = module.__name__
            self._modules[module_id] = module
            # 生成实例
            self._running_modules[module_id] = module()
            self._running_modules[module_id].init_module()
            logger.info(f"Moudle Loaded：{module_id}")

    def get_modules(self, method: str) -> Generator:
        """
        获取模块列表
        """

        def check_method(func: FunctionType) -> bool:
            """
            检查函数是否已实现
            """
            return func.__code__.co_code != b'd\x01S\x00'

        def check_setting(setting: Optional[tuple]) -> bool:
            """
            检查开关是否己打开
            """
            if not setting:
                return True
            switch, value = setting
            if getattr(settings, switch) and value is True:
                return True
            if getattr(settings, switch) == value:
                return True
            return False

        if not self._running_modules:
            return []
        for _, module in self._running_modules.items():
            if hasattr(module, method) \
                    and check_method(getattr(module, method)) \
                    and check_setting(module.init_setting()):
                yield module
