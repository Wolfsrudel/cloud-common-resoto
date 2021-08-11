from kubernetes import client
from .common import KubernetesResource
from cloudkeeper.baseresources import (
    BaseResource,
)
from typing import ClassVar
from dataclasses import dataclass


@dataclass(eq=False)
class KubernetesDeployment(KubernetesResource, BaseResource):
    resource_type: ClassVar[str] = "kubernetes_deployment"
    api: ClassVar[object] = client.AppsV1Api
    list_method: ClassVar[str] = "list_deployment_for_all_namespaces"