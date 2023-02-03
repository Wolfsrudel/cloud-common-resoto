from datetime import datetime
from typing import ClassVar, Dict, Optional, Type, List

from attr import define, field as attrs_field

from resoto_plugin_aws.aws_client import AwsClient
from resoto_plugin_aws.resource.base import AwsApiSpec, GraphBuilder, AwsResource
from resoto_plugin_aws.resource.kms import AwsKmsKey
from resoto_plugin_aws.resource.s3 import AwsS3Bucket
from resoto_plugin_aws.resource.sns import AwsSnsTopic
from resoto_plugin_aws.utils import ToDict
from resotolib.types import Json
from resotolib.baseresources import ModelReference
from resotolib.json import from_json
from resotolib.json_bender import Bender, S, bend, ForallBend, EmptyToNone, F


@define(eq=False, slots=False)
class AwsCloudTrailAdvancedFieldSelector:
    kind: ClassVar[str] = "aws_cloud_trail_advanced_field_selector"
    mapping: ClassVar[Dict[str, Bender]] = {
        "field": S("Field"),
        "equals": S("Equals"),
        "starts_with": S("StartsWith"),
        "ends_with": S("EndsWith"),
        "not_equals": S("NotEquals"),
        "not_starts_with": S("NotStartsWith"),
        "not_ends_with": S("NotEndsWith"),
    }
    equals: Optional[List[str]] = attrs_field(default=None)
    starts_with: Optional[List[str]] = attrs_field(default=None)
    ends_with: Optional[List[str]] = attrs_field(default=None)
    not_equals: Optional[List[str]] = attrs_field(default=None)
    not_starts_with: Optional[List[str]] = attrs_field(default=None)
    not_ends_with: Optional[List[str]] = attrs_field(default=None)


@define(eq=False, slots=False)
class AwsCloudTrailEventSelector:
    kind: ClassVar[str] = "aws_cloud_trail_event_selector"
    mapping: ClassVar[Dict[str, Bender]] = {
        "name": S("Name"),
        "field_selectors": S("FieldSelectors", default=[])
        >> ForallBend(AwsCloudTrailAdvancedFieldSelector.mapping)
        >> F(lambda x: {a["field"]: a for a in x}),
    }
    name: Optional[str] = attrs_field(default=None)
    field_selectors: Optional[Dict[str, AwsCloudTrailAdvancedFieldSelector]] = attrs_field(default=None)


@define(eq=False, slots=False)
class AwsCloudTrailStatus:
    kind: ClassVar[str] = "aws_cloud_trail_status"
    mapping: ClassVar[Dict[str, Bender]] = {
        "is_logging": S("IsLogging"),
        "latest_delivery_error": S("LatestDeliveryError"),
        "latest_notification_error": S("LatestNotificationError"),
        "latest_delivery_time": S("LatestDeliveryTime") >> EmptyToNone,
        "latest_notification_time": S("LatestNotificationTime") >> EmptyToNone,
        "start_logging_time": S("StartLoggingTime") >> EmptyToNone,
        "stop_logging_time": S("StopLoggingTime") >> EmptyToNone,
        "latest_cloud_watch_logs_delivery_error": S("LatestCloudWatchLogsDeliveryError"),
        "latest_cloud_watch_logs_delivery_time": S("LatestCloudWatchLogsDeliveryTime"),
        "latest_digest_delivery_time": S("LatestDigestDeliveryTime") >> EmptyToNone,
        "latest_digest_delivery_error": S("LatestDigestDeliveryError"),
        "latest_delivery_attempt_time": S("LatestDeliveryAttemptTime") >> EmptyToNone,
        "latest_notification_attempt_time": S("LatestNotificationAttemptTime") >> EmptyToNone,
        "latest_notification_attempt_succeeded": S("LatestNotificationAttemptSucceeded") >> EmptyToNone,
        "latest_delivery_attempt_succeeded": S("LatestDeliveryAttemptSucceeded") >> EmptyToNone,
        "time_logging_started": S("TimeLoggingStarted") >> EmptyToNone,
        "time_logging_stopped": S("TimeLoggingStopped") >> EmptyToNone,
    }
    is_logging: Optional[bool] = attrs_field(default=None)
    latest_delivery_error: Optional[str] = attrs_field(default=None)
    latest_notification_error: Optional[str] = attrs_field(default=None)
    latest_delivery_time: Optional[datetime] = attrs_field(default=None)
    latest_notification_time: Optional[datetime] = attrs_field(default=None)
    start_logging_time: Optional[datetime] = attrs_field(default=None)
    stop_logging_time: Optional[datetime] = attrs_field(default=None)
    latest_cloud_watch_logs_delivery_error: Optional[str] = attrs_field(default=None)
    latest_cloud_watch_logs_delivery_time: Optional[datetime] = attrs_field(default=None)
    latest_digest_delivery_time: Optional[datetime] = attrs_field(default=None)
    latest_digest_delivery_error: Optional[str] = attrs_field(default=None)
    latest_delivery_attempt_time: Optional[datetime] = attrs_field(default=None)
    latest_notification_attempt_time: Optional[datetime] = attrs_field(default=None)
    latest_notification_attempt_succeeded: Optional[datetime] = attrs_field(default=None)
    latest_delivery_attempt_succeeded: Optional[datetime] = attrs_field(default=None)
    time_logging_started: Optional[datetime] = attrs_field(default=None)
    time_logging_stopped: Optional[datetime] = attrs_field(default=None)


@define(eq=False, slots=False)
class AwsCloudTrail(AwsResource):
    kind: ClassVar[str] = "aws_cloud_trail"
    api_spec: ClassVar[AwsApiSpec] = AwsApiSpec("cloudtrail", "list-trails", "Trails")
    mapping: ClassVar[Dict[str, Bender]] = {
        "id": S("Name"),
        "name": S("Name"),
        "trail_s3_bucket_name": S("S3BucketName"),
        "trail_s3_key_prefix": S("S3KeyPrefix"),
        "trail_sns_topic_name": S("SnsTopicName"),
        "trail_sns_topic_arn": S("SnsTopicARN"),
        "trail_include_global_service_events": S("IncludeGlobalServiceEvents"),
        "trail_is_multi_region_trail": S("IsMultiRegionTrail"),
        "trail_home_region": S("HomeRegion"),
        "arn": S("TrailARN"),
        "trail_log_file_validation_enabled": S("LogFileValidationEnabled"),
        "trail_cloud_watch_logs_log_group_arn": S("CloudWatchLogsLogGroupArn"),
        "trail_cloud_watch_logs_role_arn": S("CloudWatchLogsRoleArn"),
        "trail_kms_key_id": S("KmsKeyId"),
        "trail_has_custom_event_selectors": S("HasCustomEventSelectors"),
        "trail_has_insight_selectors": S("HasInsightSelectors"),
        "trail_is_organization_trail": S("IsOrganizationTrail"),
    }
    reference_kinds: ClassVar[ModelReference] = {
        "successors": {"default": ["aws_s3_bucket", "aws_sns_topic", "aws_kms_key"]},
    }
    trail_s3_bucket_name: Optional[str] = attrs_field(default=None)
    trail_s3_key_prefix: Optional[str] = attrs_field(default=None)
    trail_sns_topic_name: Optional[str] = attrs_field(default=None)
    trail_sns_topic_arn: Optional[str] = attrs_field(default=None)
    trail_include_global_service_events: Optional[bool] = attrs_field(default=None)
    trail_is_multi_region_trail: Optional[bool] = attrs_field(default=None)
    trail_home_region: Optional[str] = attrs_field(default=None)
    arn: Optional[str] = attrs_field(default=None)
    trail_log_file_validation_enabled: Optional[bool] = attrs_field(default=None)
    trail_cloud_watch_logs_log_group_arn: Optional[str] = attrs_field(default=None)
    trail_cloud_watch_logs_role_arn: Optional[str] = attrs_field(default=None)
    trail_kms_key_id: Optional[str] = attrs_field(default=None)
    trail_has_custom_event_selectors: Optional[bool] = attrs_field(default=None)
    trail_has_insight_selectors: Optional[bool] = attrs_field(default=None)
    trail_is_organization_trail: Optional[bool] = attrs_field(default=None)
    trail_status: Optional[AwsCloudTrailStatus] = attrs_field(default=None)
    trail_event_selectors: Optional[List[AwsCloudTrailEventSelector]] = attrs_field(default=None)
    trail_insight_selectors: Optional[List[str]] = attrs_field(default=None)

    @classmethod
    def called_collect_apis(cls) -> List[AwsApiSpec]:
        return [
            AwsApiSpec("cloudtrail", "list-trails"),
            AwsApiSpec("cloudtrail", "get-trail"),
            AwsApiSpec("cloudtrail", "get-trail-status"),
            AwsApiSpec("cloudtrail", "list-tags"),
            AwsApiSpec("cloudtrail", "get-event-selectors"),
            AwsApiSpec("cloudtrail", "get-insight-selectors"),
        ]

    @classmethod
    def collect(cls: Type[AwsResource], json: List[Json], builder: GraphBuilder) -> None:
        def collect_trail(trail_arn: str) -> None:
            if trail_raw := builder.client.get("cloudtrail", "get-trail", "Trail", Name=trail_arn):
                instance = AwsCloudTrail.from_api(trail_raw)
                builder.add_node(instance, js)
                collect_status(instance)
                collect_tags(instance)
                if instance.trail_has_custom_event_selectors:
                    collect_event_selectors(instance)
                if instance.trail_has_insight_selectors:
                    collect_insight_selectors(instance)

        def collect_event_selectors(trail: AwsCloudTrail) -> None:
            trail.trail_event_selectors = []
            for item in builder.client.list(
                "cloudtrail", "get-event-selectors", "AdvancedEventSelectors", TrailName=trail.arn
            ):
                mapped = bend(AwsCloudTrailEventSelector.mapping, item)
                trail.trail_event_selectors.append(from_json(mapped, AwsCloudTrailEventSelector))

        def collect_insight_selectors(trail: AwsCloudTrail) -> None:
            trail.trail_insight_selectors = []
            for item in builder.client.list(
                "cloudtrail",
                "get-insight-selectors",
                "InsightSelectors",
                TrailName=trail.arn,
                expected_errors=["InsightNotEnabledException"],
            ):
                trail.trail_insight_selectors.append(item["InsightType"])

        def collect_status(trail: AwsCloudTrail) -> None:
            status_raw = builder.client.get("cloudtrail", "get-trail-status", Name=trail.arn)
            mapped = bend(AwsCloudTrailStatus.mapping, status_raw)
            status = from_json(mapped, AwsCloudTrailStatus)
            trail.trail_status = status
            trail.ctime = status.start_logging_time
            trail.mtime = status.latest_delivery_time

        def collect_tags(trail: AwsCloudTrail) -> None:
            for tr in builder.client.list("cloudtrail", "list-tags", "ResourceTagList", ResourceIdList=[trail.arn]):
                trail.tags = bend(S("TagsList", default=[]) >> ToDict(), tr)

        for js in json:
            if js["HomeRegion"] == builder.region.name:
                # list trails will return trails for all regions
                # filter here, to get the assignment to the correct region
                builder.submit_work(collect_trail, js["TrailARN"])

    def connect_in_graph(self, builder: GraphBuilder, source: Json) -> None:
        if s3 := self.trail_s3_bucket_name:
            builder.add_edge(self, clazz=AwsS3Bucket, name=s3)
        if sns := self.trail_sns_topic_arn:
            builder.add_edge(self, clazz=AwsSnsTopic, arn=sns)
        if kms := self.trail_kms_key_id:
            builder.add_edge(self, clazz=AwsKmsKey, id=AwsKmsKey.normalise_id(kms))
        # TODO: add link to cloudwatch log group

    def update_resource_tag(self, client: AwsClient, key: str, value: str) -> bool:
        client.call("cloudtrail", "add-tags", ResourceId=self.arn, TagsList=[{"Key": key, "Value": value}])
        return True

    def delete_resource_tag(self, client: AwsClient, key: str) -> bool:
        client.call("cloudtrail", "remove-tags", ResourceId=self.arn, TagsList=[{"Key": key}])
        return True

    def delete_resource(self, client: AwsClient) -> bool:
        client.call("cloudtrail", "delete-trail", Name=self.arn)
        return True

    @classmethod
    def called_mutator_apis(cls) -> List[AwsApiSpec]:
        return [
            AwsApiSpec("cloudtrail", "add-tags"),
            AwsApiSpec("cloudtrail", "remove-tags"),
            AwsApiSpec("cloudtrail", "delete-trail"),
        ]


resources: List[Type[AwsResource]] = [AwsCloudTrail]