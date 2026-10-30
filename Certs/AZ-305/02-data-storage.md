# Domain 2: Design data storage solutions (20–25%)

Decision guide to keep open: https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/data-store-overview

## 2.1 Design data storage solutions for relational data

- [ ] Recommend a solution for storing relational data
  - Know how to: Azure SQL Database vs Managed Instance vs SQL on VM; Azure Database for PostgreSQL/MySQL flexible server; Cosmos DB for PostgreSQL; feature-parity triggers (SQL Agent, cross-db queries, CLR) that force MI or VM.
  - Read: Azure SQL options compared https://learn.microsoft.com/en-us/azure/azure-sql/azure-sql-iaas-vs-paas-what-is-overview · PostgreSQL flexible server https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/overview · SQL Managed Instance features https://learn.microsoft.com/en-us/azure/azure-sql/managed-instance/sql-managed-instance-paas-overview
- [ ] Recommend a database service tier and compute tier
  - Know how to: DTU vs vCore, General Purpose vs Business Critical vs Hyperscale, serverless auto-pause, provisioned vs serverless compute, Hyperscale named replicas, elastic pools.
  - Read: vCore purchasing model https://learn.microsoft.com/en-us/azure/azure-sql/database/service-tiers-vcore · Hyperscale https://learn.microsoft.com/en-us/azure/azure-sql/database/service-tier-hyperscale · Serverless https://learn.microsoft.com/en-us/azure/azure-sql/database/serverless-tier-overview · Elastic pools https://learn.microsoft.com/en-us/azure/azure-sql/database/elastic-pool-overview
- [ ] Recommend a solution for database scalability
  - Know how to: vertical scale, read scale-out (Business Critical/Hyperscale read replicas), sharding with elastic database tools, Hyperscale for >4 TB, PostgreSQL read replicas, Cosmos DB for horizontal scale.
  - Read: Read scale-out https://learn.microsoft.com/en-us/azure/azure-sql/database/read-scale-out · Elastic database tools (sharding) https://learn.microsoft.com/en-us/azure/azure-sql/database/elastic-scale-introduction · Scale resources https://learn.microsoft.com/en-us/azure/azure-sql/database/scale-resources
- [ ] Recommend a solution for data protection
  - Know how to: TDE with customer-managed keys, Always Encrypted (with secure enclaves), dynamic data masking, row-level security, Defender for SQL, ledger tables, auditing, Purview classification.
  - Read: SQL security overview https://learn.microsoft.com/en-us/azure/azure-sql/database/security-overview · Always Encrypted https://learn.microsoft.com/en-us/sql/relational-databases/security/encryption/always-encrypted-database-engine · Ledger https://learn.microsoft.com/en-us/sql/relational-databases/security/ledger/ledger-overview · Dynamic data masking https://learn.microsoft.com/en-us/azure/azure-sql/database/dynamic-data-masking-overview

## 2.2 Design data storage solutions for semi-structured and unstructured data

- [ ] Recommend a solution for storing semi-structured data
  - Know how to: Cosmos DB APIs (NoSQL, MongoDB, Cassandra, Gremlin, Table), consistency levels, partition key design, RU provisioned vs serverless vs autoscale; Table storage vs Cosmos Table API; Azure Cache for Redis / Managed Redis.
  - Read: Cosmos DB overview https://learn.microsoft.com/en-us/azure/cosmos-db/introduction · Choose an API https://learn.microsoft.com/en-us/azure/cosmos-db/choose-api · Consistency levels https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels · Partitioning https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning-overview
- [ ] Recommend a solution for storing unstructured data
  - Know how to: Blob (block/append/page), Data Lake Storage Gen2 (hierarchical namespace), Azure Files (SMB/NFS, premium), Azure NetApp Files, Managed Disks types, Elastic SAN, Azure Managed Lustre for HPC.
  - Read: Storage account overview https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview · Data Lake Storage Gen2 https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction · Azure Files planning https://learn.microsoft.com/en-us/azure/storage/files/storage-files-planning · Azure NetApp Files https://learn.microsoft.com/en-us/azure/azure-netapp-files/azure-netapp-files-introduction
- [ ] Recommend a data storage solution to balance features, performance, and costs
  - Know how to: access tiers (hot, cool, cold, archive) and rehydration, lifecycle management policies, premium block blob for low latency, reserved capacity, redundancy cost (LRS→GZRS), disk performance tiers and bursting.
  - Read: Access tiers https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview · Lifecycle management https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-overview · Managed disk types https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types · Storage reserved capacity https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-reserved-capacity
- [ ] Recommend a data solution for protection and durability
  - Know how to: redundancy options (LRS, ZRS, GRS, GZRS, RA-*), soft delete (blob, container, share), versioning, point-in-time restore, immutable storage (WORM, legal hold), Azure Backup for blobs and files, object replication.
  - Read: Storage redundancy https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy · Data protection overview https://learn.microsoft.com/en-us/azure/storage/blobs/data-protection-overview · Immutable storage https://learn.microsoft.com/en-us/azure/storage/blobs/immutable-storage-overview · Object replication https://learn.microsoft.com/en-us/azure/storage/blobs/object-replication-overview

## 2.3 Design data integration

- [ ] Recommend a solution for data integration
  - Know how to: Data Factory vs Synapse pipelines vs Fabric Data Factory; integration runtimes (Azure, self-hosted, SSIS); Event Hubs / Stream Analytics for streaming; Logic Apps for app integration; Data Share.
  - Read: Data Factory overview https://learn.microsoft.com/en-us/azure/data-factory/introduction · Integration runtime https://learn.microsoft.com/en-us/azure/data-factory/concepts-integration-runtime · Fabric Data Factory https://learn.microsoft.com/en-us/fabric/data-factory/data-factory-overview · Stream Analytics https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-introduction
- [ ] Recommend a solution for data analysis
  - Know how to: Microsoft Fabric (OneLake, lakehouse, warehouse) vs Synapse Analytics vs Databricks; Azure Data Explorer for telemetry; Power BI; Analytics end-to-end reference architecture.
  - Read: What is Fabric https://learn.microsoft.com/en-us/fabric/fundamentals/microsoft-fabric-overview · Azure Databricks https://learn.microsoft.com/en-us/azure/databricks/introduction/ · Data Explorer https://learn.microsoft.com/en-us/azure/data-explorer/data-explorer-overview · Analytics architecture design https://learn.microsoft.com/en-us/azure/architecture/solution-ideas/articles/analytics-start-here
