// Four model deployments on an existing Foundry account. Same result as deploy_models.sh.
// az deployment group create -g <rg> -f deployments.bicep -p main.bicepparam
param accountName string
param skuName string = 'GlobalStandard'
param deployments array = [
  { name: 'gpt-5-mini', model: 'gpt-5-mini', version: '', format: 'OpenAI', capacity: 50 }
  { name: 'text-embedding-3-small', model: 'text-embedding-3-small', version: '', format: 'OpenAI', capacity: 50 }
  { name: 'gpt-realtime', model: 'gpt-realtime', version: '', format: 'OpenAI', capacity: 1 }
]

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' existing = {
  name: accountName
}

@batchSize(1) // deployments on one account must be created sequentially
resource dep 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = [for d in deployments: {
  parent: account
  name: d.name
  sku: { name: skuName, capacity: d.capacity }
  properties: {
    model: union({ format: d.format, name: d.model }, empty(d.version) ? {} : { version: d.version })
    versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
  }
}]

output deploymentNames array = [for (d, i) in deployments: dep[i].name]
