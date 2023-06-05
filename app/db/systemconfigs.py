import json
from typing import Any, Union

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.db.models.systemconfig import SystemConfig
from app.utils.object import ObjectUtils
from app.utils.singleton import Singleton
from app.utils.types import SystemConfigKey


class SystemConfigs(metaclass=Singleton):
    # 配置对象
    __SYSTEMCONF: dict = {}
    _db: Session = None

    def __init__(self, _db=SessionLocal()):
        """
        加载配置到内存
        """
        self._db = _db
        for item in SystemConfig.list(self._db):
            if ObjectUtils.is_obj(item.value):
                self.__SYSTEMCONF[item.key] = json.loads(item.value)
            else:
                self.__SYSTEMCONF[item.key] = item.value

    def set(self, key: Union[str, SystemConfigKey], value: Any):
        """
        设置系统设置
        """
        if isinstance(key, SystemConfigKey):
            key = key.value
        # 更新内存
        self.__SYSTEMCONF[key] = value
        # 写入数据库
        if ObjectUtils.is_obj(value):
            if value is not None:
                value = json.dumps(value)
            else:
                value = ''
        conf = SystemConfig.get_by_key(self._db, key)
        if conf:
            conf.update(self._db, {"value": value})
        else:
            conf = SystemConfig(key=key, value=value)
            conf.create(self._db)

    def get(self, key: Union[str, SystemConfigKey] = None):
        """
        获取系统设置
        """
        if isinstance(key, SystemConfigKey):
            key = key.value
        if not key:
            return self.__SYSTEMCONF
        return self.__SYSTEMCONF.get(key)
