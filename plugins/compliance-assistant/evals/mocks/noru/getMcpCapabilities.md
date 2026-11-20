{
  "organization": {
    "id": "org_demo",
    "name": "Example Co"
  },
  "connection": {
    "server": "noru-mcp-server",
    "contractVersion": "1.1.0",
    "tokenType": "oauth",
    "grantedScopes": [
      "read:organization",
      "read:frameworks",
      "read:controls",
      "read:policies",
      "read:evidence",
      "read:risks",
      "write:compliance",
      "write:controls"
    ],
    "readonly": false
  },
  "toolsets": [
    {
      "name": "core",
      "active": true
    },
    {
      "name": "frameworks",
      "active": true
    },
    {
      "name": "controls",
      "active": true
    },
    {
      "name": "policies",
      "active": true
    },
    {
      "name": "evidence",
      "active": true
    },
    {
      "name": "risks",
      "active": true
    },
    {
      "name": "compliance",
      "active": true
    },
    {
      "name": "vendors",
      "active": false
    },
    {
      "name": "datamaps",
      "active": false
    }
  ]
}
