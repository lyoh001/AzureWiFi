param location string = resourceGroup().location
param prefix string = replace(resourceGroup().name, 'rg', '')
// param prefix string = concat(replace(resourceGroup().name, 'rg', ''), substring(newGuid(), 0, 7))

resource logic_apps 'Microsoft.Logic/workflows@2019-05-01' = {
  location: location
  name: '${prefix}logicapp'
  properties: {
    definition: {
      '$schema': 'https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#'
      triggers: {
        manual: {
          type: 'request'
          kind: 'http'
        }
      }
    }
  }
}
