# Domain 3: Design business continuity solutions (15–20%)

Keep open: Well-Architected reliability pillar https://learn.microsoft.com/en-us/azure/well-architected/reliability/ and the business continuity design area https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/management-business-continuity-disaster-recovery

## 3.1 Design solutions for backup and disaster recovery

- [ ] Recommend a recovery solution for Azure and hybrid workloads that meets recovery objectives
  - Know how to: map RTO/RPO to active-active, active-passive (hot/warm/cold), backup-restore; Site Recovery for VMs (Azure-to-Azure, VMware/Hyper-V/physical to Azure), recovery plans, test failover; availability zones vs paired regions vs non-paired.
  - Read: Site Recovery overview https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-overview · Multi-region design https://learn.microsoft.com/en-us/azure/well-architected/reliability/regions-availability-zones · Azure paired regions https://learn.microsoft.com/en-us/azure/reliability/cross-region-replication-azure · Reliability guides per service https://learn.microsoft.com/en-us/azure/reliability/overview-reliability-guidance
- [ ] Recommend a backup and recovery solution for compute
  - Know how to: Azure Backup for VMs (policies, enhanced policy for zonal/trusted launch, instant restore, cross-region restore, soft delete, vault redundancy), Backup center / Business Continuity Center, AKS backup, Azure VMware Solution backup.
  - Read: Azure Backup overview https://learn.microsoft.com/en-us/azure/backup/backup-overview · VM backup https://learn.microsoft.com/en-us/azure/backup/backup-azure-vms-introduction · Business Continuity Center https://learn.microsoft.com/en-us/azure/business-continuity-center/business-continuity-center-overview · AKS backup https://learn.microsoft.com/en-us/azure/backup/azure-kubernetes-service-backup-overview
- [ ] Recommend a backup and recovery solution for databases
  - Know how to: Azure SQL automated backups, PITR and LTR, backup storage redundancy; SQL on VM with Azure Backup; Cosmos DB periodic vs continuous backup; PostgreSQL/MySQL flexible server backups and geo-restore.
  - Read: SQL automated backups https://learn.microsoft.com/en-us/azure/azure-sql/database/automated-backups-overview · LTR https://learn.microsoft.com/en-us/azure/azure-sql/database/long-term-retention-overview · Cosmos DB backup https://learn.microsoft.com/en-us/azure/cosmos-db/online-backup-and-restore · SQL Server in VM backup https://learn.microsoft.com/en-us/azure/backup/backup-azure-sql-database
- [ ] Recommend a backup and recovery solution for unstructured data
  - Know how to: blob operational backup vs vaulted backup, Azure Files share snapshots and Backup, soft delete/versioning as first line, Data Lake protection, NetApp snapshots and cross-region replication.
  - Read: Blob backup https://learn.microsoft.com/en-us/azure/backup/blob-backup-overview · Azure Files backup https://learn.microsoft.com/en-us/azure/backup/azure-file-share-backup-overview · Storage disaster recovery and failover https://learn.microsoft.com/en-us/azure/storage/common/storage-disaster-recovery-guidance

## 3.2 Design for high availability

- [ ] Recommend a high availability solution for compute
  - Know how to: availability sets vs zones vs VM scale sets (flexible orchestration, zone balancing), SLA maths by deployment shape, App Service zone redundancy, AKS multi-zone node pools, Container Apps zone redundancy, Functions premium.
  - Read: VM availability options https://learn.microsoft.com/en-us/azure/virtual-machines/availability · Scale sets zones https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-use-availability-zones · App Service reliability https://learn.microsoft.com/en-us/azure/reliability/reliability-app-service · AKS reliability https://learn.microsoft.com/en-us/azure/reliability/reliability-aks · SLA summary https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services
- [ ] Recommend a high availability solution for relational data
  - Know how to: Azure SQL zone redundancy per tier, failover groups vs active geo-replication, MI failover groups and link feature, SQL on VM Always On AG, PostgreSQL flexible server zone-redundant HA and read replicas.
  - Read: SQL high availability https://learn.microsoft.com/en-us/azure/azure-sql/database/high-availability-sla-local-zone-redundancy · Failover groups https://learn.microsoft.com/en-us/azure/azure-sql/database/failover-group-sql-db · Active geo-replication https://learn.microsoft.com/en-us/azure/azure-sql/database/active-geo-replication-overview · PostgreSQL HA https://learn.microsoft.com/en-us/azure/reliability/reliability-postgresql-flexible-server
- [ ] Recommend a high availability solution for semi-structured and unstructured data
  - Know how to: Cosmos DB multi-region writes, automatic failover, availability zones, consistency vs availability trade-off; storage ZRS/GZRS and RA-GRS read access, account failover; Azure Files ZRS; Redis zone redundancy and geo-replication.
  - Read: Cosmos DB high availability https://learn.microsoft.com/en-us/azure/cosmos-db/high-availability · Cosmos DB global distribution https://learn.microsoft.com/en-us/azure/cosmos-db/distribute-data-globally · Storage redundancy https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy · Redis high availability https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-high-availability
