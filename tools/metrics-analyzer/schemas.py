from pyspark.sql.types import StructType, StructField, StringType, TimestampType, LongType, DoubleType

# Define the schema for the incoming Kafka data
schema_disk = StructType([
    StructField("name", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("fields",
                StructType([
                    StructField("free", LongType()),
                    StructField("total", LongType()),
                    StructField("used", LongType()),
                    StructField("used_percent", DoubleType())
                ])
                ),
    StructField("tags",
                StructType([
                    StructField("device", StringType()),
                    StructField("fstype", StringType()),
                    StructField("host", StringType()),
                    StructField("mode", StringType()),
                    StructField("path", StringType())
                ])
                )
])

schema_diskio = StructType([
    StructField("name", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("fields",
                StructType([
                    StructField("io_time", LongType()),
                    StructField("read_time", LongType()),
                    StructField("reads", LongType()),
                    StructField("write_time", LongType()),
                    StructField("writes", LongType())
                ])
                ),
    StructField("tags",
                StructType([
                    StructField("host", StringType()),
                    StructField("name", StringType())
                ])
                )
])

schema_mem = StructType([
    StructField("name", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("fields",
                StructType([
                    StructField("available", LongType()),
                    StructField("free", LongType()),
                    StructField("total", LongType()),
                    StructField("used_percent", DoubleType())
                ])
                ),
    StructField("tags",
                StructType([
                    StructField("host", StringType())
                ])
                )
])

schema_cpu = StructType([
    StructField("name", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("fields",
                StructType([
                    StructField("usage_guest", DoubleType()),
                    StructField("usage_guest_nice", DoubleType()),
                    StructField("usage_idle", DoubleType()),
                    StructField("usage_iowait", DoubleType()),
                    StructField("usage_irq", DoubleType()),
                    StructField("usage_nice", DoubleType()),
                    StructField("usage_softirq", DoubleType()),
                    StructField("usage_steal", DoubleType()),
                    StructField("usage_system", DoubleType()),
                    StructField("usage_user", DoubleType())
                ])
                ),
    StructField("tags",
                StructType([
                    StructField("host", StringType()),
                    StructField("cpu", StringType())
                ])
                )
])

schema_net = StructType([
    StructField("name", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("fields",
                StructType([
                    StructField("bytes_recv", LongType()),
                    StructField("bytes_sent", LongType()),
                    StructField("drop_in", LongType()),
                    StructField("drop_out", LongType()),
                    StructField("err_in", LongType()),
                    StructField("err_out", LongType()),
                    StructField("packets_recv", LongType()),
                    StructField("packets_sent", LongType())
                ])
                ),
    StructField("tags",
                StructType([
                    StructField("host", StringType()),
                    StructField("interface", StringType())
                ])
                )
])

schema_system = StructType([
    StructField("name", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("fields",
                StructType([
                    StructField("load1", DoubleType()),
                    StructField("load5", DoubleType()),
                    StructField("load15", DoubleType())
                ])
                ),
    StructField("tags",
                StructType([
                    StructField("host", StringType())
                ])
                )
])

schema_k8s_pod_cont = StructType([
    StructField("name", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("fields",
                StructType([
                    StructField("cpu_usage_core_nanoseconds", LongType()),
                    StructField("cpu_usage_nanocores", LongType()),
                    StructField("logsfs_available_bytes", LongType()),
                    StructField("logsfs_capacity_bytes", LongType()),
                    StructField("logsfs_used_bytes", LongType()),
                    StructField("memory_major_page_faults", LongType()),
                    StructField("memory_page_faults", LongType()),
                    StructField("memory_rss_bytes", LongType()),
                    StructField("memory_usage_bytes", LongType()),
                    StructField("memory_working_set_bytes", LongType()),
                    StructField("rootfs_available_bytes", LongType()),
                    StructField("rootfs_capacity_bytes", LongType()),
                    StructField("rootfs_used_bytes", LongType())
                ])
                ),
    StructField("tags",
                StructType([
                    StructField("host", StringType()),
                    StructField("namespace", StringType()),
                    StructField("pod_name", StringType()),
                    StructField("container_name", StringType())
                ])
                )
])

schema_k8s_pod_vol = StructType([
    StructField("name", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("fields",
                StructType([
                    StructField("available_bytes", LongType()),
                    StructField("capacity_bytes", LongType()),
                    StructField("used_bytes", LongType())
                ])
                ),
    StructField("tags",
                StructType([
                    StructField("host", StringType()),
                    StructField("namespace", StringType()),
                    StructField("pod_name", StringType()),
                    StructField("volume_name", StringType())
                ])
                )
])

schema_k8s_pod_net = StructType([
    StructField("name", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("fields",
                StructType([
                    StructField("rx_bytes", LongType()),
                    StructField("rx_errors", LongType()),
                    StructField("tx_bytes", LongType()),
                    StructField("tx_errors", LongType()),
                ])
                ),
    StructField("tags",
                StructType([
                    StructField("host", StringType()),
                    StructField("namespace", StringType()),
                    StructField("pod_name", StringType())
                ])
                )
])
