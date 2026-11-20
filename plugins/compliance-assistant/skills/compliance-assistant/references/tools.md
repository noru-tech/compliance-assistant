# Noru MCP tools by scope

This is a snapshot of Noru MCP contract 1.1.0. The live list for the current connection comes from
`noru:getMcpCapabilities`, which wins over this file. A tool is listed only when the credential has
its scope **and** its toolset is active (see [scopes-and-toolsets.md](scopes-and-toolsets.md)).

Write tools change the customer's workspace. Follow [safe-actions.md](safe-actions.md) for every one.

## Read tools

| Scope | Tools |
| --- | --- |
| `read:organization` | `findOrganization`, `getCompanyProfile`, `getComplianceItems`, `getComplianceOverview`, `getMcpCapabilities`, `getRecordConnections`, `getServiceLevels`, `previewChangeImpact` |
| `read:frameworks` | `getAllFrameworks`, `getOrganizationFrameworks`, `getFrameworkPlan`, `listFrameworkPlans`, `getPlanWorkstream` |
| `read:controls` | `checkGuidanceRequirements`, `readGuidanceContent`, `reviewGuidanceAdvice`, `getOrganizationControls`, `getPendingControls`, `getControlContext`, `getControlStatus`, `getControlImplementationBrief`, `getNotApplicableSuggestions`, `getStatementOfApplicability`, `getStatementOfApplicabilityTrace`, `getUserAccessReviewGuidance` |
| `read:policies` | `getOrganizationPolicies`, `getPolicyDetails`, `getPolicyLogs`, `getPolicyControlMappings`, `previewServiceLevelChange` |
| `read:evidence` | `getOrganizationEvidence`, `getEvidenceItems`, `getEvidenceForControl`, `getEvidenceHistory`, `verifyEvidenceIntegrity` |
| `read:risks` | `getOrganizationRisks`, `getHighRiskItems`, `getRiskDetails`, `getRiskStatus`, `getRiskLogs`, `getRiskTreatments`, `getRiskControlMappings`, `getSecurityFindings` |
| `read:vendors` | `getOrganizationVendors`, `getVendorDetails`, `getVendorContacts`, `getVendorEvidence`, `getVendorLogs`, `getVendorPersonnel`, `getMergedVendors` |
| `read:personnel` | `getOrganizationPersonnel`, `listMissingPolicyAcknowledgements`, `listTrainingPlans`, `getTrainingPlanDetails`, `listTrainingCampaigns`, `getTrainingCampaignDetails`, `listTrainingCourses`, `listTrainingPolicyOptions` |
| `read:users` | `getUser`, `getRole`, `listRoles`, `getMyInbox`, `getMyTraining` |
| `read:assets` | `getOrganizationAssets`, `getAssetInventorySummary` |
| `read:datamaps` | `getPrivacyOverview`, `getPrivacySettings`, `getPrivacyTaxonomy`, `getPrivacyDataMap`, `getPrivacyDataMapLogs`, `getRopa`, `getRegulationCoverage`, `listProcessingActivities`, `getProcessingActivity`, `getProcessingActivityLogs`, `listPrivacyAssessments`, `getPrivacyAssessment`, `listAssessableRecords`, `listPrivacyDataSources`, `getPrivacyDataSource`, `listPrivacyDatasets`, `listPrivacySystems`, `listPrivacySecurityMeasures`, `listPrivacyReviewItems`, `getPrivacyReviewItem`, `getAiRegister` |
| `read:internal-audits` | `listInternalAudits`, `getInternalAudit`, `getInternalAuditChecklist`, `getInternalAuditProgramme`, `getInternalAuditReport` |
| `read:workflows` | `listWorkflows`, `getWorkflow`, `listWorkflowRuns`, `getWorkflowRun`, `exportWorkflowRun`, `listWorkflowTasks` |
| `read:webhooks` | `listWebhookEndpoints`, `listWebhookDeliveries`, `getWebhookDelivery` |
| `read:signals` | `listSignalTypes` |

## Write tools

| Scope | Tools |
| --- | --- |
| `write:compliance` | `suggestComplianceTasks`, `createCompliancePlan`, `updateFrameworkPlan`, `setFrameworkPlanStep`, `setWorkstreamLead`, `setWorkstreamTask`, `answerWorkstreamQuestions`, `setTrustServicesCategories` |
| `write:controls` | `setControlStatus`, `setControlOwner`, `updateControl`, `acceptNotApplicableSuggestions` |
| `write:policies` | `createPolicy`, `updatePolicy`, `setPolicyStatus`, `setPolicyVersion`, `setPolicyApprover`, `linkPolicyToControl`, `unlinkPolicyFromControl`, `generatePolicies` |
| `write:evidence` | `createEvidence`, `updateEvidence`, `deleteEvidence`, `linkEvidenceToControl`, `unlinkEvidenceFromControl` |
| `write:risks` | `createRisk`, `updateRisk`, `deleteRisk`, `setRiskOwner`, `setRiskStatus`, `createRiskTreatment`, `updateRiskTreatment`, `deleteRiskTreatment`, `setRiskTreatmentStatus`, `linkRiskToControl`, `unlinkRiskFromControl`, `createSecurityFinding`, `updateSecurityFinding`, `deleteSecurityFinding`, `linkSecurityFindingToRisk`, `unlinkSecurityFindingFromRisk`, `bulkLinkSecurityFindingsToRisk` |
| `write:vendors` | `createVendor`, `updateVendor`, `deleteVendor`, `setVendorOwner`, `setVendorStatus`, `setVendorTier`, `bulkSetVendorStatus`, `addVendorContact`, `updateVendorContact`, `removeVendorContact`, `linkEvidenceToVendor`, `removeVendorEvidence`, `mergeVendors`, `unmergeVendor` |
| `write:personnel` | `createPersonnel`, `updatePersonnel`, `deletePersonnel`, `requestPolicyAcknowledgement`, `recordManualPolicyAcknowledgement`, `createTrainingPlan`, `updateTrainingPlan`, `deleteTrainingPlan`, `activateTrainingPlan`, `assignTraining`, `recordManualTrainingCompletion`, `sendTrainingCampaignReminders`, `bulkSendTrainingCampaignReminders`, `bulkSetTrainingCampaignStatus`, `bulkCancelTrainingAssignments`, `archiveTrainingCampaign`, `bulkArchiveTrainingCampaigns`, `deleteTrainingCampaign`, `syncTrainingCampaignAssignmentStatuses` |
| `write:assets` | `createAsset`, `updateAsset`, `deleteAsset` |
| `write:datamaps` | `ingestDatamap`, `createProcessingActivity`, `updateProcessingActivity`, `archiveProcessingActivity`, `setProcessingActivityMeasures`, `setProcessingActivityRetentionRules`, `setProcessingActivityTransfers`, `createPrivacyAssessment`, `updatePrivacyAssessment`, `deletePrivacyAssessment`, `linkPrivacyAssessmentRisk`, `unlinkPrivacyAssessmentRisk`, `updatePrivacyDataSource`, `deletePrivacyDataSource`, `updatePrivacySystem`, `createPrivacySecurityMeasure`, `updatePrivacySecurityMeasure`, `archivePrivacySecurityMeasure`, `updatePrivacySettings`, `updateCoveredRegulations`, `reviewActivityAiSuggestion` |
| `write:ai-inventory` | `ingestAiInventory`, `reviewAiClassification`, `reviewAiFinding` |
| `write:internal-audits` | `createInternalAudit`, `completeInternalAudit`, `addInternalAuditFinding`, `updateInternalAuditFindingStatus`, `recordInternalAuditControlResults`, `refreshInternalAuditChecklist`, `setInternalAuditProgramme`, `updateInternalAuditReport` |
| `write:workflows` | `createWorkflowDraft`, `updateWorkflowDraft`, `runWorkflow`, `cancelWorkflowRun`, `decideWorkflowTask` |
| `write:webhooks` | `createWebhookEndpoint`, `updateWebhookEndpoint`, `deleteWebhookEndpoint`, `rotateWebhookSecret`, `redeliverWebhook`, `sendWebhookTest` |

## Resources

| URI | What it holds |
| --- | --- |
| `noru://frameworks/compliance-overview` | Aggregated compliance metrics for each enabled framework |
| `noru://policies/review-queue` | Policies in draft or review, with owners |
| `noru://schemas/ai-inventory-manifest` | JSON Schema for `ingestAiInventory` input |
