# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from typing import Any

from airflow.decorators.base import TaskDecorator
from airflow.decorators.branch_python import branch_task
from airflow.decorators.external_python import external_python_task
from airflow.decorators.python import python_task
from airflow.decorators.python_virtualenv import virtualenv_task
from airflow.decorators.task_group import task_group
from airflow.models.dag import dag
from airflow.providers_manager import ProvidersManager

# Please keep this in sync with the .pyi's __all__.
__all__ = [
    "TaskDecorator",
    "TaskDecoratorCollection",
    "dag",
    "task",
    "task_group",
    "python_task",
    "virtualenv_task",
    "external_python_task",
    "branch_task",
]


class TaskDecoratorCollection:
    """Implementation to provide the ``@task`` syntax."""

    python = staticmethod(python_task)
    virtualenv = staticmethod(virtualenv_task)
    external_python = staticmethod(external_python_task)
    branch = staticmethod(branch_task)

    __call__: Any = python  # Alias '@task' to '@task.python'.

    def __getattr__(self, name: str) -> TaskDecorator:
        """Dynamically get provider-registered task decorators, e.g. ``@task.docker``."""
        if name.startswith("__"):
            raise AttributeError(f"{type(self).__name__} has no attribute {name!r}")
        decorators = ProvidersManager().taskflow_decorators
        if name not in decorators:
            raise AttributeError(f"task decorator {name!r} not found")
        return decorators[name]


task = TaskDecoratorCollection()
