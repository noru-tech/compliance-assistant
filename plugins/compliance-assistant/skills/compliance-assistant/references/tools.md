# Noru MCP tools by toolset

Generated from the Noru source by `scripts/refresh-tools-reference.ts`: 383 tools in
22 toolsets. The live list for the current connection comes from
`noru:getMcpCapabilities`, which wins over this file. A tool is listed only when the credential has
its scope **and** its toolset is active (see [scopes-and-toolsets.md](scopes-and-toolsets.md)).
`tprm` tools appear only for organizations with supplier risk management enabled.

Every `write:` tool changes the customer's workspace. Follow [safe-actions.md](safe-actions.md) for
each one.

## Contents

- [core](#core)
- [tprm](#tprm)
- [users](#users)
- [frameworks](#frameworks)
- [controls](#controls)
- [risks](#risks)
- [evidence](#evidence)
- [policies](#policies)
- [vendors](#vendors)
- [personnel](#personnel)
- [assets](#assets)
- [datamaps](#datamaps)
- [ai-inventory](#ai-inventory)
- [internal-audits](#internal-audits)
- [external-audits](#external-audits)
- [webhooks](#webhooks)
- [workflows](#workflows)
- [signals](#signals)
- [tickets](#tickets)
- [access-reviews](#access-reviews)
- [trust-access](#trust-access)
- [compliance](#compliance)
- [Resources](#resources)

## core

Always included: the organization, connection capabilities, the compliance overview and the guidance tools every answer starts from.

| Scope | Tools |
| --- | --- |
| `read:controls` | `readGuidanceContent`, `checkGuidanceRequirements`, `reviewGuidanceAdvice` |
| `read:organization` | `findOrganization`, `getMcpCapabilities`, `getCompanyProfile`, `getServiceLevels`, `getRecordConnections`, `previewChangeImpact`, `getComplianceOverview`, `getComplianceItems` |
| `read:users` | `getUser` |
| `write:organization` | `updateCompanyProfile`, `updateServiceLevels` |

## tprm

Supplier risk management: contracts, services, assessments, verdicts, findings, the register and supplier signals.

| Scope | Tools |
| --- | --- |
| `read:vendors` | `listLegalEntities`, `listContracts`, `getContract`, `getContractClauseCheck`, `listUpcomingContractDeadlines`, `listServices`, `getService`, `listBusinessFunctions`, `listSupplyChain`, `listSubprocessors`, `getVendorIdentity`, `findDuplicateVendors`, `listExternalRefs`, `listProposals`, `getProposalImpact`, `listApprovals`, `getSupplierQuestions`, `listConnectedApps`, `listSignals`, `getSignal`, `listRegisterRuns`, `getRegisterRun`, `previewRegisterRun`, `getRegisterRunChanges`, `downloadRegisterDraft`, `listAssessments`, `getConcentration`, `listCtpps`, `listSupplierFindings`, `getFindingThread`, `listExitAssessments`, `getExitAssessment`, `getOffboarding`, `getAssessment`, `listClosedAssessments`, `exportAuditPeriod`, `exportSupplierAudit`, `exportPortfolioReport`, `listVerdicts`, `getSupplierSummary`, `getSupplier`, `getTrustCenter`, `getSupplierServiceStatus`, `getSupplierServiceIncidents`, `getStatusAlertScheme`, `listStatusCatalog` |
| `write:vendors` | `createLegalEntity`, `updateLegalEntity`, `checkContractClauses`, `fillContractFromDocument`, `createContract`, `updateContract`, `createService`, `updateService`, `createBusinessFunction`, `updateBusinessFunction`, `linkServiceToFunction`, `addSupplyChainLink`, `updateSupplyChainLink`, `updateVendorIdentity`, `enrichVendorIdentity`, `syncVendor`, `removeExternalRef`, `decideProposal`, `decideProposals`, `delegateProposal`, `prepareSupplierQuestions`, `sendSupplierQuestions`, `addQuestionnaireTemplate`, `decideDiscoveredSuppliers`, `importExpenseExport`, `decideSignal`, `decideSignals`, `submitIntake`, `startRegisterRun`, `validateRegisterRun`, `applyRegisterIssueFix`, `requestRegisterApproval`, `approveRegisterRun`, `exportRegisterRun`, `deleteRegisterRun`, `importRegister`, `createFindingFromVerdict`, `requestFindingRemediation`, `addFindingComment`, `linkVendorToRisk`, `acceptRisk`, `createExitAssessment`, `updateExitAssessment`, `updateOffboardingItem`, `createAssessment`, `updateAssessment`, `sendAssessmentForReview`, `closeAssessment`, `readSupplierEvidence`, `setSupplierEvidenceType`, `draftVerdicts`, `confirmVerdict`, `overrideVerdict`, `checkTrustCenter`, `setTrustCenterUrl`, `setSupplierLifecycleStage`, `deleteContract`, `deleteService`, `deleteBusinessFunction`, `unlinkServiceFromFunction`, `removeSupplyChainLink`, `detectSupplierStatusPage`, `discoverSupplierStatusPages`, `addSupplierStatusMonitor`, `updateSupplierStatusMonitor`, `updateStatusAlertScheme`, `removeSupplierStatusMonitor` |

## users

The signed-in user and their own assigned training.

| Scope | Tools |
| --- | --- |
| `read:users` | `getRole`, `listRoles`, `getMyTraining`, `getMyInbox` |

## frameworks

Frameworks available and enabled for the organization, and the plan for each one.

| Scope | Tools |
| --- | --- |
| `read:frameworks` | `getAllFrameworks`, `getOrganizationFrameworks`, `getPlanWorkstream`, `listFrameworkPlans`, `getFrameworkPlan` |

## controls

Controls, their status, owners, context and implementation briefs, and the Statement of Applicability.

| Scope | Tools |
| --- | --- |
| `read:controls` | `getStatementOfApplicability`, `getStatementOfApplicabilityTrace`, `getNotApplicableSuggestions`, `getUserAccessReviewGuidance`, `getOrganizationControls`, `getPendingControls`, `getControlStatus`, `getControlContext`, `getControlImplementationBrief` |
| `write:controls` | `acceptNotApplicableSuggestions`, `updateControl`, `setControlStatus`, `setControlOwner` |

## risks

The risk register, treatments, control mappings and security findings.

| Scope | Tools |
| --- | --- |
| `read:risks` | `getOrganizationRisks`, `getRiskDetails`, `getRiskTreatments`, `getRiskControlMappings`, `getRiskLogs`, `getHighRiskItems`, `getRiskStatus`, `getSecurityFindings` |
| `write:risks` | `createRisk`, `updateRisk`, `deleteRisk`, `setRiskOwner`, `setRiskStatus`, `linkRiskToControl`, `unlinkRiskFromControl`, `createRiskTreatment`, `updateRiskTreatment`, `deleteRiskTreatment`, `setRiskTreatmentStatus`, `createSecurityFinding`, `updateSecurityFinding`, `deleteSecurityFinding`, `linkSecurityFindingToRisk`, `unlinkSecurityFindingFromRisk`, `bulkLinkSecurityFindingsToRisk` |

## evidence

Evidence records and their links to controls.

| Scope | Tools |
| --- | --- |
| `read:evidence` | `getOrganizationEvidence`, `getEvidenceItems`, `getEvidenceForControl`, `verifyEvidenceIntegrity`, `getEvidenceHistory` |
| `write:evidence` | `createEvidence`, `updateEvidence`, `deleteEvidence`, `linkEvidenceToControl`, `unlinkEvidenceFromControl` |

## policies

Policies, their content, versions, approvers and control mappings.

| Scope | Tools |
| --- | --- |
| `read:policies` | `previewServiceLevelChange`, `getOrganizationPolicies`, `getPolicyDetails`, `getPolicyControlMappings`, `getPolicyLogs` |
| `write:policies` | `createPolicy`, `updatePolicy`, `linkPolicyToControl`, `unlinkPolicyFromControl`, `setPolicyStatus`, `setPolicyApprover`, `setPolicyVersion`, `generatePolicies` |

## vendors

The vendor directory: vendors, contacts, owners, status and vendor evidence.

| Scope | Tools |
| --- | --- |
| `read:vendors` | `getOrganizationVendors`, `getVendorDetails`, `getMergedVendors`, `getVendorContacts`, `getVendorEvidence`, `getVendorLogs`, `getVendorPersonnel` |
| `write:vendors` | `createVendor`, `mergeVendors`, `unmergeVendor`, `updateVendor`, `deleteVendor`, `setVendorStatus`, `bulkSetVendorStatus`, `setVendorOwner`, `setVendorTier`, `addVendorContact`, `updateVendorContact`, `removeVendorContact`, `linkEvidenceToVendor`, `removeVendorEvidence` |

## personnel

People, training plans and campaigns, and policy acknowledgements.

| Scope | Tools |
| --- | --- |
| `read:personnel` | `getOrganizationPersonnel`, `listTrainingPlans`, `getTrainingPlanDetails`, `listTrainingCampaigns`, `getTrainingCampaignDetails`, `listMissingPolicyAcknowledgements`, `listTrainingPolicyOptions`, `listTrainingCourses` |
| `write:personnel` | `createPersonnel`, `updatePersonnel`, `deletePersonnel`, `recordManualTrainingCompletion`, `recordManualPolicyAcknowledgement`, `assignTraining`, `requestPolicyAcknowledgement`, `createTrainingPlan`, `updateTrainingPlan`, `deleteTrainingPlan`, `activateTrainingPlan`, `syncTrainingCampaignAssignmentStatuses`, `sendTrainingCampaignReminders`, `archiveTrainingCampaign`, `bulkArchiveTrainingCampaigns`, `bulkSendTrainingCampaignReminders`, `bulkSetTrainingCampaignStatus`, `bulkCancelTrainingAssignments`, `deleteTrainingCampaign` |

## assets

The asset inventory.

| Scope | Tools |
| --- | --- |
| `read:assets` | `getOrganizationAssets`, `getAssetInventorySummary` |
| `write:assets` | `createAsset`, `updateAsset`, `deleteAsset` |

## datamaps

Privacy: data map, processing activities (RoPA), privacy assessments, data sources and the AI register.

| Scope | Tools |
| --- | --- |
| `read:datamaps` | `getAiRegister`, `getPrivacyDataMap`, `getPrivacyOverview`, `listPrivacyReviewItems`, `getPrivacyReviewItem`, `getRegulationCoverage`, `listPrivacyDataSources`, `getPrivacyDataSource`, `listPrivacySystems`, `listPrivacyDatasets`, `listProcessingActivities`, `getProcessingActivity`, `getProcessingActivityLogs`, `getPrivacyDataMapLogs`, `getRopa`, `getPrivacyTaxonomy`, `listPrivacySecurityMeasures`, `getPrivacySettings`, `listPrivacyAssessments`, `getPrivacyAssessment`, `listAssessableRecords` |
| `write:datamaps` | `createProcessingActivity`, `updateProcessingActivity`, `archiveProcessingActivity`, `setProcessingActivityTransfers`, `setProcessingActivityRetentionRules`, `setProcessingActivityMeasures`, `createPrivacySecurityMeasure`, `updatePrivacySecurityMeasure`, `archivePrivacySecurityMeasure`, `updatePrivacySettings`, `updateCoveredRegulations`, `updatePrivacySystem`, `updatePrivacyDataSource`, `deletePrivacyDataSource`, `ingestDatamap`, `createPrivacyAssessment`, `updatePrivacyAssessment`, `deletePrivacyAssessment`, `linkPrivacyAssessmentRisk`, `unlinkPrivacyAssessmentRisk`, `reviewActivityAiSuggestion` |

## ai-inventory

Ingesting and reviewing an AI inventory.

| Scope | Tools |
| --- | --- |
| `write:ai-inventory` | `ingestAiInventory`, `reviewAiClassification`, `reviewAiFinding` |

## internal-audits

Internal audits, their findings and reports.

| Scope | Tools |
| --- | --- |
| `read:internal-audits` | `listInternalAudits`, `getInternalAudit`, `getInternalAuditReport`, `getInternalAuditProgramme`, `getInternalAuditChecklist` |
| `write:internal-audits` | `createInternalAudit`, `updateInternalAuditReport`, `addInternalAuditFinding`, `updateInternalAuditFindingStatus`, `completeInternalAudit`, `setInternalAuditProgramme`, `recordInternalAuditControlResults`, `refreshInternalAuditChecklist` |

## external-audits

External audits and their milestones.

| Scope | Tools |
| --- | --- |
| `read:external-audits` | `listExternalAudits`, `getExternalAudit`, `getExternalAuditEvidence`, `listExternalAuditRequests` |
| `write:external-audits` | `progressExternalAudit`, `requestAuditPackageExport`, `respondToAuditRequest`, `respondToExternalAuditFinding`, `setExternalAuditMilestoneStatus`, `updateExternalAudit`, `createExternalAuditDraft`, `updateExternalAuditDraft` |

## webhooks

Webhook endpoints and deliveries (admin).

| Scope | Tools |
| --- | --- |
| `read:webhooks` | `listWebhookEndpoints`, `listWebhookDeliveries`, `getWebhookDelivery` |
| `write:webhooks` | `createWebhookEndpoint`, `updateWebhookEndpoint`, `rotateWebhookSecret`, `deleteWebhookEndpoint`, `redeliverWebhook`, `sendWebhookTest` |

## workflows

Workflows, their runs and the tasks waiting on people.

| Scope | Tools |
| --- | --- |
| `read:workflows` | `listWorkflows`, `getWorkflow`, `listWorkflowRuns`, `getWorkflowRun`, `exportWorkflowRun`, `listWorkflowTasks` |
| `write:workflows` | `runWorkflow`, `cancelWorkflowRun`, `createWorkflowDraft`, `updateWorkflowDraft`, `decideWorkflowTask` |

## signals

The signal types workflows can react to.

| Scope | Tools |
| --- | --- |
| `read:signals` | `listSignalTypes` |

## tickets

Tickets in the organization's task tracker for findings and evidence.

| Scope | Tools |
| --- | --- |
| `read:tickets` | `getTaskTrackerStatus`, `getItemTickets` |
| `write:tickets` | `createTicket`, `linkExistingTicket`, `removeTicketLink` |

## access-reviews

User access reviews: accounts, decisions, follow-ups and sign-off.

| Scope | Tools |
| --- | --- |
| `read:access-reviews` | `listAccessReviews`, `getAccessReview`, `listAccessReviewAccounts`, `listAccessReviewSystemUsers`, `listAccessReviewConnectedSystems`, `getAccessReviewCoverage`, `getAccessReviewActivity` |
| `write:access-reviews` | `createAccessReview`, `updateAccessReview`, `importAccessReviewAccounts`, `startAccessReview`, `cancelAccessReview`, `deleteAccessReview`, `decideAccessReviewAccounts`, `completeAccessReviewFollowUp`, `setAccessReviewAccountRoles`, `addAccessReviewRoleType`, `setAccessReviewSystemCritical`, `setAccessReviewSystemsInScope`, `signOffAccessReview`, `fileAccessReviewEvidence` |

## trust-access

Trust center access: requests for gated documents, approved viewers and the documents on offer.

| Scope | Tools |
| --- | --- |
| `read:trust-access` | `listTrustAccessRequests`, `getTrustAccessRequest`, `listTrustViewers`, `listTrustDocuments`, `listTrustAccessEvents` |
| `write:trust-access` | `approveTrustAccessRequest`, `denyTrustAccessRequest`, `revokeTrustViewer` |

## compliance

Compliance plans and suggested tasks, marking framework plan steps and setting their target and lead, and setting who leads a workstream.

| Scope | Tools |
| --- | --- |
| `write:compliance` | `answerWorkstreamQuestions`, `setWorkstreamTask`, `setWorkstreamLead`, `setFrameworkPlanStep`, `updateFrameworkPlan`, `setTrustServicesCategories`, `suggestComplianceTasks`, `setFrameworkPlanTargetDate` |

## Resources

| URI | What it holds |
| --- | --- |
| `noru://frameworks/compliance-overview` | Aggregated compliance metrics for each enabled framework |
| `noru://policies/review-queue` | Policies in draft or review, with owners |
| `noru://schemas/ai-inventory-manifest` | JSON Schema for `ingestAiInventory` input |
