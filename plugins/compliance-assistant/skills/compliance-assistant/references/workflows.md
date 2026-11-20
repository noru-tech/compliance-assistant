# Workflows

Each workflow assumes the session is already grounded (SKILL.md step 1). Tool names use the `noru:`
prefix. Anything that writes follows [safe-actions.md](safe-actions.md).

## Contents

- [Sequencing](#sequencing)
- [Gap analysis](#gap-analysis)
- [Advice](#advice)
- [Roadmap](#roadmap)
- [Audit readiness](#audit-readiness)
- [External audits](#external-audits)
- [Access reviews](#access-reviews)
- [Control drill-down](#control-drill-down)
- [Policies](#policies)
- [Risks](#risks)
- [Vendors](#vendors)
- [Supplier risk](#supplier-risk)
- [Trust center access](#trust-center-access)
- [Privacy](#privacy)
- [Tickets](#tickets)
- [My work](#my-work)

## Sequencing

"What should we do next?" or "What order should we do SOC 2 in?"

1. Resolve the framework from `noru:getOrganizationFrameworks`.
2. `noru:listFrameworkPlans`, then `noru:getFrameworkPlan` for that framework. Use
   `noru:getPlanWorkstream` to see the steps of one workstream.
3. `noru:getPendingControls` for controls that are not yet implemented or are waiting on review.
4. When the user wants a prioritized task list, call `noru:suggestComplianceTasks`. It needs
   `write:compliance` and creates suggestions, so call it only on request.
5. Answer with 3 to 5 next actions. Put blockers first: controls other work depends on, and missing
   owners. Name each control and step.

## Gap analysis

1. `noru:getComplianceOverview` gives counts by status: implemented, in progress, pending review,
   not implemented.
2. `noru:getOrganizationControls`, filtered to the framework, for the controls behind those counts.
3. ISO 27001: `noru:getStatementOfApplicability`, and `noru:getStatementOfApplicabilityTrace` for one
   control's justification. `noru:getNotApplicableSuggestions` lists controls that may be out of
   scope. Accepting them (`noru:acceptNotApplicableSuggestions`) is a write.
4. Group the gaps by theme (access, change management, vendors, people, and so on), not as one long
   list.

## Advice

"Is our MFA setup sufficient?", "Do we need a pen test?", "What does CC6.1 expect from us?"

1. `noru:checkGuidanceRequirements` with short topics or control IDs. Use the returned
   `companyContext`, and don't ask again for answers already saved there.
2. `noru:readGuidanceContent` for each relevant `sourceContent` page before you draw a conclusion
   from it.
3. Look at what is recorded: `noru:getControlStatus`, `noru:getEvidenceForControl`, and the policy
   behind the control (`noru:getPolicyControlMappings`).
4. Draft the advice, then check it with `noru:reviewGuidanceAdvice`.
5. Sufficiency questions: lead with "I cannot confirm that it is sufficient" or "Not yet" when the
   records show a gap or contradict what the company reports. Then name the conflicting facts.
   Obligation questions: separate what the source requires from what you recommend.
6. Fit the advice to the company's size and capacity. Small size is no exemption, and large size
   creates no extra mandate. Do not invent numeric thresholds.

## Roadmap

Only when the user asks for a roadmap, timeline, milestones or a target date.

1. Read the current plan with `noru:getFrameworkPlan`.
2. Confirm the target date and scope with the user.
3. `noru:setFrameworkPlanTargetDate` sets the target date and needs `write:compliance`. Changing
   plan steps, targets or leads (`noru:setFrameworkPlanStep`, `noru:updateFrameworkPlan`,
   `noru:setWorkstreamLead`) also needs the user's yes.

## Audit readiness

1. `noru:listInternalAudits`, then `noru:getInternalAuditReport` for open findings.
   `noru:getInternalAuditProgramme` shows planned coverage.
2. `noru:getStatementOfApplicability` (ISO) or `noru:getComplianceOverview` (SOC 2) for coverage.
3. Evidence: `noru:getOrganizationEvidence`, then `noru:getEvidenceHistory` for freshness and
   `noru:verifyEvidenceIntegrity` for tampering checks.
4. People: `noru:listMissingPolicyAcknowledgements` and training status from
   `noru:listTrainingCampaigns`.
5. If an external audit is under way, check its open requests and milestones (see
   [External audits](#external-audits)).
6. Report what an auditor would flag first: stale or missing evidence, open findings, policies not
   approved, missing acknowledgements, overdue access reviews. Say plainly that this is a readiness
   view, not an audit opinion.

## External audits

- `noru:listExternalAudits`, then `noru:getExternalAudit` for milestones and status.
- `noru:listExternalAuditRequests` for what the auditor has asked for, and
  `noru:getExternalAuditEvidence` for what has been shared.
- Answering a request (`noru:respondToAuditRequest`), responding to a finding
  (`noru:respondToExternalAuditFinding`), moving a milestone (`noru:setExternalAuditMilestoneStatus`,
  `noru:progressExternalAudit`) and exporting a package (`noru:requestAuditPackageExport`) are
  writes that the auditor may see. Confirm the exact wording and the files first.

## Access reviews

User access reviews are a common SOC 2 (CC6) and ISO 27001 (A.5.18) control.

1. `noru:listAccessReviews`, then `noru:getAccessReview` and `noru:getAccessReviewCoverage` to see
   which systems are in scope and how many accounts are still undecided.
2. `noru:listAccessReviewAccounts` for the accounts, and `noru:getAccessReviewActivity` for who
   decided what.
3. For guidance on running one, use `noru:getUserAccessReviewGuidance`.
4. Deciding accounts (`noru:decideAccessReviewAccounts`), signing off (`noru:signOffAccessReview`) and
   filing the result as evidence (`noru:fileAccessReviewEvidence`) are writes. A sign-off records a
   person's attestation, so the reviewer must make or confirm each decision themselves.

## Control drill-down

`noru:getControlContext` for what the control is and how it connects to other records.
`noru:getControlStatus` for its state and owner. `noru:getControlImplementationBrief` for how to
implement it at this company. `noru:getEvidenceForControl` for what proves it.
`noru:getRecordConnections` shows linked policies, risks and evidence.

## Policies

- `noru:getOrganizationPolicies`, or the resource `noru://policies/review-queue` for drafts and
  policies in review.
- `noru:getPolicyDetails` for content and version, `noru:getPolicyLogs` for history.
- `noru:listMissingPolicyAcknowledgements` shows who has not acknowledged a policy.
  `noru:requestPolicyAcknowledgement` sends requests to people, so confirm the recipients first.
- To change a policy, call `noru:previewChangeImpact` before `noru:updatePolicy`. For a service-level
  change, use `noru:previewServiceLevelChange`.

## Risks

- `noru:getHighRiskItems` first, then `noru:getOrganizationRisks`.
- `noru:getRiskDetails`, `noru:getRiskTreatments` and `noru:getRiskControlMappings` for one risk.
- `noru:getSecurityFindings` for findings that can be linked to risks.
- Creating, rescoring or closing risks are writes.

## Vendors

- `noru:getOrganizationVendors` gives tier, status and owner.
- `noru:getVendorDetails`, `noru:getVendorEvidence` (for example SOC 2 reports and DPAs) and
  `noru:getVendorContacts`.
- Flag high-tier vendors with missing or expired evidence first.

## Supplier risk

Only for organizations with supplier risk management (the `tprm` toolset). Use it for third-party
risk, DORA-style registers, contracts and supplier assessments.

- Overview: `noru:getSupplierSummary`, `noru:getSupplier`, `noru:getConcentration` and `noru:listCtpps`.
- Assessments: `noru:listAssessments`, `noru:getAssessment`, `noru:listVerdicts` and
  `noru:listSupplierFindings`, then `noru:getFindingThread`.
- Contracts: `noru:listContracts`, `noru:getContract`, `noru:getContractClauseCheck` and
  `noru:listUpcomingContractDeadlines`.
- Services and the supply chain: `noru:listServices`, `noru:listBusinessFunctions`,
  `noru:listSupplyChain` and `noru:listSubprocessors`.
- The register: `noru:listRegisterRuns`, `noru:getRegisterRun` and `noru:previewRegisterRun`.
- Waiting decisions: `noru:listProposals`, `noru:listApprovals` and `noru:listSignals`.
- Some supplier tools that sound like reads change records and need `write:vendors`:
  `noru:readSupplierEvidence`, `noru:checkTrustCenter`, `noru:draftVerdicts` and
  `noru:checkContractClauses`. Treat them as writes. Sending questions to a supplier
  (`noru:sendSupplierQuestions`) contacts an outside party, so confirm the recipient and the text.

## Trust center access

- `noru:listTrustAccessRequests` for pending requests for gated documents, and
  `noru:getTrustAccessRequest` for one request.
- `noru:listTrustViewers`, `noru:listTrustDocuments` and `noru:listTrustAccessEvents` for who can see
  what.
- Approving, denying or revoking access (`noru:approveTrustAccessRequest`,
  `noru:denyTrustAccessRequest`, `noru:revokeTrustViewer`) shares or withdraws confidential
  documents. Confirm the requester, the company and the documents first.

## Privacy

- `noru:getPrivacyOverview` and `noru:getRegulationCoverage` for GDPR and other regulations.
- `noru:getRopa` for the record of processing, and `noru:listProcessingActivities` and
  `noru:getProcessingActivity` for detail.
- `noru:listPrivacyAssessments` for DPIAs, and `noru:listPrivacyReviewItems` for items waiting on
  review.
- `noru:getAiRegister` for AI systems.

## Tickets

- `noru:getTaskTrackerStatus` shows whether a task tracker (such as Jira or Linear) is connected.
- `noru:getItemTickets` lists the tickets linked to a control, finding or evidence item.
- Creating or linking a ticket (`noru:createTicket`, `noru:linkExistingTicket`) writes to the outside
  tracker as well as Noru. Confirm the project, title and description.

## My work

`noru:getMyInbox` for items assigned to the user, `noru:listWorkflowTasks` for workflow tasks
waiting on people, and `noru:getMyTraining` for their own training. Approving or rejecting a task
(`noru:decideWorkflowTask`) is a write.
