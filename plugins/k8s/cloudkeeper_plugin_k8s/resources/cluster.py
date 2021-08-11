from .common import KubernetesResource
from cloudkeeper.baseresources import BaseAccount
from typing import ClassVar
from dataclasses import dataclass


@dataclass(eq=False)
class KubernetesCluster(KubernetesResource, BaseAccount):
    resource_type: ClassVar[str] = "kubernetes_cluster"