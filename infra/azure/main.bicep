param location string = resourceGroup().location
param suffix string = uniqueString(resourceGroup().id)

var tags = {
  project: 'LLM Inference Optimization Platform'
  product: 'TokenSRE'
  purpose: 'model-routing-evaluation-evidence'
  website: 'a2zsoc.com'
}

resource logs 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'tokensre-law-${suffix}'
  location: location
  tags: tags
  properties: {
    retentionInDays: 30
    sku: {name: 'PerGB2018'}
  }
}

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: 'tokensre${suffix}'
  location: location
  tags: tags
  sku: {name: 'Standard_LRS'}
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

resource evaluations 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  name: '${storage.name}/default/evaluation-receipts'
  properties: {publicAccess: 'None'}
}

resource insights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'tokensre-ai-${suffix}'
  location: location
  kind: 'web'
  tags: tags
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logs.id
  }
}

output workspaceName string = logs.name
output storageName string = storage.name
output insightsName string = insights.name
