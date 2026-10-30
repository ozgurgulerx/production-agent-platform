# Domain 4: Design infrastructure solutions (30–35%)

Largest domain. Keep open: compute decision tree https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree and messaging choice https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/messaging

## 4.1 Design compute solutions

- [ ] Specify components of a compute solution based on workload requirements
  - Know how to: walk the decision tree (lift-and-shift → VM; container → Container Apps / AKS / ACI; web → App Service; event → Functions; batch → Batch); hosting model, DevOps, scalability, availability, security constraints.
  - Read: Compute decision tree (above) · Compute services comparison https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree#understand-the-basic-features · Well-Architected compute https://learn.microsoft.com/en-us/azure/well-architected/service-guides/
- [ ] Recommend a virtual machine-based solution
  - Know how to: VM families and sizes, disks, spot vs reserved vs savings plan, dedicated hosts, proximity placement groups, capacity reservations, Azure Virtual Desktop, Azure VMware Solution.
  - Read: VM sizes https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/overview · Dedicated hosts https://learn.microsoft.com/en-us/azure/virtual-machines/dedicated-hosts · Spot VMs https://learn.microsoft.com/en-us/azure/virtual-machines/spot-vms · Azure VMware Solution https://learn.microsoft.com/en-us/azure/azure-vmware/introduction
- [ ] Recommend a container-based solution
  - Know how to: Container Apps (KEDA scaling, Dapr, jobs) vs AKS (full control, Automatic mode) vs ACI vs App Service for containers; ACR tiers and geo-replication; when AKS is the only answer (custom networking, GPUs, operators).
  - Read: Container Apps overview https://learn.microsoft.com/en-us/azure/container-apps/overview · Container Apps vs other options https://learn.microsoft.com/en-us/azure/container-apps/compare-options · AKS overview https://learn.microsoft.com/en-us/azure/aks/what-is-aks · AKS baseline architecture https://learn.microsoft.com/en-us/azure/architecture/reference-architectures/containers/aks/baseline-aks · ACR https://learn.microsoft.com/en-us/azure/container-registry/container-registry-intro
- [ ] Recommend a serverless-based solution
  - Know how to: Functions hosting plans (Consumption, Flex Consumption, Premium, Dedicated, Container Apps), triggers/bindings, Durable Functions patterns, Logic Apps Standard vs Consumption, Container Apps serverless.
  - Read: Functions hosting options https://learn.microsoft.com/en-us/azure/azure-functions/functions-scale · Durable Functions https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview · Logic Apps overview https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-overview · Serverless web application reference https://learn.microsoft.com/en-us/azure/architecture/web-apps/serverless/architectures/web-app
- [ ] Recommend a compute solution for batch processing
  - Know how to: Azure Batch (pools, jobs, low-priority nodes), Container Apps jobs, Functions timers, Data Factory for data pipelines, AKS jobs; HPC (CycleCloud, HPC Pack, Managed Lustre).
  - Read: Azure Batch overview https://learn.microsoft.com/en-us/azure/batch/batch-technical-overview · Container Apps jobs https://learn.microsoft.com/en-us/azure/container-apps/jobs · Batch processing architecture https://learn.microsoft.com/en-us/azure/architecture/data-guide/big-data/batch-processing · HPC on Azure https://learn.microsoft.com/en-us/azure/architecture/topics/high-performance-computing

## 4.2 Design an application architecture

- [ ] Recommend a messaging architecture
  - Know how to: Storage queues vs Service Bus (queues, topics, sessions, dead-letter, transactions) vs Event Hubs vs Event Grid; competing consumers, claim check, queue-based load levelling.
  - Read: Messaging services choice https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/messaging · Service Bus overview https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview · Storage queues vs Service Bus https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-azure-and-service-bus-queues-compared-contrasted · Asynchronous messaging patterns https://learn.microsoft.com/en-us/azure/architecture/patterns/category/messaging
- [ ] Recommend an event-driven architecture
  - Know how to: Event Grid (push, pull, namespaces, MQTT), Event Hubs (streaming, capture, Kafka), Stream Analytics, event sourcing and CQRS, EDA reference architecture.
  - Read: Event-driven architecture style https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven · Event Grid overview https://learn.microsoft.com/en-us/azure/event-grid/overview · Event Hubs overview https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-about · Event sourcing pattern https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing
- [ ] Recommend a solution for API integration
  - Know how to: API Management tiers (Consumption, Basic v2, Standard v2, Premium v2, classic), gateway topologies (internal VNet, self-hosted gateway, workspaces), policies, developer portal, AI gateway capabilities; Front Door + APIM pattern.
  - Read: APIM overview https://learn.microsoft.com/en-us/azure/api-management/api-management-key-concepts · APIM tiers https://learn.microsoft.com/en-us/azure/api-management/api-management-features · APIM landing zone accelerator https://learn.microsoft.com/en-us/azure/architecture/example-scenario/integration/app-gateway-internal-api-management-function · AI gateway https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities · In repo: F09.
- [ ] Recommend a caching solution for applications
  - Know how to: Azure Cache for Redis tiers vs Azure Managed Redis, cache-aside, session state, CDN/Front Door caching, Cosmos DB integrated cache, App Service local cache.
  - Read: Azure Managed Redis https://learn.microsoft.com/en-us/azure/redis/overview · Cache for Redis tiers https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-overview · Caching guidance https://learn.microsoft.com/en-us/azure/architecture/best-practices/caching · Front Door caching https://learn.microsoft.com/en-us/azure/frontdoor/front-door-caching
- [ ] Recommend an application configuration management solution
  - Know how to: App Configuration (key-values, labels, feature flags, Key Vault references, snapshots) vs Key Vault vs app settings; external configuration store pattern.
  - Read: App Configuration overview https://learn.microsoft.com/en-us/azure/azure-app-configuration/overview · Feature management https://learn.microsoft.com/en-us/azure/azure-app-configuration/concept-feature-management · External configuration store pattern https://learn.microsoft.com/en-us/azure/architecture/patterns/external-configuration-store
- [ ] Recommend an automated deployment solution for applications
  - Know how to: Bicep / ARM / Terraform, template specs, deployment stacks, Azure Pipelines vs GitHub Actions with OIDC, deployment slots, blue-green and canary with Front Door / Traffic Manager / App Service slots, Azure Deployment Environments, Azure Developer CLI.
  - Read: IaC overview https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/considerations/infrastructure-as-code · Bicep overview https://learn.microsoft.com/en-us/devops/deliver/what-is-infrastructure-as-code · GitHub Actions for Azure https://learn.microsoft.com/en-us/azure/developer/github/github-actions · Deployment slots https://learn.microsoft.com/en-us/azure/app-service/deploy-staging-slots · Well-Architected safe deployment https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/safe-deployments

## 4.3 Design migrations

- [ ] Evaluate a migration solution that leverages the Microsoft Cloud Adoption Framework for Azure
  - Know how to: CAF phases (Strategy, Plan, Ready, Adopt: migrate/modernize/innovate, Govern, Manage, Secure); the 5 Rs (rehost, refactor, rearchitect, rebuild, replace); landing zone before first wave.
  - Read: CAF overview https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/overview · CAF Migrate https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/migrate/ · Migration strategies (5 Rs) https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/adopt/migrate-or-modernize
- [ ] Evaluate on-premises servers, data, and applications for migration
  - Know how to: Azure Migrate discovery and assessment (appliance, agentless dependency analysis), business case, Data Migration Assistant / Azure SQL assessment, App Service migration assistant, Azure Arc inventory.
  - Read: Azure Migrate overview https://learn.microsoft.com/en-us/azure/migrate/migrate-services-overview · Assessment overview https://learn.microsoft.com/en-us/azure/migrate/concepts-assessment-overview · Business case https://learn.microsoft.com/en-us/azure/migrate/concepts-business-case-calculation · Dependency analysis https://learn.microsoft.com/en-us/azure/migrate/concepts-dependency-visualization
- [ ] Recommend a solution for migrating workloads to infrastructure as a service (IaaS) and platform as a service (PaaS)
  - Know how to: Migrate and Modernize (agentless/agent-based VMware, Hyper-V, physical), AVS for VMware estates, App Service / AKS modernization paths, containerising with Migrate, test migration and cutover.
  - Read: Server migration https://learn.microsoft.com/en-us/azure/migrate/migrate-services-overview#azure-migrate-migration-and-modernization-tool · VMware agentless migration https://learn.microsoft.com/en-us/azure/migrate/tutorial-migrate-vmware · App modernization https://learn.microsoft.com/en-us/azure/migrate/tutorial-modernize-asp-net-appservice-code · Azure VMware Solution https://learn.microsoft.com/en-us/azure/azure-vmware/introduction
- [ ] Recommend a solution for migrating databases
  - Know how to: Azure Database Migration Service (online vs offline), Azure SQL migration extension for Azure Data Studio, MI link, backup/restore to URL, log replay service, SQL Server to Azure SQL target choice, Oracle/PostgreSQL/MySQL paths.
  - Read: DMS overview https://learn.microsoft.com/en-us/azure/dms/dms-overview · SQL migration guides https://learn.microsoft.com/en-us/data-migration/ · Managed Instance link https://learn.microsoft.com/en-us/azure/azure-sql/managed-instance/managed-instance-link-feature-overview · Log Replay Service https://learn.microsoft.com/en-us/azure/azure-sql/managed-instance/log-replay-service-overview
- [ ] Recommend a solution for migrating unstructured data
  - Know how to: AzCopy, Azure Storage Mover, Data Box family (offline), Azure File Sync, Data Factory for ongoing copy, Storage Migration Service for Windows file servers; choose by volume × bandwidth × time.
  - Read: Data transfer options https://learn.microsoft.com/en-us/azure/storage/common/storage-choose-data-transfer-solution · Storage Mover https://learn.microsoft.com/en-us/azure/storage-mover/service-overview · Data Box https://learn.microsoft.com/en-us/azure/databox/data-box-overview · Azure File Sync https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-introduction

## 4.4 Design network solutions

- [ ] Recommend a connectivity solution that connects Azure resources to the internet
  - Know how to: public IP SKUs, NAT Gateway for outbound, default outbound access retirement, Load Balancer outbound rules, Front Door vs Application Gateway vs Traffic Manager for inbound, DDoS Protection tiers, Bastion.
  - Read: Outbound connectivity options https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-outbound-connections · NAT Gateway https://learn.microsoft.com/en-us/azure/nat-gateway/nat-overview · Default outbound access https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/default-outbound-access · DDoS Protection https://learn.microsoft.com/en-us/azure/ddos-protection/ddos-protection-overview
- [ ] Recommend a connectivity solution that connects Azure resources to on-premises networks
  - Know how to: Site-to-Site VPN (gateway SKUs, active-active, BGP) vs ExpressRoute (circuit SKUs, Direct, Global Reach, FastPath, private vs Microsoft peering) vs Virtual WAN; hub-and-spoke vs vWAN; Private DNS resolver for hybrid DNS.
  - Read: VPN Gateway https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpngateways · ExpressRoute overview https://learn.microsoft.com/en-us/azure/expressroute/expressroute-introduction · Virtual WAN https://learn.microsoft.com/en-us/azure/virtual-wan/virtual-wan-about · Hub-spoke topology https://learn.microsoft.com/en-us/azure/architecture/networking/architecture/hub-spoke · Hybrid DNS https://learn.microsoft.com/en-us/azure/dns/dns-private-resolver-overview
- [ ] Recommend a solution to optimize network performance
  - Know how to: ExpressRoute FastPath, accelerated networking, proximity placement groups, Front Door and CDN for edge, Global Reach, VNet peering vs gateway transit, Azure Route Server, bandwidth of gateway SKUs.
  - Read: Accelerated networking https://learn.microsoft.com/en-us/azure/virtual-network/accelerated-networking-overview · ExpressRoute FastPath https://learn.microsoft.com/en-us/azure/expressroute/about-fastpath · Front Door overview https://learn.microsoft.com/en-us/azure/frontdoor/front-door-overview · VNet peering https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-peering-overview
- [ ] Recommend a solution to optimize network security
  - Know how to: NSG and ASG, Azure Firewall tiers (Basic/Standard/Premium: TLS inspection, IDPS), Firewall Manager, WAF on App Gateway/Front Door, Private Link and private endpoints vs service endpoints, forced tunnelling, Network Watcher, zero-trust network design.
  - Read: Azure Firewall https://learn.microsoft.com/en-us/azure/firewall/overview · Firewall SKU comparison https://learn.microsoft.com/en-us/azure/firewall/choose-firewall-sku · Private Link https://learn.microsoft.com/en-us/azure/private-link/private-link-overview · Service endpoints vs private endpoints https://learn.microsoft.com/en-us/azure/virtual-network/vnet-integration-for-azure-services · WAF https://learn.microsoft.com/en-us/azure/web-application-firewall/overview · Network security design area https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/network-topology-and-connectivity
- [ ] Recommend a load-balancing and routing solution
  - Know how to: the four-way choice (Front Door: global HTTP; Traffic Manager: DNS; Application Gateway: regional L7 with WAF; Load Balancer: regional L4), Gateway Load Balancer for NVAs, cross-region Load Balancer, user-defined routes and Route Server, Application Gateway for Containers.
  - Read: Load-balancing options https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/load-balancing-overview · Application Gateway https://learn.microsoft.com/en-us/azure/application-gateway/overview · Traffic Manager https://learn.microsoft.com/en-us/azure/traffic-manager/traffic-manager-overview · Load Balancer https://learn.microsoft.com/en-us/azure/load-balancer/load-balancer-overview · UDR https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-udr-overview
